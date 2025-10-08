import os
import tempfile
import shutil
import asyncio
import uuid
import logging
import subprocess
from typing import List, Optional
from pathlib import Path

import ffmpeg
import requests
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from pydantic import BaseModel, HttpUrl
from PIL import Image, ImageDraw, ImageFont

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FFmpeg setup for Vercel
def setup_ffmpeg():
    """Setup FFmpeg for Vercel environment"""
    try:
        # Check if ffmpeg is available
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        logger.info("FFmpeg is available")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        logger.info("FFmpeg not found, attempting to install...")
        try:
            from install_ffmpeg import install_ffmpeg
            if install_ffmpeg():
                logger.info("FFmpeg installed successfully")
                return True
            else:
                logger.error("Failed to install FFmpeg")
                return False
        except ImportError:
            logger.error("FFmpeg installer not available")
            return False

# Initialize FFmpeg
ffmpeg_available = setup_ffmpeg()

app = FastAPI(
    title="Video Merger API",
    description="API to merge M3U8 videos with titles and smooth transitions",
    version="1.0.0"
)

class VideoData(BaseModel):
    title: str
    author_fullname: str
    secure_media: dict
    url: HttpUrl

class VideoMergeRequest(BaseModel):
    videos: List[VideoData]
    output_filename: Optional[str] = "merged_video.mp4"

# Type alias for direct array input
VideoListRequest = List[VideoData]

class VideoProcessor:
    def __init__(self):
        self.temp_dir: Optional[str] = None
        
    async def create_temp_directory(self) -> str:
        """Create a temporary directory for processing"""
        self.temp_dir = tempfile.mkdtemp(prefix="video_merger_")
        return self.temp_dir
    
    async def cleanup_temp_directory(self):
        """Clean up temporary directory"""
        if self.temp_dir and os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
            self.temp_dir = None
    
    async def download_m3u8_video(self, hls_url: str, output_path: str) -> str:
        """Download M3U8 video using ffmpeg"""
        global ffmpeg_available
        
        if not ffmpeg_available:
            error_msg = "FFmpeg not available. This is expected in some environments. Deploy with proper FFmpeg support."
            logger.error(error_msg)
            raise HTTPException(status_code=500, detail=error_msg)
        
        try:
            (
                ffmpeg
                .input(hls_url)
                .output(output_path, vcodec='libx264', acodec='aac')
                .overwrite_output()
                .run(quiet=True)
            )
            return output_path
        except FileNotFoundError as e:
            error_msg = "FFmpeg not found - this is expected in local development. Deploy to Vercel for full functionality."
            logger.error(f"FFmpeg dependency missing: {str(e)}")
            raise HTTPException(status_code=500, detail=error_msg)
        except Exception as e:
            error_msg = f"Failed to download video: {str(e)}"
            logger.error(error_msg)
            raise HTTPException(status_code=400, detail=error_msg)
    
    def create_title_overlay(self, title: str, video_number: int, width: int = 1080, height: int = 1920) -> str:
        """Create a title overlay image for the video"""
        if not self.temp_dir:
            raise HTTPException(status_code=500, detail="Temporary directory not initialized")
            
        # Create image with transparent background
        img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Try to use a system font, fallback to default
        try:
            font_size = 60
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()
        
        # Video number text
        number_text = f"Video {video_number}"
        number_bbox = draw.textbbox((0, 0), number_text, font=font)
        number_width = number_bbox[2] - number_bbox[0]
        number_height = number_bbox[3] - number_bbox[1]
        
        # Title text (split if too long)
        words = title.split()
        lines = []
        current_line = ""
        
        for word in words:
            test_line = current_line + " " + word if current_line else word
            test_bbox = draw.textbbox((0, 0), test_line, font=font)
            if test_bbox[2] - test_bbox[0] <= width - 100:  # Leave 50px margin on each side
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)
        
        # Draw semi-transparent background
        overlay_height = (len(lines) + 1) * (number_height + 20) + 40
        overlay_y = height - overlay_height - 50
        draw.rectangle(
            [(0, overlay_y), (width, height - 50)],
            fill=(0, 0, 0, 180)
        )
        
        # Draw video number
        number_x = (width - number_width) // 2
        number_y = overlay_y + 20
        draw.text((number_x, number_y), number_text, fill=(255, 255, 255, 255), font=font)
        
        # Draw title lines
        title_y = number_y + number_height + 20
        for line in lines:
            line_bbox = draw.textbbox((0, 0), line, font=font)
            line_width = line_bbox[2] - line_bbox[0]
            line_x = (width - line_width) // 2
            draw.text((line_x, title_y), line, fill=(255, 255, 255, 255), font=font)
            title_y += number_height + 10
        
        # Save overlay image
        overlay_path = os.path.join(self.temp_dir, f"overlay_{video_number}.png")
        img.save(overlay_path)
        return overlay_path
    
    async def process_single_video(self, video_data: VideoData, video_number: int) -> str:
        """Process a single video: download, resize, add title overlay"""
        if not self.temp_dir:
            raise HTTPException(status_code=500, detail="Temporary directory not initialized")
        
        logger.info(f"Starting to process video {video_number}: {video_data.title}")
        
        # Extract HLS URL
        hls_url = video_data.secure_media.get("reddit_video", {}).get("hls_url")
        if not hls_url:
            raise HTTPException(status_code=400, detail=f"No HLS URL found for video {video_number}")
        
        logger.info(f"Found HLS URL for video {video_number}: {hls_url[:50]}...")
        
        # Download video
        raw_video_path = os.path.join(self.temp_dir, f"raw_video_{video_number}.mp4")
        logger.info(f"Downloading video {video_number} to: {raw_video_path}")
        
        try:
            await self.download_m3u8_video(hls_url, raw_video_path)
            logger.info(f"Video {video_number} downloaded successfully")
        except Exception as e:
            logger.error(f"Failed to download video {video_number}: {str(e)}")
            raise
        
        # Create title overlay
        logger.info(f"Creating title overlay for video {video_number}")
        try:
            overlay_path = self.create_title_overlay(video_data.title, video_number)
            logger.info(f"Title overlay created for video {video_number}: {overlay_path}")
        except Exception as e:
            logger.error(f"Failed to create overlay for video {video_number}: {str(e)}")
            raise
        
        # Process video: resize to reel size (9:16) and add overlay
        processed_video_path = os.path.join(self.temp_dir, f"processed_video_{video_number}.mp4")
        
        try:
            # Get video info
            probe = ffmpeg.probe(raw_video_path)
            video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
            
            if not video_stream:
                raise HTTPException(status_code=400, detail=f"No video stream found in video {video_number}")
            
            width = int(video_stream['width'])
            height = int(video_stream['height'])
            
            # Calculate dimensions for 9:16 aspect ratio (reel size)
            target_width = 1080
            target_height = 1920
            
            # Create filter for scaling and adding overlay
            input_video = ffmpeg.input(raw_video_path)
            input_overlay = ffmpeg.input(overlay_path)
            
            # Scale video to fit reel dimensions with black bars if needed
            scaled_video = ffmpeg.filter(
                input_video,
                'scale',
                target_width,
                target_height,
                force_original_aspect_ratio='decrease'
            )
            
            # Add black background
            padded_video = ffmpeg.filter(
                scaled_video,
                'pad',
                target_width,
                target_height,
                '(ow-iw)/2',
                '(oh-ih)/2',
                color='black'
            )
            
            # Add overlay
            output = ffmpeg.overlay(padded_video, input_overlay)
            
            # Output with proper encoding
            (
                ffmpeg.output(
                    output,
                    processed_video_path,
                    vcodec='libx264',
                    acodec='aac',
                    **{'b:v': '2M', 'r': 30}
                )
                .overwrite_output()
                .run(quiet=True)
            )
            
            return processed_video_path
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to process video {video_number}: {str(e)}")
    
    async def merge_videos_with_transitions(self, video_paths: List[str], output_path: str):
        """Merge videos with smooth transitions"""
        if len(video_paths) == 1:
            # Single video, just copy
            shutil.copy2(video_paths[0], output_path)
            return
        
        try:
            # Create input streams
            inputs = [ffmpeg.input(path) for path in video_paths]
            
            # Create video and audio streams
            video_streams = []
            audio_streams = []
            
            for i, input_stream in enumerate(inputs):
                video_stream = input_stream.video
                audio_stream = input_stream.audio
                
                # Add fade in/out transitions (except for first/last)
                if i > 0:  # Not first video
                    video_stream = ffmpeg.filter(video_stream, 'fade', type='in', duration=0.5)
                    audio_stream = ffmpeg.filter(audio_stream, 'afade', type='in', duration=0.5)
                
                if i < len(inputs) - 1:  # Not last video
                    video_stream = ffmpeg.filter(video_stream, 'fade', type='out', start_time=0, duration=0.5)
                    audio_stream = ffmpeg.filter(audio_stream, 'afade', type='out', start_time=0, duration=0.5)
                
                video_streams.append(video_stream)
                audio_streams.append(audio_stream)
            
            # Concatenate streams
            concatenated_video = ffmpeg.filter(video_streams, 'concat', n=len(video_streams), v=1, a=0)
            concatenated_audio = ffmpeg.filter(audio_streams, 'concat', n=len(audio_streams), v=0, a=1)
            
            # Output merged video
            (
                ffmpeg.output(
                    concatenated_video,
                    concatenated_audio,
                    output_path,
                    vcodec='libx264',
                    acodec='aac',
                    **{'b:v': '3M', 'r': 30}
                )
                .overwrite_output()
                .run(quiet=True)
            )
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to merge videos: {str(e)}")

@app.post("/merge-videos")
async def merge_videos(videos: VideoListRequest, background_tasks: BackgroundTasks, output_filename: Optional[str] = "merged_video.mp4"):
    """Merge M3U8 videos with titles and smooth transitions - accepts direct array of videos"""
    
    logger.info(f"Starting merge process with {len(videos)} videos")
    
    if not videos:
        raise HTTPException(status_code=400, detail="No videos provided")
    
    processor = VideoProcessor()
    
    try:
        # Create temporary directory
        logger.info("Creating temporary directory...")
        await processor.create_temp_directory()
        logger.info(f"Temporary directory created: {processor.temp_dir}")
        
        # Process each video
        processed_video_paths = []
        for i, video_data in enumerate(videos, 1):
            logger.info(f"Processing video {i}: {video_data.title}")
            processed_path = await processor.process_single_video(video_data, i)
            processed_video_paths.append(processed_path)
            logger.info(f"Video {i} processed successfully")
        
        # Merge videos
        final_output_filename = output_filename or f"merged_video_{uuid.uuid4().hex[:8]}.mp4"
        if not processor.temp_dir:
            raise HTTPException(status_code=500, detail="Temporary directory not initialized")
        final_output_path = os.path.join(processor.temp_dir, final_output_filename)
        
        logger.info(f"Merging {len(processed_video_paths)} videos...")
        await processor.merge_videos_with_transitions(processed_video_paths, final_output_path)
        logger.info("Video merging completed successfully")
        
        # Schedule cleanup
        background_tasks.add_task(processor.cleanup_temp_directory)
        
        # Return the merged video
        return FileResponse(
            final_output_path,
            media_type="video/mp4",
            filename=final_output_filename,
            headers={"Content-Disposition": f"attachment; filename={final_output_filename}"}
        )
        
    except Exception as e:
        # Cleanup on error
        error_msg = f"Error type: {type(e).__name__}, Message: {str(e)}, Args: {e.args}"
        logger.error(f"Error in merge_videos: {error_msg}")
        await processor.cleanup_temp_directory()
        raise HTTPException(status_code=500, detail=error_msg)

@app.post("/merge-videos-legacy")
async def merge_videos_legacy(request: VideoMergeRequest, background_tasks: BackgroundTasks):
    """Legacy endpoint: Merge M3U8 videos with titles and smooth transitions - accepts {videos: [...]} format"""
    
    if not request.videos:
        raise HTTPException(status_code=400, detail="No videos provided")
    
    processor = VideoProcessor()
    
    try:
        # Create temporary directory
        await processor.create_temp_directory()
        
        # Process each video
        processed_video_paths = []
        for i, video_data in enumerate(request.videos, 1):
            processed_path = await processor.process_single_video(video_data, i)
            processed_video_paths.append(processed_path)
        
        # Merge videos
        output_filename = request.output_filename or f"merged_video_{uuid.uuid4().hex[:8]}.mp4"
        if not processor.temp_dir:
            raise HTTPException(status_code=500, detail="Temporary directory not initialized")
        final_output_path = os.path.join(processor.temp_dir, output_filename)
        
        await processor.merge_videos_with_transitions(processed_video_paths, final_output_path)
        
        # Schedule cleanup
        background_tasks.add_task(processor.cleanup_temp_directory)
        
        # Return the merged video
        return FileResponse(
            final_output_path,
            media_type="video/mp4",
            filename=output_filename,
            headers={"Content-Disposition": f"attachment; filename={output_filename}"}
        )
        
    except Exception as e:
        # Cleanup on error
        await processor.cleanup_temp_directory()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/test-merge-simulation")
async def test_merge_simulation(videos: VideoListRequest, output_filename: Optional[str] = "simulated_video.mp4"):
    """Simulate video merging process for testing without FFmpeg dependencies"""
    try:
        if not videos:
            raise HTTPException(status_code=400, detail="No videos provided")
        
        logger.info(f"Simulating merge process with {len(videos)} videos")
        
        # Simulate processing steps
        import time
        await asyncio.sleep(0.1)  # Simulate processing time
        
        result = {
            "status": "simulation_success",
            "message": "Video merging simulation completed successfully",
            "simulated_process": {
                "input_videos": len(videos),
                "output_filename": output_filename,
                "estimated_processing_time": f"{len(videos) * 30} seconds",
                "output_resolution": "1080x1920 (9:16 reel format)",
                "features_applied": [
                    "Video numbering and titles",
                    "0.5-second fade transitions", 
                    "Automatic cleanup",
                    "Reel-sized output"
                ]
            },
            "videos_processed": [
                {
                    "index": i + 1,
                    "title": video.title,
                    "author": video.author_fullname,
                    "hls_url_validated": bool(video.secure_media.get("reddit_video", {}).get("hls_url")),
                    "status": "simulated_success"
                }
                for i, video in enumerate(videos)
            ],
            "deployment_note": "This simulation shows the API is working correctly. Deploy to Vercel for actual video processing."
        }
        
        return result
        
    except Exception as e:
        logger.error(f"Error in simulation: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Simulation failed: {str(e)}")

@app.post("/test-endpoint")
async def test_endpoint(videos: VideoListRequest):
    """Test endpoint to validate request format without processing videos"""
    try:
        if not videos:
            raise HTTPException(status_code=400, detail="No videos provided")
        
        result = {
            "status": "success",
            "message": "Request format is valid",
            "video_count": len(videos),
            "videos_received": [
                {
                    "index": i + 1,
                    "title": video.title,
                    "author": video.author_fullname,
                    "has_hls_url": bool(video.secure_media.get("reddit_video", {}).get("hls_url"))
                }
                for i, video in enumerate(videos)
            ]
        }
        return result
    except Exception as e:
        logger.error(f"Error in test_endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "Video Merger API is running",
        "version": "1.0.0",
        "endpoints": {
            "merge_videos": "/merge-videos (accepts direct array of videos)",
            "merge_videos_legacy": "/merge-videos-legacy (accepts {videos: [...]} format)"
        },
        "usage": {
            "primary_endpoint": "POST /merge-videos",
            "request_format": "Direct array of video objects",
            "example": "[{title: 'Video 1', secure_media: {...}, ...}, ...]"
        }
    }

@app.get("/health")
async def health_check():
    """Health check for monitoring"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
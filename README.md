# Video Merger API

A FastAPI application that merges M3U8 videos into a single reel-sized video with titles and smooth transitions. Designed to be deployed on Vercel and used with n8n workflows.

## Features

- ✅ Download and process M3U8 (HLS) videos
- ✅ Resize videos to reel format (9:16 aspect ratio, 1080x1920)
- ✅ Add video titles and numbering as overlays
- ✅ Smooth fade transitions between videos
- ✅ Automatic cleanup of temporary files
- ✅ Vercel deployment ready
- ✅ n8n compatible API

## API Endpoints

### POST /merge-videos

Merges multiple M3U8 videos into a single video file.

**Request Body:**
```json
{
  "videos": [
    {
      "title": "he learned a good lesson",
      "author_fullname": "t2_9hw8f8o3",
      "secure_media": {
        "reddit_video": {
          "hls_url": "https://v.redd.it/8hjc3ez0hktf1/HLSPlaylist.m3u8?a=1762433138%2CM2Q4NDhlMDBlZjkzMTZkOGFmMWZmYmNkYjkzMjIxMmYxOGIxMmMzMzJhNjE0OTZjZDU2MzQ2YjJmYmQyMGIwNQ%3D%3D&v=1&f=sd"
        }
      },
      "url": "https://v.redd.it/8hjc3ez0hktf1"
    }
  ],
  "output_filename": "merged_video.mp4"
}
```

**Response:**
Returns the merged video file as a downloadable MP4.

### GET /

Health check and API information.

### GET /health

Simple health check endpoint.

## Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the development server:
```bash
uvicorn main:app --reload
```

3. Access the API at `http://localhost:8000`
4. View API documentation at `http://localhost:8000/docs`

## Deployment on Vercel

1. Install Vercel CLI:
```bash
npm i -g vercel
```

2. Deploy:
```bash
vercel
```

The `vercel.json` configuration file is already set up for Python deployment.

## Usage with n8n

1. Use HTTP Request node to send POST request to `/merge-videos`
2. Set the request body with your video data array
3. The response will be the merged video file
4. Use additional nodes to handle the downloaded video file as needed

## Video Processing Details

- **Input Format:** M3U8/HLS streams
- **Output Format:** MP4 (H.264/AAC)
- **Resolution:** 1080x1920 (9:16 aspect ratio for reels)
- **Transitions:** 0.5-second fade in/out between videos
- **Titles:** Overlaid at the bottom with video numbering
- **Cleanup:** Temporary files are automatically deleted after processing

## Requirements

- Python 3.8+
- FFmpeg (automatically handled on Vercel)
- Internet connection for downloading M3U8 streams

## Error Handling

The API includes comprehensive error handling for:
- Invalid M3U8 URLs
- Network download failures
- Video processing errors
- File system issues
- Automatic cleanup on errors

## Limitations

- Maximum file size depends on Vercel's limits (512MB for Pro plans)
- Processing time depends on video length and count
- Requires stable internet connection for M3U8 downloads
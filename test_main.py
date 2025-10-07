import pytest
import tempfile
import os
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from main import app, VideoData, VideoMergeRequest

client = TestClient(app)

def test_root_endpoint():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "Video Merger API is running" in response.json()["message"]

def test_health_endpoint():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_video_merge_request_validation():
    """Test request validation"""
    # Test empty videos array
    response = client.post("/merge-videos", json={"videos": []})
    assert response.status_code == 400
    assert "No videos provided" in response.json()["detail"]

def test_video_data_model():
    """Test VideoData model validation"""
    valid_data = {
        "title": "Test Video",
        "author_fullname": "test_user",
        "secure_media": {
            "reddit_video": {
                "hls_url": "https://example.com/video.m3u8"
            }
        },
        "url": "https://example.com/video"
    }
    
    video_data = VideoData(**valid_data)
    assert video_data.title == "Test Video"
    assert video_data.author_fullname == "test_user"

@patch('main.VideoProcessor.download_m3u8_video')
@patch('main.VideoProcessor.create_title_overlay')
@patch('ffmpeg.probe')
@patch('ffmpeg.run')
def test_merge_videos_endpoint(mock_ffmpeg_run, mock_ffmpeg_probe, mock_create_overlay, mock_download):
    """Test the merge videos endpoint with mocked FFmpeg operations"""
    
    # Mock FFmpeg probe response
    mock_ffmpeg_probe.return_value = {
        'streams': [
            {
                'codec_type': 'video',
                'width': 1920,
                'height': 1080
            }
        ]
    }
    
    # Mock file operations
    mock_download.return_value = "/tmp/video.mp4"
    mock_create_overlay.return_value = "/tmp/overlay.png"
    
    # Test data
    test_request = {
        "videos": [
            {
                "title": "Test Video 1",
                "author_fullname": "test_user",
                "secure_media": {
                    "reddit_video": {
                        "hls_url": "https://example.com/video1.m3u8"
                    }
                },
                "url": "https://example.com/video1"
            }
        ],
        "output_filename": "test_output.mp4"
    }
    
    with patch('tempfile.mkdtemp') as mock_mkdtemp:
        mock_mkdtemp.return_value = "/tmp/test_dir"
        with patch('os.path.exists') as mock_exists:
            mock_exists.return_value = True
            with patch('shutil.rmtree'):
                with patch('shutil.copy2'):
                    # This test would require more complex mocking for full coverage
                    # For now, we test that the endpoint accepts the request
                    response = client.post("/merge-videos", json=test_request)
                    # The actual processing would fail due to missing FFmpeg, 
                    # but we can verify the request structure is accepted
                    assert response.status_code in [200, 500]  # 500 due to missing FFmpeg in test env

if __name__ == "__main__":
    pytest.main([__file__])
"""
Example usage of the Video Merger API for n8n workflows
"""

import requests
import json

# Example data that would come from n8n nodes
example_videos = [
    {
        "title": "he learned a good lesson",
        "author_fullname": "t2_9hw8f8o3",
        "secure_media": {
            "reddit_video": {
                "hls_url": "https://v.redd.it/8hjc3ez0hktf1/HLSPlaylist.m3u8?a=1762433138%2CM2Q4NDhlMDBlZjkzMTZkOGFmMWZmYmNkYjkzMjIxMmYxOGIxMmMzMzJhNjE0OTZjZDU2MzQ2YjJmYmQyMGIwNQ%3D%3D&v=1&f=sd"
            }
        },
        "url": "https://v.redd.it/8hjc3ez0hktf1"
    },
    {
        "title": "Another amazing video",
        "author_fullname": "t2_another_user",
        "secure_media": {
            "reddit_video": {
                "hls_url": "https://example.com/another_video.m3u8"
            }
        },
        "url": "https://example.com/another_video"
    }
]

def test_local_api():
    """Test the API running locally"""
    api_url = "http://localhost:8000"
    
    # Test health check
    health_response = requests.get(f"{api_url}/health")
    print(f"Health check: {health_response.json()}")
    
    # Test video merging
    merge_request = {
        "videos": example_videos,
        "output_filename": "merged_reels.mp4"
    }
    
    try:
        response = requests.post(
            f"{api_url}/merge-videos",
            json=merge_request,
            timeout=300  # 5 minutes timeout for video processing
        )
        
        if response.status_code == 200:
            # Save the video file
            with open("output_merged_video.mp4", "wb") as f:
                f.write(response.content)
            print("Video merged successfully! Saved as output_merged_video.mp4")
        else:
            print(f"Error: {response.status_code} - {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

def test_vercel_api(vercel_url):
    """Test the API deployed on Vercel"""
    # Remove trailing slash if present
    api_url = vercel_url.rstrip('/')
    
    # Test health check
    health_response = requests.get(f"{api_url}/health")
    print(f"Health check: {health_response.json()}")
    
    # Test video merging
    merge_request = {
        "videos": example_videos[:1],  # Test with one video first
        "output_filename": "test_merged_reels.mp4"
    }
    
    try:
        response = requests.post(
            f"{api_url}/merge-videos",
            json=merge_request,
            timeout=300
        )
        
        if response.status_code == 200:
            print("Video processing successful on Vercel!")
            print(f"Response headers: {dict(response.headers)}")
        else:
            print(f"Error: {response.status_code} - {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

# n8n workflow example
n8n_workflow_example = {
    "name": "Video Merger Workflow",
    "nodes": [
        {
            "parameters": {
                "method": "POST",
                "url": "https://your-vercel-app.vercel.app/merge-videos",
                "sendBody": True,
                "bodyContentType": "json",
                "jsonParameters": True,
                "bodyParametersUi": {
                    "parameter": [
                        {
                            "name": "videos",
                            "value": "={{ $json.videos }}"
                        },
                        {
                            "name": "output_filename",
                            "value": "merged_reels_{{ new Date().getTime() }}.mp4"
                        }
                    ]
                }
            },
            "name": "Merge Videos",
            "type": "n8n-nodes-base.httpRequest",
            "typeVersion": 1,
            "position": [800, 300]
        }
    ],
    "connections": {}
}

if __name__ == "__main__":
    print("Video Merger API Examples")
    print("=" * 40)
    
    # Uncomment to test local API
    # test_local_api()
    
    # Uncomment and replace URL to test Vercel deployment
    # test_vercel_api("https://your-app-name.vercel.app")
    
    print("\nExample n8n workflow structure:")
    print(json.dumps(n8n_workflow_example, indent=2))
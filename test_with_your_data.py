import requests
import json

# Your provided video data
video_data = [
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
        "title": "Bro must have lost a bet",
        "author_fullname": "t2_1p18mk321r",
        "secure_media": {
            "reddit_video": {
                "hls_url": "https://v.redd.it/mqylx4hjtitf1/HLSPlaylist.m3u8?a=1762433138%2COTUxODE5MDUwMTIxYmEwM2M4MTk5ZTBmYjg1MzllOGZhZTBhNDE3YzhkY2IzOWExNWI1YmRkNTBhMjkyZTM3Ng%3D%3D&v=1&f=sd"
            }
        },
        "url": "https://v.redd.it/mqylx4hjtitf1"
    },
    {
        "title": "Wth is this",
        "author_fullname": "t2_kx59g8gl",
        "secure_media": {
            "reddit_video": {
                "hls_url": "https://v.redd.it/i9q2g3shiktf1/HLSPlaylist.m3u8?a=1762433138%2CZDcwMTI5YWM2ZTU4ZmE1MWFmODhiMzdmYjY1ZmZlZGY2NGUyMjlhNDNkODZjNTU2YzQ0MWM3NjY5ZjZkZjM4Zg%3D%3D&v=1&f=sd"
            }
        },
        "url": "https://v.redd.it/i9q2g3shiktf1"
    },
    {
        "title": "Extras from Walking the dead sets",
        "author_fullname": "t2_1kfoi79e31",
        "secure_media": {
            "reddit_video": {
                "hls_url": "https://v.redd.it/vc92fc99aktf1/HLSPlaylist.m3u8?a=1762433138%2CMmI2MGY5ZDA0MmYyOGNlNTI4YjI0YzBmZmE0OTY0NDY4ZmQ1MTQzMzk3OThiOThkMzljMWY3ZDY2MzQxZWRkNQ%3D%3D&v=1&f=sd"
            }
        },
        "url": "https://v.redd.it/vc92fc99aktf1"
    },
    {
        "title": "Death by Snu Snu",
        "author_fullname": "t2_a5l9z61h",
        "secure_media": {
            "reddit_video": {
                "hls_url": "https://v.redd.it/elq20k4ynmtf1/HLSPlaylist.m3u8?a=1762433138%2CYzE1MjhiMGNkMzc4MTlmODkxNjI3YWYxYjgyYjEwNGViNTM4NTU3NzkzZDEwM2QxMzBlODc0MzhlNmFjOGNhNQ%3D%3D&v=1&f=sd"
            }
        },
        "url": "https://v.redd.it/elq20k4ynmtf1"
    },
    {
        "title": "kid trying wasabi for the first time 🤣🤣",
        "author_fullname": "t2_9hw8f8o3",
        "secure_media": {
            "reddit_video": {
                "hls_url": "https://v.redd.it/g1x925oolitf1/HLSPlaylist.m3u8?a=1762433138%2CY2EzNmU3MzlhNDQwYTE4OGZmNDU5ZjM2NTdhMWZiNGI4NTI5YjExMjk1MjI2MTkwYTg2Yjk1MTRiYjMwZTBkYQ%3D%3D&v=1&f=sd"
            }
        },
        "url": "https://v.redd.it/g1x925oolitf1"
    },
    {
        "title": "One way to clean the dip stick",
        "author_fullname": "t2_1g6jubbjze",
        "secure_media": {
            "reddit_video": {
                "hls_url": "https://v.redd.it/sfnnwc8enhtf1/HLSPlaylist.m3u8?a=1762433138%2CNDViNGFkMzI5NmVjMDYzZjFmY2VlMGQwNGUyNTg3YmQ4NGIzOTA4YWY5ZjE0YjE2NGQ3NjczYjRhNGIxMDk0Yg%3D%3D&v=1&f=sd"
            }
        },
        "url": "https://v.redd.it/sfnnwc8enhtf1"
    },
    {
        "title": "Mom, dinner is ready",
        "author_fullname": "t2_1a96kp4swd",
        "secure_media": {
            "reddit_video": {
                "hls_url": "https://v.redd.it/ycifzof5aotf1/HLSPlaylist.m3u8?a=1762433138%2CZDBiNzgyNTdmZjFmNmM5YTNjOWRhYzZhOGY4M2RmOGU5MjkyMjFlNjdjM2ZhYTBiOGFhMzIwMzRlYTM0ZWI4Nw%3D%3D&v=1&f=sd"
            }
        },
        "url": "https://v.redd.it/ycifzof5aotf1"
    },
    {
        "title": "The plot twist of all plot twists!",
        "author_fullname": "t2_1gnm5bvcxf",
        "secure_media": {
            "reddit_video": {
                "hls_url": "https://v.redd.it/ugqge1h9lotf1/HLSPlaylist.m3u8?a=1762433138%2CYzhjYWRkMzAyOGZhZTk4MDQxOGQ5MTVmN2E4OWM3MDBiMzgxNzAwOTkxMWI3ZTkwN2UyY2Y2MWMyNTIwZDc1YQ%3D%3D&v=1&f=sd"
            }
        },
        "url": "https://v.redd.it/ugqge1h9lotf1"
    },
    {
        "title": "A lack of racism can actually be more hurtful than racism itself",
        "author_fullname": "t2_pf0g3",
        "secure_media": {
            "reddit_video": {
                "hls_url": "https://v.redd.it/qkq0y5h82otf1/HLSPlaylist.m3u8?a=1762433138%2CNGE4MGIzYzM1NGQ3YWI1NmMxMjUzYTNkZGE3OTAwZWY2OWJlOTIxOGI4NjZmYTM2YzQ0NzhjMWM1YjdiZjJjZQ%3D%3D&v=1&f=sd"
            }
        },
        "url": "https://v.redd.it/qkq0y5h82otf1"
    }
]

def test_api():
    """Test the video merger API with your data"""
    api_url = "http://localhost:8000"
    
    # Test health check first
    try:
        health_response = requests.get(f"{api_url}/health")
        print(f"✅ Health check: {health_response.json()}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Health check failed: {e}")
        return
    
    # Test with first 3 videos to start (faster testing)
    # Now sending direct array instead of {videos: [...]}
    test_request = video_data[:3]  # Direct array format
    
    print(f"\n🚀 Starting video merge process with {len(test_request)} videos...")
    print("📋 Videos to merge:")
    for i, video in enumerate(test_request, 1):
        print(f"   {i}. {video['title']}")
    
    try:
        response = requests.post(
            f"{api_url}/merge-videos",
            json=test_request,  # Direct array
            params={"output_filename": "test_merged_reels.mp4"},  # As query parameter
            timeout=600  # 10 minutes timeout for video processing
        )
        
        if response.status_code == 200:
            # Save the video file
            with open("merged_output.mp4", "wb") as f:
                f.write(response.content)
            print("✅ Video merged successfully! Saved as 'merged_output.mp4'")
            print(f"📊 File size: {len(response.content) / (1024*1024):.2f} MB")
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
            
    except requests.exceptions.Timeout:
        print("⏰ Request timed out - video processing took too long")
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")

def test_all_videos():
    """Test with all 10 videos"""
    api_url = "http://localhost:8000"
    
    # Direct array format
    test_request = video_data  # All 10 videos as direct array
    
    print(f"\n🚀 Starting FULL video merge process with {len(test_request)} videos...")
    print("📋 All videos to merge:")
    for i, video in enumerate(test_request, 1):
        print(f"   {i}. {video['title']}")
    
    try:
        response = requests.post(
            f"{api_url}/merge-videos",
            json=test_request,  # Direct array
            params={"output_filename": "full_merged_reels.mp4"},
            timeout=1200  # 20 minutes timeout for full processing
        )
        
        if response.status_code == 200:
            # Save the video file
            with open("full_merged_output.mp4", "wb") as f:
                f.write(response.content)
            print("✅ All videos merged successfully! Saved as 'full_merged_output.mp4'")
            print(f"📊 File size: {len(response.content) / (1024*1024):.2f} MB")
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
            
    except requests.exceptions.Timeout:
        print("⏰ Request timed out - video processing took too long")
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")

if __name__ == "__main__":
    print("🎬 Video Merger API Test")
    print("=" * 50)
    
    # Test with first 3 videos
    test_api()
    
    # Uncomment to test with all 10 videos (will take much longer)
    print("\n" + "="*50)
    print("To test with all 10 videos, uncomment the line below:")
    print("# test_all_videos()")
    
    # test_all_videos()  # Uncomment this line to test with all videos
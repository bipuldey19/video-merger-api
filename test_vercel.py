import requests
import json

# Your 14-video dataset
your_videos = [
    {
        "title": "The plot twist of all plot twists!",
        "author_fullname": "t2_1gnm5bvcxf",
        "secure_media": {
            "reddit_video": {
                "hls_url": "https://v.redd.it/ugqge1h9lotf1/HLSPlaylist.m3u8?a=1762493081%2CZjUxMGJmODc2NmE1ZGY4OWVhMTYwOWFjNzNiZDIxNDY1NTFhMjAyYTViNGUyNWRhOWZmNTdhZjViMDdhYWQ4OA%3D%3D&v=1&f=sd"
            }
        },
        "url": "https://v.redd.it/ugqge1h9lotf1"
    },
    {
        "title": "Mom, dinner is ready",
        "author_fullname": "t2_1a96kp4swd",
        "secure_media": {
            "reddit_video": {
                "hls_url": "https://v.redd.it/ycifzof5aotf1/HLSPlaylist.m3u8?a=1762493081%2CNGJjNmJkZTI1ZmI4OTFjNWZlNGNhZDhiNzI2NmNhODJhMjU2NTkxZWFiM2YwYzJjN2M1YzYzMjAxMzJhZWQxNA%3D%3D&v=1&f=sd"
            }
        },
        "url": "https://v.redd.it/ycifzof5aotf1"
    },
    {
        "title": "Death by Snu Snu",
        "author_fullname": "t2_a5l9z61h",
        "secure_media": {
            "reddit_video": {
                "hls_url": "https://v.redd.it/elq20k4ynmtf1/HLSPlaylist.m3u8?a=1762493081%2CNjExOTI0ZDg3MzRmY2E2M2UyYTY1Y2VlNmQwNzJhMzhjNTAyNThmYjg3Nzc2MjhhMTU2YzFkMjA3MDU2NDFjNA%3D%3D&v=1&f=sd"
            }
        },
        "url": "https://v.redd.it/elq20k4ynmtf1"
    }
    # Add your other 11 videos here...
]

def test_vercel_deployment(vercel_url):
    """Test the Vercel deployment with simulation"""
    print(f"🧪 Testing Vercel Deployment: {vercel_url}")
    print("=" * 60)
    
    # Remove trailing slash
    base_url = vercel_url.rstrip('/')
    
    # Test 1: Health check
    print("\n📋 Step 1: Health Check")
    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        if response.status_code == 200:
            print("✅ API is online and healthy")
        else:
            print(f"⚠️ Health check returned {response.status_code}")
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False
    
    # Test 2: Format validation
    print("\n📋 Step 2: Format Validation")
    try:
        response = requests.post(
            f"{base_url}/test-endpoint",
            json=your_videos[:3],  # Test with 3 videos
            timeout=15
        )
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Format validation passed - {result['video_count']} videos detected")
        else:
            print(f"❌ Format validation failed: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Format validation error: {e}")
        return False
    
    # Test 3: Simulation (should work on Vercel)
    print("\n📋 Step 3: Processing Simulation")
    try:
        response = requests.post(
            f"{base_url}/test-merge-simulation",
            json=your_videos[:3],
            params={"output_filename": "test_simulation.mp4"},
            timeout=20
        )
        if response.status_code == 200:
            result = response.json()
            print("✅ Simulation successful!")
            print(f"   📊 Status: {result['status']}")
            print(f"   🎬 Videos: {result['simulated_process']['input_videos']}")
            print(f"   ⏱️ Est. time: {result['simulated_process']['estimated_processing_time']}")
            print(f"   📐 Format: {result['simulated_process']['output_resolution']}")
        else:
            print(f"❌ Simulation failed: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Simulation error: {e}")
        return False
    
    # Test 4: Actual processing (will fail due to FFmpeg but should give clear error)
    print("\n📋 Step 4: Actual Processing Test (Expected to fail with clear error)")
    try:
        response = requests.post(
            f"{base_url}/merge-videos",
            json=your_videos[:1],  # Just 1 video for quick test
            timeout=30
        )
        if response.status_code == 500:
            error = response.json().get('detail', '')
            if 'FFmpeg' in error:
                print(f"✅ Clear FFmpeg error message: {error}")
            else:
                print(f"⚠️ Unclear error: {error}")
        else:
            print(f"🎉 Unexpected success! Processing might actually work: {response.status_code}")
    except Exception as e:
        print(f"⚠️ Processing test error (expected): {e}")
    
    return True

def main():
    print("🚀 Vercel Deployment Test")
    print("Enter your Vercel deployment URL below:")
    print("Example: https://video-merger-api-abc123.vercel.app")
    
    vercel_url = input("\nVercel URL: ").strip()
    
    if not vercel_url:
        print("❌ No URL provided")
        return
    
    if not vercel_url.startswith('http'):
        vercel_url = f"https://{vercel_url}"
    
    success = test_vercel_deployment(vercel_url)
    
    if success:
        print("\n🎯 Summary:")
        print("✅ Your API structure is working on Vercel")
        print("✅ JSON format validation works perfectly")
        print("✅ Simulation endpoint provides full testing capability")
        print("❌ FFmpeg not available (expected limitation)")
        print("\n🚀 Next Steps:")
        print("1. Use simulation endpoint for n8n workflow testing")
        print("2. Deploy to Railway/Render for full video processing")
        print("3. Check DEPLOYMENT.md for detailed instructions")
    else:
        print("\n❌ Some tests failed - check deployment status")

if __name__ == "__main__":
    main()
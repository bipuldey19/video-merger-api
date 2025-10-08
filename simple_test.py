import requests
import json

def test_health():
    try:
        response = requests.get("http://localhost:8000/health")
        print(f"Health check: {response.status_code} - {response.json()}")
        return True
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

def test_root():
    try:
        response = requests.get("http://localhost:8000/")
        print(f"Root endpoint: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return True
    except Exception as e:
        print(f"Root endpoint failed: {e}")
        return False

def test_simple_request():
    # Simple test with minimal data
    test_data = [
        {
            "title": "Test Video",
            "author_fullname": "test_user",
            "secure_media": {
                "reddit_video": {
                    "hls_url": "https://test.m3u8"
                }
            },
            "url": "https://test.com"
        }
    ]
    
    try:
        response = requests.post(
            "http://localhost:8000/merge-videos",
            json=test_data,
            timeout=10
        )
        print(f"Merge endpoint: {response.status_code}")
        if response.status_code != 200:
            print(f"Error response: {response.text}")
        else:
            print("Success!")
        return response.status_code == 200
    except Exception as e:
        print(f"Merge endpoint failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing API endpoints...")
    print("=" * 40)
    
    if test_health():
        print("✅ Health check passed")
    else:
        print("❌ Health check failed")
        exit(1)
    
    print()
    if test_root():
        print("✅ Root endpoint passed")
    else:
        print("❌ Root endpoint failed")
    
    print()
    print("Testing merge endpoint with simple data...")
    if test_simple_request():
        print("✅ Merge endpoint test passed")
    else:
        print("❌ Merge endpoint test failed")
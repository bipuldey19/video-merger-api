import requests
import json

def test_new_endpoint():
    test_data = [
        {
            "title": "Test Video 1",
            "author_fullname": "test_user",
            "secure_media": {
                "reddit_video": {
                    "hls_url": "https://test.m3u8"
                }
            },
            "url": "https://test.com"
        },
        {
            "title": "Test Video 2",
            "author_fullname": "test_user_2",
            "secure_media": {
                "reddit_video": {
                    "hls_url": "https://test2.m3u8"
                }
            },
            "url": "https://test2.com"
        }
    ]
    
    try:
        response = requests.post(
            "http://localhost:8000/test-endpoint",
            json=test_data,
            timeout=10
        )
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Test endpoint works!")
            print(json.dumps(response.json(), indent=2))
        else:
            print(f"❌ Error: {response.text}")
    except Exception as e:
        print(f"❌ Request failed: {e}")

if __name__ == "__main__":
    print("🧪 Testing the new test endpoint...")
    test_new_endpoint()
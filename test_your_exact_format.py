import requests
import json

# Your exact data format
your_data = [
  {
    "title": "The plot twist of all plot twists!",
    "author_fullname": "t2_1gnm5bvcxf",
    "secure_media": {
      "reddit_video": {
        "hls_url": "https://v.redd.it/ugqge1h9lotf1/HLSPlaylist.m3u8?a=1762493081%2CZjUxMGJmODc2NmE1ZGY4OWVhMTYwOWFjNzNiZDIxNDY1NTFhMjAyYTViNGUyNWRhOWZmNTdhZjViMDdhYWQ4OA%3D%3D&amp;v=1&amp;f=sd"
      }
    },
    "url": "https://v.redd.it/ugqge1h9lotf1"
  },
  {
    "title": "Mom, dinner is ready",
    "author_fullname": "t2_1a96kp4swd",
    "secure_media": {
      "reddit_video": {
        "hls_url": "https://v.redd.it/ycifzof5aotf1/HLSPlaylist.m3u8?a=1762493081%2CNGJjNmJkZTI1ZmI4OTFjNWZlNGNhZDhiNzI2NmNhODJhMjU2NTkxZWFiM2YwYzJjN2M1YzYzMjAxMzJhZWQxNA%3D%3D&amp;v=1&amp;f=sd"
      }
    },
    "url": "https://v.redd.it/ycifzof5aotf1"
  },
  {
    "title": "Death by Snu Snu",
    "author_fullname": "t2_a5l9z61h",
    "secure_media": {
      "reddit_video": {
        "hls_url": "https://v.redd.it/elq20k4ynmtf1/HLSPlaylist.m3u8?a=1762493081%2CNjExOTI0ZDg3MzRmY2E2M2UyYTY1Y2VlNmQwNzJhMzhjNTAyNThmYjg3Nzc2MjhhMTU2YzFkMjA3MDU2NDFjNA%3D%3D&amp;v=1&amp;f=sd"
      }
    },
    "url": "https://v.redd.it/elq20k4ynmtf1"
  },
  {
    "title": "When your coworker brings their own talent to the workplace",
    "author_fullname": "t2_3grio7i1",
    "secure_media": {
      "reddit_video": {
        "hls_url": "https://v.redd.it/r8531v2fvptf1/HLSPlaylist.m3u8?a=1762493081%2CYzJjOTUwZTUwMDFhMGI0ODk0MzQxYzc2ZDgyMjgyZTU1NmEwYzVhYTBmN2ZjMjRlZDgxZmQ1MzFmODA4MTUxYg%3D%3D&amp;v=1&amp;f=sd"
      }
    },
    "url": "https://v.redd.it/r8531v2fvptf1"
  },
  {
    "title": "Yall better hide yo kids, hide yo wife, and hide yo husbands in these times.",
    "author_fullname": "t2_5rlj1pnx",
    "secure_media": {
      "reddit_video": {
        "hls_url": "https://v.redd.it/v4m8lsngsrtf1/HLSPlaylist.m3u8?a=1762493081%2CZWNiNTk5MmNhYzczNzE2NGM2NDZjMmVlMDU4YTk2NzEzMjhkZTg4YWVhODY3OThmNTg0MjgzMjI5MWFhMGVkZQ%3D%3D&amp;v=1&amp;f=sd"
      }
    },
    "url": "https://v.redd.it/v4m8lsngsrtf1"
  },
  {
    "title": "Dude loves his job.",
    "author_fullname": "t2_suet3mfqn",
    "secure_media": {
      "reddit_video": {
        "hls_url": "https://v.redd.it/xizxw8zz8ptf1/HLSPlaylist.m3u8?a=1762493081%2CZjNmMGNmYmMzMjZmZmMyZDUwOGM5MzNmZmEwNTc1NDUxNzRjZDI5MzM2MTlkZWI2YWY1MDM2OWRjNjQyOWVlNw%3D%3D&amp;v=1&amp;f=sd"
      }
    },
    "url": "https://v.redd.it/xizxw8zz8ptf1"
  },
  {
    "title": "My school days latent",
    "author_fullname": "t2_1s5ihgl0d4",
    "secure_media": {
      "reddit_video": {
        "hls_url": "https://v.redd.it/ri33awq24qtf1/HLSPlaylist.m3u8?a=1762493081%2CZWY4ODMxMTg3MjlkYjA2ZjE2YzBmZDRiODVhZGMyYWI2ZWVhMGJhM2JkMDA1NGVjZDU1MjU1OTYyOTg4Nzg1YQ%3D%3D&amp;v=1&amp;f=sd"
      }
    },
    "url": "https://v.redd.it/ri33awq24qtf1"
  },
  {
    "title": "Sleepy boy",
    "author_fullname": "t2_da26nfrp",
    "secure_media": {
      "reddit_video": {
        "hls_url": "https://v.redd.it/ullduqhjqotf1/HLSPlaylist.m3u8?a=1762493081%2CNGI1MzU4ZTJiZWFlYzU3OWMwZDE0NzZkMWFlYmY5ODU3ODU3MDIyMjk4MTM2YWM2M2Y0N2EwY2NlNTAwNWVjZg%3D%3D&amp;v=1&amp;f=sd"
      }
    },
    "url": "https://v.redd.it/ullduqhjqotf1"
  },
  {
    "title": "He felt every note...",
    "author_fullname": "t2_1undnm7n5d",
    "secure_media": {
      "reddit_video": {
        "hls_url": "https://v.redd.it/ry9iic7hqqtf1/HLSPlaylist.m3u8?a=1762493081%2CZjAwOTRlZDk2NWJjZTMzZTI5YTRjZjJlYWFjZTU0NDZhZGEyZWE0MjkxMWZiZDA2YTQ3ZWRmZGRlYjVhZDI4Zg%3D%3D&amp;v=1&amp;f=sd"
      }
    },
    "url": "https://v.redd.it/ry9iic7hqqtf1"
  },
  {
    "title": "A lack of racism can actually be more hurtful than racism itself",
    "author_fullname": "t2_pf0g3",
    "secure_media": {
      "reddit_video": {
        "hls_url": "https://v.redd.it/qkq0y5h82otf1/HLSPlaylist.m3u8?a=1762493081%2CYzRiMGIxN2IyYWMzNTlmNDhiZTM4MWZjYjliODhiMmU0MjM2ZDgxZmE0NWNiNjQ5MjBmZDU2OGE4NjA3NDdlYQ%3D%3D&amp;v=1&amp;f=sd"
      }
    },
    "url": "https://v.redd.it/qkq0y5h82otf1"
  },
  {
    "title": "Flying Kick",
    "author_fullname": "t2_ceqkxycc",
    "secure_media": {
      "reddit_video": {
        "hls_url": "https://v.redd.it/xfyjn2bqrotf1/HLSPlaylist.m3u8?a=1762493081%2COTMyNzFjZWYzZjRjNzFkZjAwMmNmZTgwYzkzOTY1YzhkOGE1NjBhY2QxODRiYTU0MTFhM2QzZTgwOTFiYzhhYw%3D%3D&amp;v=1&amp;f=sd"
      }
    },
    "url": "https://v.redd.it/xfyjn2bqrotf1"
  },
  {
    "title": "Out of nowhere...",
    "author_fullname": "t2_ceqkxycc",
    "secure_media": {
      "reddit_video": {
        "hls_url": "https://v.redd.it/osnvl3y2rotf1/HLSPlaylist.m3u8?a=1762493081%2CYWM5ODA3OTQ3NDdhNjIwZTQwM2RjMmNjMTYzODcxNjliNjcxZDA0NjhiNmY3NjNjOTIyY2Y5MTIxNmY2ZjA0NQ%3D%3D&amp;v=1&amp;f=sd"
      }
    },
    "url": "https://v.redd.it/osnvl3y2rotf1"
  },
  {
    "title": "kid's logic",
    "author_fullname": "t2_9hw8f8o3",
    "secure_media": {
      "reddit_video": {
        "hls_url": "https://v.redd.it/ww3yft80eqtf1/HLSPlaylist.m3u8?a=1762493081%2CNjllMWNjODQ0NTRkYWZkZTc5NjQ0YzFkNTVjYzBjOGQ3OTE2ODNjYTIyNGFiZTY4YmY3NDczMmVjZDg5MGVjOQ%3D%3D&amp;v=1&amp;f=sd"
      }
    },
    "url": "https://v.redd.it/ww3yft80eqtf1"
  },
  {
    "title": "Her father had 8 kids and 3 wives but prefers pegging by men.",
    "author_fullname": "t2_5of0gi38",
    "secure_media": {
      "reddit_video": {
        "hls_url": "https://v.redd.it/52z11465qstf1/HLSPlaylist.m3u8?a=1762493081%2CNGQ4MTk1ZjM5YjBhZDI1Nzk5ZGFjYWUwYWVlYzg4Yzg2ZDIwMWM1ZDc4YTYzN2QzMTA3ZGE0YjgxYjViZDNlZA%3D%3D&amp;v=1&amp;f=sd"
      }
    },
    "url": "https://v.redd.it/52z11465qstf1"
  }
]

def test_your_format():
    print("🧪 Testing with your exact data format...")
    
    # Test the validation endpoint first
    try:
        response = requests.post(
            "http://localhost:8000/test-endpoint", 
            json=your_data,
            timeout=10
        )
        print(f"✅ Format validation: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"   📊 Video count: {result['video_count']}")
            for video in result['videos_received']:
                print(f"   📺 {video['index']}. {video['title']} (HLS: {video['has_hls_url']})")
        else:
            print(f"❌ Validation failed: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Validation request failed: {e}")
        return False
    
    print("\n" + "="*50)
    print("🎬 Testing actual video processing...")
    
    # Test actual processing (will fail due to FFmpeg but we'll see the error)
    try:
        response = requests.post(
            "http://localhost:8000/merge-videos",
            json=your_data,
            timeout=30
        )
        print(f"Video processing: {response.status_code}")
        if response.status_code != 200:
            print(f"Expected error (no FFmpeg): {response.text}")
        else:
            print("✅ Unexpected success!")
    except Exception as e:
        print(f"Processing request failed: {e}")
    
    return True

if __name__ == "__main__":
    test_your_format()
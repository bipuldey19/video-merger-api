#!/usr/bin/env python3
"""
Health check script for production monitoring
"""
import requests
import sys
import json
from datetime import datetime

def check_api_health(base_url="http://localhost:8000"):
    """Comprehensive health check for the Video Merger API"""
    
    print(f"🔍 Health Check - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    issues = []
    
    # Test 1: Basic health endpoint
    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        if response.status_code == 200:
            print("✅ Health endpoint: OK")
        else:
            issues.append(f"Health endpoint returned {response.status_code}")
            print(f"❌ Health endpoint: {response.status_code}")
    except Exception as e:
        issues.append(f"Health endpoint unreachable: {e}")
        print(f"❌ Health endpoint: {e}")
    
    # Test 2: API info endpoint
    try:
        response = requests.get(f"{base_url}/", timeout=10)
        if response.status_code == 200:
            info = response.json()
            print(f"✅ API info: v{info.get('version', 'unknown')}")
        else:
            issues.append(f"API info endpoint returned {response.status_code}")
            print(f"❌ API info: {response.status_code}")
    except Exception as e:
        issues.append(f"API info endpoint error: {e}")
        print(f"❌ API info: {e}")
    
    # Test 3: Format validation
    test_data = [{
        "title": "Health Check Test",
        "author_fullname": "test_user",
        "secure_media": {"reddit_video": {"hls_url": "https://test.m3u8"}},
        "url": "https://test.com"
    }]
    
    try:
        response = requests.post(
            f"{base_url}/test-endpoint",
            json=test_data,
            timeout=15
        )
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Format validation: {result['video_count']} videos processed")
        else:
            issues.append(f"Format validation failed: {response.status_code}")
            print(f"❌ Format validation: {response.status_code}")
    except Exception as e:
        issues.append(f"Format validation error: {e}")
        print(f"❌ Format validation: {e}")
    
    # Test 4: FFmpeg availability (through simulation)
    try:
        response = requests.post(
            f"{base_url}/test-merge-simulation",
            json=test_data,
            timeout=20
        )
        if response.status_code == 200:
            print("✅ Video processing simulation: OK")
        else:
            issues.append(f"Simulation failed: {response.status_code}")
            print(f"❌ Video processing simulation: {response.status_code}")
    except Exception as e:
        issues.append(f"Simulation error: {e}")
        print(f"❌ Video processing simulation: {e}")
    
    # Summary
    print("\n" + "=" * 50)
    if not issues:
        print("🎉 All health checks passed!")
        return 0
    else:
        print(f"⚠️ Found {len(issues)} issues:")
        for i, issue in enumerate(issues, 1):
            print(f"   {i}. {issue}")
        return 1

if __name__ == "__main__":
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"
    exit_code = check_api_health(base_url)
    sys.exit(exit_code)
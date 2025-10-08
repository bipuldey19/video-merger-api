#!/usr/bin/env python3
"""
FFmpeg installation script for Vercel deployment
"""
import os
import sys
import subprocess
import urllib.request
import tarfile
import zipfile
import shutil
from pathlib import Path

def install_ffmpeg():
    """Install FFmpeg binary for Vercel environment"""
    try:
        # Check if ffmpeg is already available
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        print("FFmpeg already available")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass
    
    # Create a directory for FFmpeg
    ffmpeg_dir = Path('/tmp/ffmpeg')
    ffmpeg_dir.mkdir(exist_ok=True)
    
    # Download pre-compiled FFmpeg binary
    ffmpeg_url = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-linux64-gpl.tar.xz"
    ffmpeg_archive = "/tmp/ffmpeg.tar.xz"
    
    try:
        print("Downloading FFmpeg...")
        urllib.request.urlretrieve(ffmpeg_url, ffmpeg_archive)
        
        print("Extracting FFmpeg...")
        with tarfile.open(ffmpeg_archive, 'r:xz') as tar:
            tar.extractall('/tmp/')
        
        # Find the extracted directory
        extracted_dirs = [d for d in Path('/tmp').glob('ffmpeg-master-*') if d.is_dir()]
        if not extracted_dirs:
            raise Exception("FFmpeg extraction failed")
        
        ffmpeg_extracted = extracted_dirs[0]
        ffmpeg_bin = ffmpeg_extracted / 'bin' / 'ffmpeg'
        
        if ffmpeg_bin.exists():
            # Copy to a standard location
            shutil.copy2(str(ffmpeg_bin), '/tmp/ffmpeg/ffmpeg')
            os.chmod('/tmp/ffmpeg/ffmpeg', 0o755)
            
            # Add to PATH
            os.environ['PATH'] = f"/tmp/ffmpeg:{os.environ.get('PATH', '')}"
            
            print("FFmpeg installed successfully")
            return True
        else:
            raise Exception("FFmpeg binary not found in extracted archive")
            
    except Exception as e:
        print(f"Failed to install FFmpeg: {e}")
        return False
    finally:
        # Cleanup
        if os.path.exists(ffmpeg_archive):
            os.remove(ffmpeg_archive)

if __name__ == "__main__":
    success = install_ffmpeg()
    sys.exit(0 if success else 1)
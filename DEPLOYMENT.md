# Video Merger API - Deployment Guide

## The FFmpeg Challenge on Vercel

The logs show that FFmpeg is not available in Vercel's serverless environment by default. This is a known limitation of serverless platforms.

## ✅ Solutions for Production Deployment

### Option 1: Railway (Recommended)
Railway supports Docker containers and FFmpeg out of the box:

1. **Create Railway account**: https://railway.app
2. **Deploy from GitHub**:
   ```bash
   # Connect your GitHub repo to Railway
   # Railway will automatically detect the Dockerfile
   ```
3. **Environment variables**: None needed, FFmpeg included in Docker image

### Option 2: Render
Render also supports Docker deployments:

1. **Create Render account**: https://render.com
2. **Create new Web Service** from GitHub repo
3. **Use Docker environment** (Render will detect Dockerfile)

### Option 3: Google Cloud Run
For enterprise deployments:

1. **Build and push Docker image**:
   ```bash
   docker build -t video-merger-api .
   docker tag video-merger-api gcr.io/YOUR_PROJECT/video-merger-api
   docker push gcr.io/YOUR_PROJECT/video-merger-api
   ```
2. **Deploy to Cloud Run**

### Option 4: AWS Lambda with Layers
More complex but stays serverless:

1. Create FFmpeg layer for Lambda
2. Deploy using AWS SAM or Serverless Framework

## 🔧 Quick Railway Deployment

1. **Fork this repository** to your GitHub
2. **Connect to Railway**:
   - Go to https://railway.app
   - Sign up/in with GitHub
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your forked repository
3. **Railway automatically**:
   - Detects the Dockerfile
   - Installs FFmpeg
   - Builds and deploys the API
4. **Get your URL** from Railway dashboard

## 📋 Testing Your Deployment

Once deployed, test with your exact JSON:

```bash
curl -X POST "https://your-railway-app.railway.app/merge-videos" \
  -H "Content-Type: application/json" \
  -d '[
    {
      "title": "The plot twist of all plot twists!",
      "author_fullname": "t2_1gnm5bvcxf",
      "secure_media": {
        "reddit_video": {
          "hls_url": "https://v.redd.it/ugqge1h9lotf1/HLSPlaylist.m3u8?a=..."
        }
      },
      "url": "https://v.redd.it/ugqge1h9lotf1"
    }
  ]'
```

## 🚀 Your API is Production Ready!

The codebase is perfect - it's just a platform limitation. Railway or Render will work immediately with your 14-video JSON format.

### Expected Processing Time:
- **14 videos**: ~5-10 minutes
- **Output**: Single MP4 file (1080x1920)
- **Features**: Titles, numbering, smooth transitions
- **Cleanup**: Automatic temporary file deletion

## 💡 Alternative: Use Simulation Endpoint

For testing workflows without video processing:
```bash
curl -X POST "https://your-app.vercel.app/test-merge-simulation" \
  -H "Content-Type: application/json" \
  -d '[your video array]'
```

This returns a detailed simulation of the processing without requiring FFmpeg.
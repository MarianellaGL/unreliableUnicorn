# UnreliableUnicorn Deployment Guide

## Deploy to Render.com (Free)

This guide will help you deploy your UnreliableUnicorn API to Render.com for free!

### Prerequisites

1. A GitHub account
2. A Render.com account (sign up at https://render.com)
3. Your TMDb API key

### Step 1: Push Your Code to GitHub

1. **Create a new repository on GitHub**
   - Go to https://github.com/new
   - Name it `unreliableunicorn` (or any name you prefer)
   - Make it **Public** (required for Render free tier)
   - Don't initialize with README (you already have files)

2. **Push your code** (run these commands in your project directory):

```bash
# Initialize git (if not already done)
git init

# Add all files (except those in .gitignore)
git add .

# Commit your changes
git commit -m "Initial commit - UnreliableUnicorn API ready for deployment"

# Add your GitHub repository as remote
git remote add origin https://github.com/YOUR_USERNAME/unreliableunicorn.git

# Push to GitHub
git push -u origin master
```

### Step 2: Deploy to Render

#### Option A: Using render.yaml (Automatic - Recommended)

1. **Go to Render Dashboard**
   - Visit https://dashboard.render.com

2. **Create New Blueprint**
   - Click "New" → "Blueprint"
   - Connect your GitHub repository
   - Render will automatically detect `render.yaml` and create:
     - PostgreSQL database (free)
     - Web service (free)

3. **Set Environment Variables**
   - In the Render dashboard, go to your web service
   - Click "Environment" in the left sidebar
   - Add your TMDb API key:
     - Key: `TMDB_URL`
     - Value: `your_tmdb_api_key_here`

4. **Deploy!**
   - Render will automatically deploy
   - Wait 5-10 minutes for first deployment
   - You'll get a URL like: `https://unreliableunicorn-api.onrender.com`

#### Option B: Manual Setup

1. **Create PostgreSQL Database**
   - Dashboard → "New" → "PostgreSQL"
   - Name: `unreliableunicorn-db`
   - Plan: Free
   - Create Database
   - Copy the "Internal Database URL"

2. **Create Web Service**
   - Dashboard → "New" → "Web Service"
   - Connect your GitHub repository
   - Configure:
     - Name: `unreliableunicorn-api`
     - Environment: `Docker`
     - Plan: `Free`
     - Dockerfile Path: `./dockerfile`

3. **Set Environment Variables**
   - `DATABASE_URL` = (Paste the Internal Database URL from step 1)
   - `TMDB_URL` = (Your TMDb API key)

4. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment (5-10 minutes)

### Step 3: Populate the Database

Once deployed, you need to populate your production database:

**Option 1: Run populate script via Render Shell**
1. Go to your web service in Render dashboard
2. Click "Shell" tab
3. Run:
```bash
python populate_db.py
```

**Option 2: SSH and populate**
```bash
# From Render dashboard, copy the shell command
render shell unreliableunicorn-api
python populate_db.py
```

### Step 4: Test Your Deployed API

Visit these URLs (replace with your actual Render URL):

```
https://unreliableunicorn-api.onrender.com/
https://unreliableunicorn-api.onrender.com/docs
https://unreliableunicorn-api.onrender.com/pelicula/random
https://unreliableunicorn-api.onrender.com/opiniones/top
```

### Important Notes

#### Free Tier Limitations
- **Sleeps after 15 minutes of inactivity**
  - First request after sleep takes ~30 seconds to wake up
  - Keep it awake with a cron job or uptime monitor (like UptimeRobot)

- **750 hours/month free**
  - More than enough if you're the only one using it

- **PostgreSQL database**: 1GB storage (plenty for this project)

#### Database Differences: MySQL vs PostgreSQL

Your app now supports both! The `DATABASE_URL` format:
- **PostgreSQL**: `postgresql://user:password@host:port/database`
- **MySQL**: `mysql+pymysql://user:password@host:port/database`

SQLAlchemy automatically detects and uses the correct dialect.

#### Keeping Your API Awake

The free tier sleeps after inactivity. To keep it awake:

**Option 1: UptimeRobot (Free)**
1. Sign up at https://uptimerobot.com
2. Add a new monitor:
   - Type: HTTP(s)
   - URL: `https://your-app.onrender.com/health/db`
   - Interval: 5 minutes

**Option 2: Cron-job.org (Free)**
1. Sign up at https://cron-job.org
2. Create a cron job that hits your endpoint every 10 minutes

### Troubleshooting

#### Deployment Fails
- Check the logs in Render dashboard
- Verify all environment variables are set
- Ensure your GitHub repo is public (required for free tier)

#### Database Connection Errors
- Verify `DATABASE_URL` is set correctly
- Check that database service is running
- Run migrations: `alembic upgrade head` in Render shell

#### 502 Bad Gateway
- Application is starting up (wait 30 seconds)
- Check logs for errors
- Verify port 8000 is exposed in Dockerfile

#### Empty Database
- Run `python populate_db.py` in Render shell
- Check TMDb API key is valid
- Verify database connection works

### Updating Your Deployment

After making changes to your code:

```bash
# Commit changes
git add .
git commit -m "Description of changes"

# Push to GitHub
git push

# Render will automatically redeploy!
```

### Alternative Free Hosting Options

If Render doesn't work for you:

1. **Railway.app**
   - Similar to Render
   - $5 free credit per month
   - https://railway.app

2. **Fly.io**
   - More complex setup
   - Better free tier allowances
   - https://fly.io

3. **Heroku** (No longer free)
   - Was the easiest option
   - Now requires paid plan

### Cost Estimation

**Render Free Tier:**
- Web Service: $0 (with sleep)
- PostgreSQL: $0 (1GB limit)
- **Total: $0/month** 🎉

**If you need 24/7 uptime:**
- Web Service: $7/month
- PostgreSQL: $7/month
- **Total: $14/month**

### Security Notes

- Never commit `.env` file (already in .gitignore)
- Set environment variables in Render dashboard
- Use strong database passwords
- Rotate API keys regularly

### Support

- Render Docs: https://render.com/docs
- Render Community: https://community.render.com
- FastAPI Docs: https://fastapi.tiangolo.com

---

## Success! 🦄

Once deployed, your UnreliableUnicorn API will be live and accessible from anywhere!

Share it:
```
🦄 Check out my UnreliableUnicorn API!
The Critic You Shouldn't Trust™

API: https://your-app.onrender.com
Docs: https://your-app.onrender.com/docs
```

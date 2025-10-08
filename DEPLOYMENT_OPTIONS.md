# 🚀 Deployment Options for Flight Delay Dashboard

## Important: Data File Issue
The flight data CSV is **1.3 GB** - too large for GitHub (100MB limit).

## Recommended Deployment Options

### ✅ Option 1: Render.com (RECOMMENDED for Dash Apps)
**Best for Python Dash applications**

1. Push code to GitHub (without the large CSV)
2. Upload CSV to Google Drive/Dropbox and get a public sharing link
3. Set environment variable `CSV_URL` on Render with the CSV URL
4. Deploy using the existing `Procfile`

**Steps:**
- Create account at [render.com](https://render.com)
- Create New Web Service
- Connect your GitHub repository
- Set environment variable: `CSV_URL` = your CSV public URL
- Deploy!

### ⚡ Option 2: Railway.app
**Fast and easy deployment**

Similar to Render, very developer-friendly:
- Connect GitHub repo
- Set `CSV_URL` environment variable
- Auto-deploys from GitHub

### 🌐 Option 3: Streamlit Cloud
**If you convert to Streamlit** (instead of Dash)
- Free tier available
- Direct GitHub integration
- Would require rewriting dashboard code

### ❌ Vercel - NOT Recommended
Vercel is optimized for:
- Static sites (React, Next.js, Vue)
- Serverless functions
- NOT for long-running Python Dash apps

## Current Setup

### Portfolio Site (index.html)
- Deploy on Vercel/Netlify/GitHub Pages
- Keep it separate from the dashboard

### Dashboard (Dash app)
- Deploy on Render/Railway
- Link to it from your portfolio

## Data Hosting Options

1. **Google Drive**: Upload CSV, make it publicly accessible
2. **Dropbox**: Similar to Google Drive
3. **GitHub Large File Storage (LFS)**: Costs money
4. **Use sample data**: Deploy with `flight_data_2024_sample.csv` instead

## Quick Deploy to Render

1. Upload CSV to Google Drive:
   - Right-click → Share → Anyone with link
   - Copy the sharing link
   - Convert to direct download link

2. Push to GitHub (I'll help with this next)

3. Go to Render:
   - New → Web Service
   - Connect GitHub repo
   - Environment Variables:
     - `CSV_URL`: Your CSV download URL
   - Deploy!

---

Ready to push to GitHub? I'll help you with the git commands next.


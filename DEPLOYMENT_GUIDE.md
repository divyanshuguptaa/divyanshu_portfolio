# 🚀 Complete Deployment Guide

Your code is now on GitHub! Here's how to deploy both your portfolio and dashboard.

## 📊 GitHub Repository
**URL:** https://github.com/divyanshuguptaa/divyanshu_portfolio

---

## 🌐 STEP 1: Deploy Portfolio Website (Vercel)

### Option A: Vercel (Recommended for Portfolio)

1. **Go to [vercel.com](https://vercel.com)**
2. **Sign up/Login** with your GitHub account
3. **Click "Add New Project"**
4. **Select your repository:** `divyanshuguptaa/divyanshu_portfolio`
5. **Configure:**
   - Framework Preset: **Other**
   - Root Directory: `./` (leave as default)
   - Build Command: Leave empty
   - Output Directory: Leave empty
6. **Click "Deploy"**
7. **Done!** Your portfolio will be live at: `https://divyanshu-portfolio-xxx.vercel.app`

### Option B: Netlify (Alternative)

1. Go to [netlify.com](https://netlify.com)
2. Click "Add new site" → "Import an existing project"
3. Connect GitHub and select your repository
4. Click Deploy!

---

## ✈️ STEP 2: Deploy Flight Dashboard (Render.com)

**Important:** The dashboard needs the large CSV file (1.3GB) which is NOT on GitHub.

### Option 1: Use Sample Data (Quick Test)
The dashboard will work with the sample data that's already in the repo!

1. **Go to [render.com](https://render.com)**
2. **Sign up/Login** with GitHub
3. **Click "New +" → "Web Service"**
4. **Connect your repository:** `divyanshuguptaa/divyanshu_portfolio`
5. **Configure:**
   - Name: `flight-delay-dashboard`
   - Region: Choose closest to you
   - Branch: `main`
   - Root Directory: Leave empty
   - Runtime: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn flight_delay_dashboard:server`
6. **Instance Type:** Free
7. **Click "Create Web Service"**
8. **Wait 5-10 minutes** for deployment

Your dashboard will be live at: `https://flight-delay-dashboard.onrender.com`

### Option 2: Use Full Dataset (1.3 GB)

#### A. Upload CSV to Google Drive
1. Upload `flight delay/flight_data_2024.csv` to Google Drive
2. Right-click → Share → "Anyone with the link"
3. Copy the sharing link (looks like): 
   ```
   https://drive.google.com/file/d/1ABC123.../view?usp=sharing
   ```
4. Convert to direct download link:
   ```
   https://drive.google.com/uc?export=download&id=1ABC123...
   ```
   (Replace `1ABC123...` with the ID from your link)

#### B. Set Environment Variable on Render
1. In your Render dashboard, go to your web service
2. Click **"Environment"** tab
3. Add variable:
   - Key: `CSV_URL`
   - Value: Your Google Drive direct download link
4. Click **"Save Changes"**
5. Render will automatically redeploy with full data!

#### Alternative: Use Dropbox
1. Upload CSV to Dropbox
2. Get sharing link
3. Change `?dl=0` to `?dl=1` at the end
4. Use this as your `CSV_URL`

---

## 🔗 STEP 3: Link Dashboard to Portfolio

Once both are deployed, update your portfolio `index.html` to link to your dashboard:

```html
<a href="https://your-dashboard.onrender.com" target="_blank">
  View Live Flight Dashboard
</a>
```

---

## 📱 Your Live URLs

After deployment, you'll have:

1. **Portfolio:** `https://your-name.vercel.app`
2. **Dashboard:** `https://flight-delay-dashboard.onrender.com`

---

## 🐛 Troubleshooting

### Render Dashboard Not Loading?
- Check logs in Render dashboard
- Ensure `Procfile` exists
- Verify `requirements.txt` has all dependencies

### Dashboard Shows Error?
- If using full CSV: Verify `CSV_URL` is set correctly
- Test the CSV URL in browser (should download file)
- Check Render logs for specific errors

### Free Tier Limitations
- **Render Free:** App sleeps after 15 min of inactivity (takes 30-60s to wake up)
- **Vercel Free:** Unlimited, but bandwidth limited
- **Upgrade:** If needed, both have affordable paid plans

---

## 🎯 Quick Summary

1. ✅ Code pushed to GitHub: `divyanshuguptaa/divyanshu_portfolio`
2. 🌐 Deploy portfolio on Vercel (5 minutes)
3. ✈️ Deploy dashboard on Render (10 minutes)
4. 🔗 Link them together
5. 🎉 Share your live portfolio!

---

## 💡 Pro Tips

- **Custom Domain:** Both Vercel and Render support custom domains for free
- **Analytics:** Add Google Analytics to track visitors
- **Resume:** Upload your resume to the repo and link it from portfolio
- **GitHub Pages:** Alternative free hosting for portfolio

---

Need help? Let me know! 🚀

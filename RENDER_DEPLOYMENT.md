# 🚀 Render.com Deployment Instructions

## Your GitHub Repository
**URL:** https://github.com/divyanshuguptaa/divyanshu_portfolio

## Your Full CSV on Google Drive
**File ID:** `1xGIJpdobrxBqweE9SRhgEb7CD0-RE9eF`
**Direct Download URL:** `https://drive.google.com/uc?export=download&id=1xGIJpdobrxBqweE9SRhgEb7CD0-RE9eF`

---

## 📋 Step-by-Step Deployment

### STEP 1: Initial Deployment (Sample Data)

1. Go to **[render.com](https://render.com)**
2. Sign in with **GitHub**
3. Click **"New +" → "Web Service"**
4. Select repository: **divyanshuguptaa/divyanshu_portfolio**
5. Configure:

| Setting | Value |
|---------|-------|
| Name | `flight-delay-dashboard` |
| Region | Oregon (US West) or closest to you |
| Branch | `main` |
| Root Directory | (leave empty) |
| Runtime | `Python 3` |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `gunicorn flight_delay_dashboard:server` |
| Instance Type | **Free** |

6. Click **"Create Web Service"**
7. Wait 5-10 minutes for deployment

**Status:** Dashboard will be live with 10,000 sample records

---

### STEP 2: Upgrade to Full Dataset (1.2 GB)

After initial deployment succeeds:

1. In Render dashboard, click your **flight-delay-dashboard** service
2. Click **"Environment"** tab (left sidebar)
3. Click **"Add Environment Variable"**
4. Add variable:
   - **Key:** `CSV_URL`
   - **Value:** `https://drive.google.com/uc?export=download&id=1xGIJpdobrxBqweE9SRhgEb7CD0-RE9eF`
5. Click **"Save Changes"**
6. Render will **auto-redeploy** (5-10 minutes)

**Status:** Dashboard now uses full 1.2 GB dataset! ✅

---

## 🔍 Verify It's Working

### Check Logs:
1. Go to your service in Render
2. Click **"Logs"** tab
3. Look for:
   ```
   Loading flight data...
   Loaded data from URL: https://drive.google.com/uc?...
   Data loaded successfully: [NUMBER] records
   ```

### Test Dashboard:
1. Open your dashboard URL: `https://flight-delay-dashboard.onrender.com`
2. Check if visualizations load
3. Verify data count in dashboard

---

## ⚠️ Important Notes

### Free Tier Limitations:
- App "sleeps" after 15 minutes of inactivity
- First request after sleep takes 30-60 seconds to wake up
- Full CSV download from Google Drive may take 1-2 minutes on first load
- This is normal for free tier!

### If Google Drive Blocks Downloads:
If you get errors about too many downloads:

**Option 1:** Make file publicly accessible:
1. In Google Drive, right-click file → Share
2. Change to "Anyone with the link can view"
3. Verify permissions

**Option 2:** Use Dropbox instead:
1. Upload CSV to Dropbox
2. Get sharing link
3. Change `?dl=0` to `?dl=1` at the end
4. Use that as `CSV_URL`

---

## 🎯 Expected Timeline

| Step | Time |
|------|------|
| Initial deployment (sample data) | 5-10 minutes |
| Add CSV_URL variable | 1 minute |
| Redeploy with full data | 5-10 minutes |
| **Total** | **~15 minutes** |

---

## 📱 Your Live URLs

After deployment:

- **Dashboard:** `https://flight-delay-dashboard.onrender.com`
- **GitHub Repo:** `https://github.com/divyanshuguptaa/divyanshu_portfolio`
- **CSV on Drive:** [Google Drive Link](https://drive.google.com/file/d/1xGIJpdobrxBqweE9SRhgEb7CD0-RE9eF/view?usp=drive_link)

---

## 🐛 Troubleshooting

### Dashboard not loading?
- Check Render logs for errors
- Verify `requirements.txt` exists
- Make sure `Procfile` is correct

### CSV not loading from Google Drive?
- Test direct download URL in browser
- Verify file is set to "Anyone with link can view"
- Check Render logs for download errors

### App keeps sleeping?
- Normal for free tier
- Consider upgrading to paid plan ($7/month) for always-on
- Or use Railway.app as alternative

---

## ✅ Success Checklist

- [ ] Render account created
- [ ] Repository connected
- [ ] Initial deployment successful (sample data)
- [ ] Dashboard accessible at URL
- [ ] CSV_URL environment variable added
- [ ] Redeployment successful (full data)
- [ ] Dashboard shows full dataset
- [ ] Link added to portfolio website

---

Need help? Check the logs or let me know! 🚀


# 🚂 Railway Deployment Guide

## ✅ Pre-Deployment Checklist

### Files Ready:
- ✅ `app.py` - Main bot code (cleaned & optimized)
- ✅ `requirements.txt` - Python dependencies
- ✅ `Procfile` - Railway start command
- ✅ `runtime.txt` - Python 3.11.9
- ✅ `railway.json` - Railway configuration
- ✅ `.gitignore` - Protects sensitive files

---

## 🔐 Step 1: Reset Your Bot Token (CRITICAL!)

Your old token was compromised. **You MUST reset it:**

1. Go to https://discord.com/developers/applications
2. Select your bot application
3. Click "Bot" in the left sidebar
4. Click **"Reset Token"** button
5. Confirm the reset
6. **Copy the new token immediately** (shown only once!)

---

## 🚀 Step 2: Deploy to Railway

### A. Create New Project
1. Go to https://railway.app
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Connect your GitHub account
5. Select this repository

### B. Set Environment Variables

In Railway Dashboard → Your Project → Variables tab:

#### **Required Variables:**

**1. DISCORD_TOKEN**
```
DISCORD_TOKEN=your_new_reset_token_here
```
⚠️ Use the NEW token you just reset, NOT the old one!

**2. GOOGLE_CREDENTIALS** (for Google Sheets)

Open your `credentials.json` file, copy the ENTIRE content, and paste it as one line:
```
GOOGLE_CREDENTIALS={"type":"service_account","project_id":"...entire JSON here..."}
```

**OR** alternatively, upload `credentials.json` to Railway and set:
```
GOOGLE_APPLICATION_CREDENTIALS=/app/credentials.json
```

---

## 📊 Step 3: Verify Deployment

### Check Logs
In Railway Dashboard → Your Service → Deployments → View Logs

Look for these success messages:
```
✅ Bot is online as [Your Bot Name]
🆔 Bot ID: [Bot ID]
📊 Connected to [N] guild(s)
🔄 Syncing slash commands...
✅ Synced [N] command(s)
🎯 Bot is ready to receive commands!
```

### If Google Sheets fails:
```
✅ Google Sheets client initialized from environment variable
```
or
```
✅ Google Sheets client initialized from credentials file
```

---

## 🎯 Step 4: Test Your Bot

### Test Commands in Discord:

1. **Team Balance:**
   ```
   /team_balance levels: 48,50,51,35,51,50,50,37,51,52
   ```

2. **Check-In:**
   ```
   /sunday-check-in level: 50
   /saturday-check-in level: 50
   ```

3. **Support (Admin only):**
   ```
   /support-ars command:add-role user:@someone role:@role
   ```

4. **Warzone (Commander/Judge only):**
   ```
   /warzone-cc-all round_type:R1-5vs5
   /warzone-winners ...
   ```

---

## 🔧 Troubleshooting

### Bot doesn't start:
- Check Railway logs for errors
- Verify `DISCORD_TOKEN` is set correctly (new token, not old one)
- Check Python version matches `runtime.txt` (3.11.9)

### Google Sheets not working:
- Verify `GOOGLE_CREDENTIALS` environment variable is set
- Make sure the JSON is properly formatted (no line breaks)
- Check Google Sheets API is enabled in Google Cloud Console
- Verify service account has access to the spreadsheet

### Commands not showing:
- Wait 5-10 minutes for Discord to sync
- Check bot has `applications.commands` scope
- Try `/` in Discord to see if commands appear

### Permission errors:
- Verify role IDs in `ROLE_IDS` dictionary are correct
- Check bot has proper Discord permissions
- Make sure bot role is high enough in role hierarchy

---

## 📝 Important Notes

1. **Never commit sensitive files:**
   - `.env` (blocked by .gitignore ✅)
   - `credentials.json` (blocked by .gitignore ✅)
   - Never share bot token publicly again!

2. **Update PROGRESSION_ROLES:**
   In `app.py`, replace placeholder IDs with actual role IDs:
   ```python
   PROGRESSION_ROLES = {
       "2.0": "actual_role_id_here",
       "3.0": "actual_role_id_here",
       "4.0": "actual_role_id_here",
       "5.0": "actual_role_id_here"
   }
   ```

3. **Railway will auto-deploy:**
   - Every time you push to GitHub
   - Deployment takes 2-5 minutes
   - Monitor logs during deployment

---

## 🎉 Your Bot Commands

### 1. Team Management:
- `/team_balance` - Balance two teams based on player levels

### 2. Warzone Tournament System:
- `/warzone-cc-all` - Assign players to warzone rooms
- `/warzone-winners` - Announce tournament winners

### 3. Support & Role Management:
- `/support-ars` - Add/Remove/Swap roles

### 4. Check-In Commands:
- `/sunday-check-in` - Sunday check-in for players
- `/saturday-check-in` - Saturday check-in for players

---

## 💡 Support

If you encounter issues:
1. Check Railway logs first
2. Verify all environment variables are set
3. Make sure bot token is the NEW reset one
4. Ensure Google Sheets credentials are correct

---

**Your bot is ready for Railway deployment! 🚀**


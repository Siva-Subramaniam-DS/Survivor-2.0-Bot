# ✅ Credentials Setup Checklist

## 1. Verify credentials.json exists
- [ ] File is in the same folder as app.py
- [ ] File is named exactly `credentials.json` (not credentials.json.txt)

## 2. Check credentials.json content
Open the file and verify it has:
```json
{
  "type": "service_account",
  "project_id": "your-project-name",
  "private_key_id": "...",
  "private_key": "-----BEGIN PRIVATE KEY-----\n...",
  "client_email": "your-service-account@your-project.iam.gserviceaccount.com",
  ...
}
```

## 3. ⚠️ CRITICAL: Share Google Sheet with Service Account

This is the MOST important step!

1. Open your credentials.json file
2. Find the `"client_email"` value (looks like: something@something.iam.gserviceaccount.com)
3. Copy that email address
4. Go to your Google Sheet:
   https://docs.google.com/spreadsheets/d/1PrULRObdldtnsCiPp1JAdGwzbgvj55mBalfLxfSTj3M/
5. Click "Share" button (top right)
6. Paste the service account email
7. Give it "Editor" permission
8. Uncheck "Notify people"
9. Click "Share"

**Without this step, your bot CANNOT access the sheet!**

## 4. Test Locally (Optional)

Before deploying to Railway, test locally:

1. Make sure you have your NEW bot token in .env file:
   ```
   DISCORD_TOKEN=your_new_reset_token
   ```

2. Run the bot locally:
   ```bash
   python app.py
   ```

3. Check for this message in console:
   ```
   ✅ Google Sheets client initialized from credentials file
   ```

## 5. For Railway Deployment

Choose ONE method:

### Method A: Environment Variable (Recommended)
1. Open credentials.json
2. Copy the ENTIRE content (all the JSON)
3. In Railway → Variables → Add:
   - Name: `GOOGLE_CREDENTIALS`
   - Value: Paste entire JSON

### Method B: Upload File
1. Include credentials.json in your git repo (NOT recommended for security)
2. Or use Railway's volume mount feature

## 6. Verify in Railway

After deployment, check Railway logs for:
```
✅ Google Sheets client initialized from environment variable
```
or
```
✅ Google Sheets client initialized from credentials file
```

---

## 🔍 Common Issues:

### "Google Sheets client not available"
- credentials.json is missing or incorrectly formatted
- credentials.json is not in the same folder as app.py

### "Permission denied" or "403 error"
- You forgot to share the sheet with the service account email
- Service account doesn't have "Editor" permission

### "Worksheet not found"
- Check the worksheet name in app.py matches exactly: "Give Sheet - H"
- Sheet names are case-sensitive!

---

**Once everything is checked, your bot is ready!** 🚀


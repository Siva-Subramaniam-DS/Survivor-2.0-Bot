# 🔧 Railway Command Sync Fix Guide

## Your Issue: Bot Online But Commands Not Showing

You mentioned: "Starting Container I guess it's not sync?"

This means your bot is running on Railway but Discord commands aren't appearing. Here's how to fix it:

---

## 🎯 Quick Fix (Most Likely Solution)

### Problem: Missing `applications.commands` Scope

Your bot was probably invited WITHOUT the `applications.commands` scope, which is required for slash commands.

### Solution: Re-invite Your Bot

1. **Go to Discord Developer Portal:**
   - https://discord.com/developers/applications
   - Select your bot application

2. **Generate New Invite URL:**
   - Go to "OAuth2" → "URL Generator"
   - Select BOTH scopes:
     - ✅ `bot`
     - ✅ `applications.commands` ← **THIS IS CRITICAL!**

3. **Select Permissions:**
   - ✅ Administrator (recommended)
   - OR select specific permissions your bot needs

4. **Copy the Generated URL** (should look like this):
   ```
   https://discord.com/api/oauth2/authorize?client_id=YOUR_BOT_ID&permissions=8&scope=bot%20applications.commands
   ```

5. **Use URL to Re-invite Bot:**
   - Open the URL in your browser
   - Select your Discord server
   - Authorize the bot

6. **Wait 5-10 Minutes:**
   - Discord takes time to sync commands
   - Restart your Discord client
   - Type `/` in a channel to see commands

---

## 🔍 How to Check Railway Logs

1. **Open Railway Dashboard:**
   - Go to https://railway.app
   - Select your project
   - Click on your service

2. **View Deployment Logs:**
   - Click "Deployments" tab
   - Click on the latest deployment
   - Click "View Logs"

3. **Look for These Messages:**

   **✅ Good Signs:**
   ```
   ✅ Bot is online as YourBotName
   📊 Connected to 1 guild(s)
   🔄 Syncing slash commands (attempt 1/3)...
   ✅ Successfully synced 10 command(s)
   📝 Synced commands:
      - /team_balance: Balance two teams based on player levels
      - /warzone-cc-all: Assign players to warzone rooms
      ... more commands ...
   🔍 Verified 10 commands are registered with Discord
   🎯 Bot is ready to receive commands!
   ```

   **❌ Bad Signs:**
   ```
   ❌ Bot doesn't have permission to sync commands
   ❌ HTTP error syncing commands: 403 Forbidden
   ⚠️ No commands were synced!
   🔍 Verified 0 commands are registered with Discord
   ```

4. **If You See Permission Errors:**
   - This confirms you need to re-invite the bot with `applications.commands` scope
   - Follow the "Quick Fix" section above

---

## 🧪 Test Command Sync Locally (Before Railway)

Run this diagnostic script to test if your bot can sync commands:

```bash
python railway_startup.py
```

This will:
- ✅ Check environment variables
- ✅ Test Discord connection
- ✅ Attempt command sync
- ✅ Show detailed error messages
- ✅ Verify commands are registered

---

## 🚀 Deploy Updated Code to Railway

Your `app.py` now has improved command syncing with:
- ✅ Retry logic (attempts 3 times)
- ✅ Better error handling
- ✅ Detailed logging
- ✅ Command verification
- ✅ Debug commands (`/sync-commands`, `/bot-status`)

To deploy:

### Option 1: Git Push (Recommended)
```bash
git add .
git commit -m "Fix command sync issues"
git push
```
Railway will auto-deploy in 2-5 minutes.

### Option 2: Railway CLI
```bash
railway up
```

---

## 🔧 Use Debug Commands (After Re-inviting Bot)

Once your bot is re-invited with proper permissions:

### 1. Check Bot Status
```
/bot-status
```
This shows:
- Bot permissions
- Number of registered commands
- What"s wrong if commands aren"t working

### 2. Manually Sync Commands
```
/sync-commands
```
This forces a command sync without redeploying.

**Note:** These debug commands require Administrator permissions in Discord.

---

## 📋 Complete Checklist

- [ ] Re-invite bot with `applications.commands` scope
- [ ] Wait 5-10 minutes after re-inviting
- [ ] Restart Discord client
- [ ] Check Railway logs for sync messages
- [ ] Try typing `/` in Discord to see commands
- [ ] Use `/bot-status` to verify (if commands appear)
- [ ] Use `/sync-commands` if needed (if commands appear)

---

## 🎯 Why This Happens

Discord requires the `applications.commands` scope for slash commands to work. Without it:
- ✅ Bot can connect and be "online"
- ✅ Bot can sync commands internally
- ❌ Discord won"t show commands to users
- ❌ Commands appear as "not registered"

The scope must be added during the OAuth2 authorization (bot invite).

---

## 💡 If Nothing Works

1. **Verify Bot Token is Correct:**
   - Check Railway environment variable `DISCORD_TOKEN`
   - Make sure it"s your current, valid token

2. **Check Discord API Status:**
   - https://discordstatus.com
   - Sometimes Discord has outages

3. **Check Bot Permissions in Discord:**
   - Server Settings → Roles
   - Find your bot"s role
   - Make sure it has proper permissions
   - Move bot role higher in hierarchy

4. **Try Global vs Guild Commands:**
   - Your bot uses global commands (work everywhere)
   - They take 1 hour to sync initially
   - Guild commands sync instantly but only work in one server

5. **Contact Support:**
   - Check Railway logs for specific errors
   - Share the error messages

---

## 🎉 Success Indicators

You"ll know it"s working when:

1. ✅ Railway logs show "Successfully synced X command(s)"
2. ✅ Type `/` in Discord and see your commands listed
3. ✅ `/bot-status` shows "Registered Commands: 10+"
4. ✅ You can execute commands like `/team_balance`

---

**Most Common Fix: Re-invite bot with `applications.commands` scope!**
#!/usr/bin/env python3
"""
Railway-specific startup script with enhanced command syncing
This helps diagnose and fix command sync issues on Railway
"""

import discord
from discord.ext import commands
import os
import asyncio
import sys

def check_environment():
    """Check if all required environment variables are set"""
    print("="*60)
    print("🔍 CHECKING ENVIRONMENT VARIABLES")
    print("="*60)
    
    token = os.environ.get("DISCORD_TOKEN")
    if not token:
        print("❌ DISCORD_TOKEN not found!")
        print("⚠️  Please set DISCORD_TOKEN in Railway environment variables")
        return False
    else:
        print(f"✅ DISCORD_TOKEN found (length: {len(token)} chars)")
    
    google_creds = os.environ.get("GOOGLE_CREDENTIALS")
    if google_creds:
        print(f"✅ GOOGLE_CREDENTIALS found (length: {len(google_creds)} chars)")
    else:
        print("⚠️  GOOGLE_CREDENTIALS not set (Google Sheets features will be disabled)")
    
    print("="*60)
    return True

async def test_bot_connection():
    """Test bot connection and command syncing"""
    print("\n" + "="*60)
    print("🤖 TESTING BOT CONNECTION")
    print("="*60)
    
    token = os.environ.get("DISCORD_TOKEN")
    if not token:
        print("❌ Cannot test - no token found")
        return False
    
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True
    intents.guilds = True
    
    bot = commands.Bot(command_prefix="!", intents=intents)
    tree = bot.tree
    
    # Add a simple test command
    @tree.command(name="railway-test", description="Test if commands are syncing on Railway")
    async def railway_test(interaction: discord.Interaction):
        await interaction.response.send_message("✅ Railway deployment is working! Commands are syncing properly.", ephemeral=True)
    
    @bot.event
    async def on_ready():
        print(f"✅ Bot connected as: {bot.user}")
        print(f"🆔 Bot ID: {bot.user.id}")
        print(f"📊 Connected to {len(bot.guilds)} guild(s)")
        
        if len(bot.guilds) == 0:
            print("❌ WARNING: Bot is not in any guilds!")
            print("🔧 Make sure you've invited the bot to your Discord server")
            await bot.close()
            return
        
        for guild in bot.guilds:
            print(f"\n📍 Guild: {guild.name} (ID: {guild.id})")
            
            # Check bot member and permissions
            bot_member = guild.get_member(bot.user.id)
            if bot_member:
                perms = bot_member.guild_permissions
                print(f"   🔐 Administrator: {perms.administrator}")
                print(f"   🔐 Manage Roles: {perms.manage_roles}")
                print(f"   🔐 Manage Channels: {perms.manage_channels}")
                
                if not perms.administrator and not perms.manage_roles:
                    print(f"   ⚠️  WARNING: Bot has limited permissions in {guild.name}")
        
        # Test command sync with detailed error handling
        print("\n" + "="*60)
        print("🔄 TESTING COMMAND SYNC")
        print("="*60)
        
        try:
            print("📤 Attempting to sync commands...")
            synced = await tree.sync()
            print(f"✅ Successfully synced {len(synced)} command(s)")
            
            if synced:
                print("\n📝 Synced commands:")
                for cmd in synced:
                    print(f"   ✓ /{cmd.name}")
            
            # Verify commands are registered
            print("\n🔍 Verifying command registration...")
            await asyncio.sleep(2)
            registered = await tree.fetch_commands()
            print(f"✅ Verified {len(registered)} command(s) registered with Discord")
            
            if len(registered) == 0:
                print("❌ WARNING: No commands registered!")
                print("🔧 Possible issues:")
                print("   1. Bot missing 'applications.commands' scope")
                print("   2. Rate limiting from Discord")
                print("   3. Bot permissions issue")
            else:
                print("\n🎉 SUCCESS! Commands are properly syncing on Railway!")
                print("💡 Your main bot (app.py) should work correctly now")
        
        except discord.Forbidden as e:
            print(f"❌ PERMISSION ERROR: {e}")
            print("🔧 Bot doesn't have permission to sync commands")
            print("💡 Make sure bot was invited with 'applications.commands' scope")
            print("📝 Re-invite URL should include: scope=bot%20applications.commands")
        
        except discord.HTTPException as e:
            print(f"❌ HTTP ERROR: {e}")
            if "rate limited" in str(e).lower():
                print("⏳ Rate limited by Discord - wait a few minutes and try again")
            else:
                print("🔧 Check your internet connection and Discord API status")
        
        except Exception as e:
            print(f"❌ UNEXPECTED ERROR: {e}")
            print(f"📋 Error type: {type(e).__name__}")
        
        print("\n" + "="*60)
        print("✅ Test complete - closing bot")
        print("="*60)
        await bot.close()
    
    try:
        print("🚀 Connecting to Discord...")
        await bot.start(token)
    except discord.LoginFailure:
        print("❌ INVALID TOKEN")
        print("🔧 Please check your DISCORD_TOKEN in Railway environment variables")
        return False
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False
    
    return True

async def main():
    """Main test function"""
    print("\n" + "="*60)
    print("🚂 RAILWAY DISCORD BOT DIAGNOSTICS")
    print("="*60)
    print("This script will test your bot configuration on Railway\n")
    
    # Step 1: Check environment
    if not check_environment():
        print("\n❌ Environment check failed")
        sys.exit(1)
    
    # Step 2: Test bot connection and sync
    print("\n⏳ Starting bot connection test...")
    await test_bot_connection()
    
    print("\n" + "="*60)
    print("📊 DIAGNOSTIC COMPLETE")
    print("="*60)
    print("\nIf you saw '🎉 SUCCESS' above, your bot is ready!")
    print("If you saw errors, follow the suggested fixes above.")
    print("\n💡 After fixing issues, deploy your main app.py to Railway")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Fatal error: {e}")
        sys.exit(1)
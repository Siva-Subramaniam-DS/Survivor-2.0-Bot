#!/usr/bin/env python3
"""
Test script to verify Discord bot commands are properly registered
Run this locally to test before deploying to Railway
"""

import discord
from discord import app_commands
from discord.ext import commands
import os
import asyncio
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Simple test bot setup
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree

@tree.command(name="test-ping", description="Test command to verify bot is working")
async def test_ping(interaction: discord.Interaction):
    """Simple test command"""
    await interaction.response.send_message("🏓 Pong! Bot is working and commands are synced!", ephemeral=True)

@bot.event
async def on_ready():
    print(f"✅ Test bot is online as {bot.user}")
    print(f"🆔 Bot ID: {bot.user.id}")
    print(f"📊 Connected to {len(bot.guilds)} guild(s)")
    
    # List guilds
    for guild in bot.guilds:
        print(f"   - {guild.name} (ID: {guild.id})")
        
        # Check bot permissions
        bot_member = guild.get_member(bot.user.id)
        if bot_member:
            perms = bot_member.guild_permissions
            print(f"     🔐 Administrator: {perms.administrator}")
            print(f"     🔐 Use Slash Commands: {perms.use_slash_commands}")
    
    # Test command sync
    try:
        print("🔄 Testing command sync...")
        synced = await tree.sync()
        print(f"✅ Synced {len(synced)} test command(s)")
        
        # Verify commands
        registered = await tree.fetch_commands()
        print(f"🔍 Verified {len(registered)} commands registered:")
        for cmd in registered:
            print(f"   - /{cmd.name}")
            
        if len(registered) > 0:
            print("🎉 SUCCESS: Commands are properly syncing!")
            print("💡 Your main bot should work on Railway now.")
        else:
            print("❌ ISSUE: No commands registered")
            print("🔧 Check bot permissions and invite URL")
            
    except Exception as e:
        print(f"❌ Command sync failed: {e}")
        print("🔧 This indicates a permission or configuration issue")
    
    print("\n" + "="*50)
    print("Test complete. Press Ctrl+C to stop the bot.")

if __name__ == "__main__":
    token = os.environ.get("DISCORD_TOKEN")
    
    if not token:
        print("❌ DISCORD_TOKEN not found in environment variables")
        print("Make sure your .env file contains: DISCORD_TOKEN=your_token_here")
        exit(1)
    
    try:
        print("🚀 Starting test bot...")
        bot.run(token, log_handler=None)
    except discord.LoginFailure:
        print("❌ Invalid Discord token")
    except Exception as e:
        print(f"❌ Error: {e}")
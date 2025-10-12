import discord
import discord
from discord import app_commands
from discord.ext import commands
import os
import random
from dotenv import load_dotenv
from itertools import combinations
import datetime
import asyncio
import io
import gspread
from google.oauth2.service_account import Credentials

# Load environment variables
load_dotenv()

# Google Sheets configuration
GOOGLE_SHEETS_CONFIG = {
    "spreadsheet_id": "1PrULRObdldtnsCiPp1JAdGwzbgvj55mBalfLxfSTj3M",
    "worksheet_name": "Give Sheet - H",
    "credentials_path": "credentials.json"
}

# Initialize Google Sheets client
def get_google_sheets_client():
    """Initialize and return Google Sheets client"""
    try:
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        
        # Try to load credentials from environment variable first (for Railway)
        google_creds_env = os.environ.get("GOOGLE_CREDENTIALS")
        if google_creds_env:
            import json
            creds_dict = json.loads(google_creds_env)
            creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
            client = gspread.authorize(creds)
            print("✅ Google Sheets client initialized from environment variable")
            return client
        
        # Fallback to credentials file
        if not os.path.exists(GOOGLE_SHEETS_CONFIG["credentials_path"]):
            print(f"❌ Google Sheets credentials file not found: {GOOGLE_SHEETS_CONFIG['credentials_path']}")
            print("💡 Set GOOGLE_CREDENTIALS environment variable with your credentials JSON")
            return None
        
        creds = Credentials.from_service_account_file(
            GOOGLE_SHEETS_CONFIG["credentials_path"], 
            scopes=scope
        )
        
        client = gspread.authorize(creds)
        print("✅ Google Sheets client initialized from credentials file")
        return client
    except Exception as e:
        print(f"❌ Error initializing Google Sheets client: {e}")
        return None

async def log_warzone_assignments_to_sheet(round_type: str, assignments: list, tournament_type: str = "Main"):
    """Log warzone assignments to Google Sheets"""
    try:
        client = get_google_sheets_client()
        if not client:
            print("❌ Google Sheets client not available")
            return False

        spreadsheet = client.open_by_key(GOOGLE_SHEETS_CONFIG["spreadsheet_id"])
        
        # Determine which worksheet to use based on round progression
        sheet_mapping = {
            "r1": "1.0",   # Round 1 winners go to 1.0 sheet
            "r2": "2.0",   # Round 2 winners go to 2.0 sheet  
            "r3": "3.0",   # Round 3 winners go to 3.0 sheet
            "r4": "4.0",   # Round 4 winners go to 4.0 sheet
            "r5": "5.0"    # Round 5 winners go to 5.0 sheet
        }
        
        target_worksheet = sheet_mapping.get(round_type, "1.0")
        
        try:
            worksheet = spreadsheet.worksheet(target_worksheet)
            print(f"✅ Using worksheet: {target_worksheet}")
        except gspread.WorksheetNotFound:
            worksheet = spreadsheet.get_worksheet(0)
            print(f"⚠️ Worksheet '{target_worksheet}' not found, using first available worksheet")
        
        rows_to_add = []
        
        for assignment in assignments:
            room_code = assignment["room_code"]
            players = assignment["players"]
            
            for player in players:
                discord_name = player.name
                discord_id = str(player.id)
                
                level_map = {
                    "r1": "R1-5vs5",
                    "r2": "R2-4vs4", 
                    "r3": "R3-3vs3",
                    "r4": "R4-2vs2",
                    "r5": "R5-1vs1"
                }
                ingame_level = level_map.get(round_type, f"Round-{round_type}")
                
                emoji_map = {
                    "r1": "⚔️",
                    "r2": "🛡️",
                    "r3": "⚡",
                    "r4": "🎯",
                    "r5": "👑"
                }
                emoji = emoji_map.get(round_type, "🏆")
                
                rows_to_add.append([
                    discord_id,
                    discord_name,
                    ingame_level,
                    emoji
                ])
        
        if rows_to_add:
            worksheet.append_rows(rows_to_add)
            print(f"✅ Logged {len(rows_to_add)} assignments to Google Sheets worksheet: {target_worksheet}")
            return True
        
        return False
            
    except Exception as e:
        print(f"❌ Error logging to Google Sheets: {e}")
        return False

# Channel IDs
CHANNEL_IDS = {
    "support_logs": 1246124687021314140
}

# Role IDs for permissions
ROLE_IDS = {
    "commander": 1172453428052631593,        # Can use warzone tournament commands and support
    "main_judge": 1051425023962919013,       # Can use winners command to post result and team balance
    "super_admin": 1125379786383044638,      # All access
    "admin": 1291348778200207431             # All access
}

# Tournament Role IDs
TOURNAMENT_ROLES = {
    "joined_main": "1194644728755519549",           # Replace with actual role ID
    "joined_parallel": "1194644860939022366",   # Replace with actual role ID
    "round1_main": "1195645662965010492",           # Replace with actual role ID
    "round1_parallel": "1195646439573946439"    # Replace with actual role ID
}

# Warzone Role and Channel Mappings
WARZONE_MAPPINGS = {
    # Warzone 1.x
    "1051103004461379674": {"role_name": "Warzone#1.1", "channel_id": "1234063969602371656", "channel_name": "war-zone-1"},
    "1051424554112798770": {"role_name": "Warzone#1.2", "channel_id": "1234059291686862869", "channel_name": "war-zone-2"},
    "1051424558365806622": {"role_name": "Warzone#1.3", "channel_id": "1234060314559905805", "channel_name": "war-zone-3"},
    "1051424560072884254": {"role_name": "Warzone#1.4", "channel_id": "1226447193817354291", "channel_name": "war-zone-4"},
    "1051424562342002701": {"role_name": "Warzone#1.5", "channel_id": "1234066500743073824", "channel_name": "war-zone-5"},
    "1061338706516131871": {"role_name": "Warzone#1.6", "channel_id": "1061493333018550272", "channel_name": "war-zone-6"},
    "1061338718948044943": {"role_name": "Warzone#1.7", "channel_id": "1234067842312175705", "channel_name": "war-zone-7"},
    "1061338724304175226": {"role_name": "Warzone#1.8", "channel_id": "1061493819159363664", "channel_name": "war-zone-8"},
    "1061338727407956009": {"role_name": "Warzone#1.9", "channel_id": "1234069097864626196", "channel_name": "war-zone-9"},
    "1061338733472907274": {"role_name": "Warzone#1.10", "channel_id": "1061494274568486943", "channel_name": "war-zone-10"},
    "1137659945769242645": {"role_name": "Warzone#1.11", "channel_id": "1147489946853199892", "channel_name": "war-zone-11"},
    "1137659985787093045": {"role_name": "Warzone#1.12", "channel_id": "1147490073814761483", "channel_name": "war-zone-12"},
    "1137659991457796207": {"role_name": "Warzone#1.13", "channel_id": "1147490100851253249", "channel_name": "war-zone-13"},
    "1137659995173945374": {"role_name": "Warzone#1.14", "channel_id": "1147490127849996369", "channel_name": "war-zone-14"},
    "1137659998911078431": {"role_name": "Warzone#1.15", "channel_id": "1147490152541868142", "channel_name": "war-zone-15"},
    "1137660006947360858": {"role_name": "Warzone#1.16", "channel_id": "1147490186071121943", "channel_name": "war-zone-16"},
    "1183715079007510558": {"role_name": "Warzone#1.17", "channel_id": "1183714809829654548", "channel_name": "war-zone-17"},
    "1183715140969975849": {"role_name": "Warzone#1.18", "channel_id": "1183714913546412042", "channel_name": "war-zone-18"},
    "1183715182149644289": {"role_name": "Warzone#1.19", "channel_id": "1183714937747546132", "channel_name": "war-zone-19"},
    "1183724483274612737": {"role_name": "Warzone#1.20", "channel_id": "1183714965522239498", "channel_name": "war-zone-20"},
    
    # Warzone 2.x
    "1055482548836388994": {"role_name": "Warzone#2.1", "channel_id": "1055482444528222279", "channel_name": "war-zone-2-1"},
    "1055482753237393458": {"role_name": "Warzone#2.2", "channel_id": "1055483638004854814", "channel_name": "war-zone-2-2"},
    "1055482763337285663": {"role_name": "Warzone#2.3", "channel_id": "1055484150829830164", "channel_name": "war-zone-2-3"},
    "1055482928097927198": {"role_name": "Warzone#2.4", "channel_id": "1055484370955284501", "channel_name": "war-zone-2-4"},
    "1055482933567311952": {"role_name": "Warzone#2.5", "channel_id": "1060850799917416519", "channel_name": "war-zone-2-5"},
    "1137681647257518180": {"role_name": "Warzone#2.6", "channel_id": "1137681372765499392", "channel_name": "war-zone-2-6"},
    "1183339990739070986": {"role_name": "Warzone#2.7", "channel_id": "1183751886537510963", "channel_name": "war-zone-2-7"},
    "1183752529650135040": {"role_name": "Warzone#2.8", "channel_id": "1183751930674167839", "channel_name": "war-zone-2-8"},
    "1183752614098243654": {"role_name": "Warzone#2.9", "channel_id": "1183751956511072256", "channel_name": "war-zone-2-9"},
    
    # Warzone 3.x
    "1058313518174179358": {"role_name": "Warzone#3.1", "channel_id": "1060891251672629268", "channel_name": "war-zone-3-1"},
    "1058313529041621012": {"role_name": "Warzone#3.2", "channel_id": "1066610535476498452", "channel_name": "war-zone-3-2"},
    "1058313540089413643": {"role_name": "Warzone#3.3", "channel_id": "1060891377153622056", "channel_name": "war-zone-3-3"},
    "1183753000574009415": {"role_name": "Warzone#3.4", "channel_id": "1183752054204792912", "channel_name": "war-zone-3-4"},
    "1183753078525153330": {"role_name": "Warzone#3.5", "channel_id": "1183752085779533924", "channel_name": "war-zone-3-5"},
    "1389932302720565268": {"role_name": "Warzone#3.6", "channel_id": "1389931457916702790", "channel_name": "war-zone-3-6"},
    "1389932996592926922": {"role_name": "Warzone#3.7", "channel_id": "1389931486857396224", "channel_name": "war-zone-3-7"},
    "1389933007569424394": {"role_name": "Warzone#3.8", "channel_id": "1389931514787139604", "channel_name": "war-zone-3-8"},
    "1389933008617865237": {"role_name": "Warzone#3.9", "channel_id": "1389931554100346932", "channel_name": "war-zone-3-9"},
    
    # Warzone 4.x
    "1061496973485682710": {"role_name": "Warzone#4.1", "channel_id": "1089462251263635476", "channel_name": "war-zone-4-1"},
    "1061497162812370994": {"role_name": "Warzone#4.2", "channel_id": "1173214822737916015", "channel_name": "war-zone-4-2"},
    "1183753888420073482": {"role_name": "Warzone#4.3", "channel_id": "1183754369292845107", "channel_name": "war-zone-4-3"},
    "1389933806953173095": {"role_name": "Warzone#4.4", "channel_id": "1389931580977446932", "channel_name": "war-zone-4-4"},
    "1389933811386814515": {"role_name": "Warzone#4.5", "channel_id": "1389931601999298690", "channel_name": "war-zone-4-5"},
    
    # Warzone 5.x
    "1055502005482823811": {"role_name": "Warzone#5.0", "channel_id": "1198241810062000298", "channel_name": "finalist"}
}

# Progression Role IDs for tournament advancement
PROGRESSION_ROLES = {
    "2.0": "PROGRESSION_ROLE_2_0_ID",  # Replace with actual role ID for 2.0
    "3.0": "PROGRESSION_ROLE_3_0_ID",  # Replace with actual role ID for 3.0
    "4.0": "PROGRESSION_ROLE_4_0_ID",  # Replace with actual role ID for 4.0
    "5.0": "PROGRESSION_ROLE_5_0_ID"   # Replace with actual role ID for 5.0
}

# Round progression mapping
ROUND_PROGRESSION = {
    "r1": {"players": 10, "room_prefix": "1.", "next_progression": "2.0"},
    "r2": {"players": 8, "room_prefix": "2.", "next_progression": "3.0"},
    "r3": {"players": 6, "room_prefix": "3.", "next_progression": "4.0"},
    "r4": {"players": 4, "room_prefix": "4.", "next_progression": "5.0"},
    "r5": {"players": 2, "room_prefix": "5.", "next_progression": None}
}

# Set Windows event loop policy for asyncio
import sys
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True
intents.guild_messages = True

bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree

# Permission checking functions
def has_event_create_permission(interaction):
    """Check if user has permission to create events (Commander, Super Admin, or Admin)"""
    commander_role = discord.utils.get(interaction.user.roles, id=ROLE_IDS["commander"])
    super_admin_role = discord.utils.get(interaction.user.roles, id=ROLE_IDS["super_admin"])
    admin_role = discord.utils.get(interaction.user.roles, id=ROLE_IDS["admin"])
    return (commander_role is not None or super_admin_role is not None or admin_role is not None)

def has_event_result_permission(interaction):
    """Check if user has permission to post event results (Commander, Main Judge, Super Admin, or Admin)"""
    commander_role = discord.utils.get(interaction.user.roles, id=ROLE_IDS["commander"])
    main_judge_role = discord.utils.get(interaction.user.roles, id=ROLE_IDS["main_judge"])
    super_admin_role = discord.utils.get(interaction.user.roles, id=ROLE_IDS["super_admin"])
    admin_role = discord.utils.get(interaction.user.roles, id=ROLE_IDS["admin"])
    return (commander_role is not None or main_judge_role is not None or super_admin_role is not None or admin_role is not None)

def has_team_balance_permission(interaction):
    """Check if user has permission to use team balance (Main Judge, Super Admin, or Admin)"""
    main_judge_role = discord.utils.get(interaction.user.roles, id=ROLE_IDS["main_judge"])
    super_admin_role = discord.utils.get(interaction.user.roles, id=ROLE_IDS["super_admin"])
    admin_role = discord.utils.get(interaction.user.roles, id=ROLE_IDS["admin"])
    return (main_judge_role is not None or super_admin_role is not None or admin_role is not None)

@bot.event
async def on_ready():
    print(f"✅ Bot is online as {bot.user}")
    print(f"🆔 Bot ID: {bot.user.id}")
    print(f"📊 Connected to {len(bot.guilds)} guild(s)")
    
    # Sync commands with timeout handling
    try:
        print("🔄 Syncing slash commands...")
        synced = await asyncio.wait_for(tree.sync(), timeout=30.0)
        print(f"✅ Synced {len(synced)} command(s)")
    except asyncio.TimeoutError:
        print("⚠️ Command sync timed out, but bot will continue running")
    except Exception as e:
        print(f"❌ Error syncing commands: {e}")
        print("⚠️ Bot will continue running without command sync")
    
    print("🎯 Bot is ready to receive commands!")

# ===========================================================================================
# TEAM MANAGEMENT COMMAND
# ===========================================================================================

@tree.command(name="team_balance", description="Balance two teams based on player levels")
@app_commands.describe(levels="Comma-separated player levels (e.g. 48,50,51,35,51,50,50,37,51,52)")
async def team_balance(interaction: discord.Interaction, levels: str):
    # Check permissions
    if not has_team_balance_permission(interaction):
        await interaction.response.send_message("❌ You need **Main Judge**, **Super Admin**, or **Admin** role to use this command.", ephemeral=True)
        return
    
    try:
        level_list = [int(x.strip()) for x in levels.split(",") if x.strip()]
        n = len(level_list)
        if n % 2 != 0:
            await interaction.response.send_message("❌ Number of players must be even (e.g., 8 or 10).", ephemeral=True)
            return

        team_size = n // 2
        min_diff = float('inf')
        best_team_a = []
        for combo in combinations(level_list, team_size):
            team_a = list(combo)
            team_b = list(level_list)
            for lvl in team_a:
                team_b.remove(lvl)
            diff = abs(sum(team_a) - sum(team_b))
            if diff < min_diff:
                min_diff = diff
                best_team_a = team_a
        team_b = list(level_list)
        for lvl in best_team_a:
            team_b.remove(lvl)
        sum_a = sum(best_team_a)
        sum_b = sum(team_b)
        diff = abs(sum_a - sum_b)
        await interaction.response.send_message(
            f"**Team A:** {best_team_a} | Total Level: {sum_a}\n"
            f"**Team B:** {team_b} | Total Level: {sum_b}\n"
            f"**Level Difference:** {diff}",
            ephemeral=True
        )
    except Exception as e:
        await interaction.response.send_message(f"❌ Error: {e}", ephemeral=True)

# ===========================================================================================
# WARZONE TOURNAMENT SYSTEM COMMANDS
# ===========================================================================================

@tree.command(name="warzone-cc-all", description="Assign players to warzone rooms based on round structure")
@app_commands.describe(
    round_type="Round type to assign players to",
    warzone="Specific warzone room to assign to (optional)"
)
@app_commands.choices(
    round_type=[
        app_commands.Choice(name="R1-5vs5 (10 people)", value="r1"),
        app_commands.Choice(name="R2-4vs4 (8 people)", value="r2"),
        app_commands.Choice(name="R3-3vs3 (6 people)", value="r3"),
        app_commands.Choice(name="R4-2vs2 (4 people)", value="r4"),
        app_commands.Choice(name="R5-1vs1 (2 people)", value="r5")
    ],
    warzone=[
        app_commands.Choice(name="Warzone#1.1", value="1.1"),
        app_commands.Choice(name="Warzone#1.2", value="1.2"),
        app_commands.Choice(name="Warzone#1.3", value="1.3"),
        app_commands.Choice(name="Warzone#1.4", value="1.4"),
        app_commands.Choice(name="Warzone#1.5", value="1.5"),
        app_commands.Choice(name="Warzone#1.6", value="1.6"),
        app_commands.Choice(name="Warzone#1.7", value="1.7"),
        app_commands.Choice(name="Warzone#1.8", value="1.8"),
        app_commands.Choice(name="Warzone#1.9", value="1.9"),
        app_commands.Choice(name="Warzone#1.10", value="1.10"),
        app_commands.Choice(name="Warzone#1.11", value="1.11"),
        app_commands.Choice(name="Warzone#1.12", value="1.12"),
        app_commands.Choice(name="Warzone#1.13", value="1.13"),
        app_commands.Choice(name="Warzone#1.14", value="1.14"),
        app_commands.Choice(name="Warzone#1.15", value="1.15"),
        app_commands.Choice(name="Warzone#1.16", value="1.16"),
        app_commands.Choice(name="Warzone#1.17", value="1.17"),
        app_commands.Choice(name="Warzone#1.18", value="1.18"),
        app_commands.Choice(name="Warzone#1.19", value="1.19"),
        app_commands.Choice(name="Warzone#1.20", value="1.20"),
        app_commands.Choice(name="Warzone#2.1", value="2.1"),
        app_commands.Choice(name="Warzone#2.2", value="2.2"),
        app_commands.Choice(name="Warzone#2.3", value="2.3"),
        app_commands.Choice(name="Warzone#2.4", value="2.4"),
        app_commands.Choice(name="Warzone#2.5", value="2.5"),
        app_commands.Choice(name="Warzone#2.6", value="2.6"),
        app_commands.Choice(name="Warzone#2.7", value="2.7"),
        app_commands.Choice(name="Warzone#2.8", value="2.8"),
        app_commands.Choice(name="Warzone#2.9", value="2.9"),
        app_commands.Choice(name="Warzone#3.1", value="3.1"),
        app_commands.Choice(name="Warzone#3.2", value="3.2"),
        app_commands.Choice(name="Warzone#3.3", value="3.3"),
        app_commands.Choice(name="Warzone#3.4", value="3.4"),
        app_commands.Choice(name="Warzone#3.5", value="3.5"),
        app_commands.Choice(name="Warzone#3.6", value="3.6"),
        app_commands.Choice(name="Warzone#3.7", value="3.7"),
        app_commands.Choice(name="Warzone#3.8", value="3.8"),
        app_commands.Choice(name="Warzone#3.9", value="3.9"),
        app_commands.Choice(name="Warzone#4.1", value="4.1"),
        app_commands.Choice(name="Warzone#4.2", value="4.2"),
        app_commands.Choice(name="Warzone#4.3", value="4.3"),
        app_commands.Choice(name="Warzone#4.4", value="4.4"),
        app_commands.Choice(name="Warzone#4.5", value="4.5"),
        app_commands.Choice(name="Warzone#5.0 (Finalist)", value="5.0")
    ]
)
async def warzone_cc_all(
    interaction: discord.Interaction,
    round_type: app_commands.Choice[str],
    warzone: app_commands.Choice[str] = None
):
    """Assign players to warzone rooms based on round structure"""
    
    await interaction.response.defer(ephemeral=True)
    
    # Check permissions
    if not has_event_result_permission(interaction):
        await interaction.followup.send("❌ You need **Commander**, **Main Judge**, **Super Admin**, or **Admin** role to use this command.", ephemeral=True)
        return
    
    # Get members based on round type
    warzone_members = []
    
    if round_type.value == "r1":
        # For R1, get all members with Round1 roles (from check-in)
        round1_main_id = TOURNAMENT_ROLES.get("round1_main")
        round1_parallel_id = TOURNAMENT_ROLES.get("round1_parallel")
        
        if round1_main_id.startswith("ROUND1_") or round1_parallel_id.startswith("ROUND1_"):
            await interaction.followup.send("❌ Round1 role IDs not configured. Please update TOURNAMENT_ROLES in the code.", ephemeral=True)
            return
        
        # Get Round1 role objects
        round1_main_role = discord.utils.get(interaction.guild.roles, id=int(round1_main_id))
        round1_parallel_role = discord.utils.get(interaction.guild.roles, id=int(round1_parallel_id))
        
        if round1_main_role:
            warzone_members.extend(round1_main_role.members)
        if round1_parallel_role:
            warzone_members.extend(round1_parallel_role.members)
    else:
        # For R2+, get members with the appropriate progression role (2.0, 3.0, 4.0, 5.0)
        progression_role_id = PROGRESSION_ROLES.get(ROUND_PROGRESSION[round_type.value]["next_progression"])
        if progression_role_id and not progression_role_id.startswith("PROGRESSION_ROLE_"):
            progression_role = discord.utils.get(interaction.guild.roles, id=int(progression_role_id))
            if progression_role:
                warzone_members = list(progression_role.members)
            else:
                await interaction.followup.send(f"❌ Progression role for {ROUND_PROGRESSION[round_type.value]['next_progression']} not found.", ephemeral=True)
                return
        else:
            await interaction.followup.send(f"❌ Progression role for {ROUND_PROGRESSION[round_type.value]['next_progression']} not configured.", ephemeral=True)
            return
    
    # Remove duplicates
    warzone_members = list(set(warzone_members))
    
    if not warzone_members:
        if round_type.value == "r1":
            await interaction.followup.send("❌ No members found with warzone roles.", ephemeral=True)
        else:
            await interaction.followup.send(f"❌ No members found with progression role for {ROUND_PROGRESSION[round_type.value]['next_progression']}.", ephemeral=True)
        return

    # Get round configuration
    config = ROUND_PROGRESSION[round_type.value]
    config["name"] = {
        "r1": "R1-5vs5",
        "r2": "R2-4vs4", 
        "r3": "R3-3vs3",
        "r4": "R4-2vs2",
        "r5": "R5-1vs1"
    }[round_type.value]
    
    # Filter members for specific warzone if provided
    if warzone:
        target_role_id = None
        for role_id, mapping in WARZONE_MAPPINGS.items():
            if mapping["role_name"].replace("Warzone#", "") == warzone.value:
                target_role_id = role_id
                break
        
        if target_role_id:
            target_role = discord.utils.get(interaction.guild.roles, id=int(target_role_id))
            if target_role:
                warzone_members = [member for member in warzone_members if target_role in member.roles]
    
    # Calculate rooms needed
    total_players = len(warzone_members)
    players_per_room = config["players"]
    rooms_needed = (total_players + players_per_room - 1) // players_per_room
    
    if total_players == 0:
        await interaction.followup.send("❌ No eligible players found for assignment.", ephemeral=True)
        return
            
    # Get available rooms
    available_rooms = []
    for role_id, mapping in WARZONE_MAPPINGS.items():
        room_code = mapping["role_name"].replace("Warzone#", "")
        if room_code.startswith(config["room_prefix"]):
            available_rooms.append({
                "role_id": role_id,
                "role_name": mapping["role_name"],
                "channel_id": mapping["channel_id"],
                "channel_name": mapping["channel_name"],
                "room_code": room_code
            })
    
    if len(available_rooms) < rooms_needed:
        await interaction.followup.send(f"❌ Not enough available rooms for {config['name']}. Need {rooms_needed} rooms but only {len(available_rooms)} available.", ephemeral=True)
        return

    # Shuffle players for fair distribution
    random.shuffle(warzone_members)
    
    # Create assignment embed
    embed = discord.Embed(
        title=f"🏆 {config['name']} - Room Assignments",
        description=f"**Total Players:** {total_players}\n**Players per Room:** {players_per_room}\n**Rooms Created:** {rooms_needed}",
        color=discord.Color.blue(),
        timestamp=discord.utils.utcnow()
    )
    
    # Assign players to rooms
    assignment_results = []
    assignment_data = []
    
    for i in range(rooms_needed):
        room = available_rooms[i]
        start_idx = i * players_per_room
        end_idx = min(start_idx + players_per_room, total_players)
        room_players = warzone_members[start_idx:end_idx]
        
        # Get the role and channel objects
        role = discord.utils.get(interaction.guild.roles, id=int(room["role_id"]))
        channel = interaction.guild.get_channel(int(room["channel_id"]))
        
        if role and channel:
            # Add players to the role
            added_count = 0
            for player in room_players:
                try:
                    if role not in player.roles:
                        await player.add_roles(role)
                        added_count += 1
                except discord.Forbidden:
                    print(f"Error: Bot doesn't have permission to assign role {role.name} to {player.display_name}")
                except Exception as e:
                    print(f"Error assigning role to {player.display_name}: {e}")
            
            # Set channel permissions for the role
            try:
                await channel.set_permissions(
                    role,
                    read_messages=True,
                    send_messages=True,
                    view_channel=True,
                    embed_links=True,
                    attach_files=True,
                    read_message_history=True
                )
            except Exception as e:
                print(f"Error setting channel permissions for {room['channel_name']}: {e}")
            
            # Create room assignment info
            player_list = "\n".join([f"• {player.display_name}" for player in room_players])
            assignment_results.append(f"**{room['role_name']}** ({room['channel_name']})\n{player_list}\n**Assigned:** {added_count}/{len(room_players)}")
            
            # Store assignment data for Google Sheets
            assignment_data.append({
                "room_code": room["room_code"],
                "role_name": room["role_name"],
                "channel_name": room["channel_name"],
                "players": room_players
            })
    
    # Add room assignments to embed
    for i, result in enumerate(assignment_results):
        embed.add_field(
            name=f"Room {i+1}",
            value=result,
            inline=False
        )
    
    # Add staff acknowledgment
    embed.add_field(
        name="👨‍⚖️ Staff",
        value=f"**Assigned by:** {interaction.user.mention}",
        inline=False
    )
    
    embed.set_footer(text="Warzone Room Assignment • 😈The Devil's Spot😈")
    
    # Send the assignment results
    await interaction.channel.send(embed=embed)
    
    # Log assignments to Google Sheets
    sheets_success = False
    if assignment_data:
        sheets_success = await log_warzone_assignments_to_sheet(round_type.value, assignment_data)
    
    # Send confirmation to user
    confirmation_text = f"✅ **{config['name']}** room assignments completed!\n"
    confirmation_text += f"• **{total_players} players** assigned to **{rooms_needed} rooms**\n"
    confirmation_text += f"• Each room contains **{players_per_room} players**\n"
    confirmation_text += f"• Players have been given access to their assigned channels\n"
    
    if sheets_success:
        confirmation_text += f"• 📊 **Assignments logged to Google Sheets**"
    else:
        confirmation_text += f"• ⚠️ **Google Sheets logging failed** (check credentials/config)"
    
    await interaction.followup.send(confirmation_text, ephemeral=True)

@tree.command(name="warzone-winners", description="Announce warzone tournament winners")
@app_commands.describe(
    close_role="Role ID to close channel access for",
    win_role="Win role number (2.0, 3.0, 4.0, 5.0)",
    win_no="Number of winners",
    tour_type="Tournament type",
    judge="Judge who handled the match",
    user_1="Winner 1",
    user_2="Winner 2 (optional)",
    user_3="Winner 3 (optional)",
    user_4="Winner 4 (optional)",
    user_5="Winner 5 (optional)",
    screenshot="Result screenshot (upload)"
)
@app_commands.choices(
    win_role=[
        app_commands.Choice(name="2.0", value="2.0"),
        app_commands.Choice(name="3.0", value="3.0"),
        app_commands.Choice(name="4.0", value="4.0"),
        app_commands.Choice(name="5.0", value="5.0")
    ],
    tour_type=[
        app_commands.Choice(name="Main-Tour", value="Main-Tour"),
        app_commands.Choice(name="Parallel-Tour", value="Parallel-Tour")
    ]
)
async def warzone_winners(
    interaction: discord.Interaction,
    close_role: discord.Role,
    win_role: app_commands.Choice[str],
    win_no: int,
    tour_type: app_commands.Choice[str],
    judge: discord.Member,
    user_1: discord.Member,
    user_2: discord.Member = None,
    user_3: discord.Member = None,
    user_4: discord.Member = None,
    user_5: discord.Member = None,
    screenshot: discord.Attachment = None
):
    """Announce warzone tournament winners and manage roles/channels"""
    
    await interaction.response.defer(ephemeral=True)
    
    # Check permissions
    if not has_event_result_permission(interaction):
        await interaction.followup.send("❌ You need **Commander**, **Main Judge**, **Super Admin**, or **Admin** role to announce warzone winners.", ephemeral=True)
        return

    # Validate win_no matches number of provided users
    provided_users = [user for user in [user_1, user_2, user_3, user_4, user_5] if user is not None]
    if len(provided_users) != win_no:
        await interaction.followup.send(f"❌ Number of winners ({win_no}) must match the number of users provided ({len(provided_users)}).", ephemeral=True)
        return

    # Get the progression role for winners
    progression_role_id = PROGRESSION_ROLES.get(win_role.value)
    if not progression_role_id or progression_role_id.startswith("PROGRESSION_ROLE_"):
        await interaction.followup.send(f"❌ Progression role for {win_role.value} not configured. Please update PROGRESSION_ROLES in the code.", ephemeral=True)
        return
    
    target_win_role = discord.utils.get(interaction.guild.roles, id=int(progression_role_id))
    
    if not target_win_role:
        await interaction.followup.send(f"❌ Progression role for {win_role.value} not found. Please check the role ID configuration.", ephemeral=True)
        return

    try:
        # Close channel access for close_role members
        await interaction.channel.set_permissions(
            close_role,
            read_messages=False,
            send_messages=False,
            view_channel=False
        )
        
        # Create winner announcement embed
        embed = discord.Embed(
            title="🏆 Winner of the Current Round!!",
            description=f"**{tour_type.value}** - Progression to Round {win_role.value}",
            color=discord.Color.gold(),
            timestamp=discord.utils.utcnow()
        )
        
        # Add winners section
        winners_text = "**Winner of the Current Round!! Given to**\n"
        for i, user in enumerate(provided_users, 1):
            winners_text += f"• {user.mention}\n"
        
        embed.add_field(name="", value=winners_text, inline=False)
        
        # Add channel status
        embed.add_field(
            name="📢 Progression Status",
            value=f"❌ **Closed Channel** for Role `{close_role.mention}`\n✅ **Progression Role Assigned** `{target_win_role.mention}`\n🎯 **Ready for Next Round** - Use `/warzone-cc-all` to assign rooms",
            inline=False
        )
        
        # Add staff acknowledgment
        staff_text = f"**Thanks to** {judge.mention} **Judge**\n"
        staff_text += f"**Posted By** {interaction.user.mention}"
        embed.add_field(name="👨‍⚖️ Staff", value=staff_text, inline=False)
        
        embed.set_footer(text="Powered By Metal Wings")
        
        # Handle screenshot attachment
        file_to_send = None
        if screenshot:
            try:
                file_data = await screenshot.read()
                file_to_send = discord.File(
                    fp=io.BytesIO(file_data),
                    filename=f"warzone_result_{screenshot.filename}"
                )
                embed.add_field(name="📷 Screenshot", value="Result screenshot attached", inline=False)
            except Exception as e:
                print(f"Error processing screenshot: {e}")
        
        # Send the announcement
        if file_to_send:
            await interaction.channel.send(embed=embed, file=file_to_send)
        else:
            await interaction.channel.send(embed=embed)
        
        # Assign win roles to winners
        assigned_count = 0
        for user in provided_users:
            try:
                if target_win_role not in user.roles:
                    await user.add_roles(target_win_role)
                    assigned_count += 1
            except discord.Forbidden:
                print(f"Error: Bot doesn't have permission to assign role {target_win_role.name} to {user.display_name}")
            except Exception as e:
                print(f"Error assigning role to {user.display_name}: {e}")
        
        # Send confirmation to user
        confirmation_text = f"✅ Tournament progression completed!\n"
        confirmation_text += f"• **{win_no} winners** advanced to Round {win_role.value}\n"
        confirmation_text += f"• **Channel closed** for {close_role.mention}\n"
        confirmation_text += f"• **Progression role assigned** to {assigned_count}/{win_no} users\n"
        confirmation_text += f"• **Tournament type:** {tour_type.value}\n"
        confirmation_text += f"• **Next round role:** {target_win_role.mention}\n"
        confirmation_text += f"• 🎯 **Ready for next round** - Use `/warzone-cc-all` to assign rooms"
        
        await interaction.followup.send(confirmation_text, ephemeral=True)
        
    except discord.Forbidden:
        await interaction.followup.send("❌ Bot doesn't have permission to manage roles or channel permissions.", ephemeral=True)
    except Exception as e:
        await interaction.followup.send(f"❌ An error occurred: {str(e)}", ephemeral=True)
        print(f"Error in warzone_winners command: {e}")

# ===========================================================================================
# SUPPORT & ROLE MANAGEMENT COMMAND
# ===========================================================================================

async def log_to_support_channel(commander: discord.Member, details: str, target_member: discord.Member = None):
    """Log support actions to the support-logs channel"""
    try:
        support_channel = bot.get_channel(CHANNEL_IDS["support_logs"])
        if not support_channel:
            print("❌ Support logs channel not found")
            return
        
        # Create log message with template format
        log_message = f"<@873061751413940295>:<@{commander.id}> {details}"
        
        if target_member:
            log_message += f" to <@{target_member.id}>"
        
        # Send to support logs channel
        await support_channel.send(log_message)
        print(f"✅ Logged to support channel: {details}")
        
    except Exception as e:
        print(f"❌ Error logging to support channel: {e}")

@tree.command(name="support-ars", description="Support Add/Remove/Swap roles")
@app_commands.describe(
    command="Action to perform",
    user="Target user",
    role="Role to add/remove/swap"
)
@app_commands.choices(
    command=[
        app_commands.Choice(name="add-role", value="add"),
        app_commands.Choice(name="remove-role", value="remove"),
        app_commands.Choice(name="swap-role", value="swap")
    ]
)
async def support_ars(
    interaction: discord.Interaction,
    command: app_commands.Choice[str],
    user: discord.Member,
    role: discord.Role
):
    """Support command for adding, removing, or swapping roles"""
    
    await interaction.response.defer(ephemeral=True)
    
    # Check permissions
    if not has_event_create_permission(interaction):
        await interaction.followup.send("❌ You need **Commander**, **Super Admin**, or **Admin** role to use this command.", ephemeral=True)
        return
    
    try:
        if command.value == "add":
            # Add role to user
            if role not in user.roles:
                await user.add_roles(role)
                details = f"Added {role.name}"
                await log_to_support_channel(interaction.user, details, user)
                await interaction.followup.send(f"✅ Added role **{role.name}** to {user.display_name}", ephemeral=True)
            else:
                await interaction.followup.send(f"❌ {user.display_name} already has the role **{role.name}**", ephemeral=True)
                
        elif command.value == "remove":
            # Remove role from user
            if role in user.roles:
                await user.remove_roles(role)
                details = f"Removed {role.name}"
                await log_to_support_channel(interaction.user, details, user)
                await interaction.followup.send(f"✅ Removed role **{role.name}** from {user.display_name}", ephemeral=True)
            else:
                await interaction.followup.send(f"❌ {user.display_name} doesn't have the role **{role.name}**", ephemeral=True)
                
        elif command.value == "swap":
            # Swap role (remove current warzone roles and add new one)
            warzone_roles_removed = []
            
            # Find and remove all warzone roles
            for role_id, mapping in WARZONE_MAPPINGS.items():
                warzone_role = discord.utils.get(interaction.guild.roles, id=int(role_id))
                if warzone_role and warzone_role in user.roles:
                    await user.remove_roles(warzone_role)
                    warzone_roles_removed.append(warzone_role.name)
            
            # Add new role
            await user.add_roles(role)
            
            # Log the swap action
            removed_roles_text = ", ".join(warzone_roles_removed) if warzone_roles_removed else "No warzone roles"
            details = f"Swapped roles (removed: {removed_roles_text}, added: {role.name})"
            await log_to_support_channel(interaction.user, details, user)
            
            await interaction.followup.send(
                f"✅ **Role Swap Completed**\n"
                f"**Removed:** {', '.join(warzone_roles_removed) if warzone_roles_removed else 'No warzone roles'}\n"
                f"**Added:** {role.name}\n"
                f"**User:** {user.display_name}",
                ephemeral=True
            )
        
    except discord.Forbidden:
        await interaction.followup.send("❌ Bot doesn't have permission to manage roles.", ephemeral=True)
    except Exception as e:
        await interaction.followup.send(f"❌ An error occurred: {str(e)}", ephemeral=True)
        print(f"Error in support_ars command: {e}")

# ===========================================================================================
# CHECK-IN COMMANDS
# ===========================================================================================

@tree.command(name="sunday-check-in", description="Sunday check-in for players")
@app_commands.describe(
    level="Player's ingame level",
    tournament_type="Tournament type to join"
)
@app_commands.choices(
    tournament_type=[
        app_commands.Choice(name="Main Tournament", value="main"),
        app_commands.Choice(name="Parallel Tournament", value="parallel")
    ]
)
async def sunday_check_in(interaction: discord.Interaction, level: int, tournament_type: app_commands.Choice[str]):
    """Sunday check-in command for players"""
    
    await interaction.response.defer(ephemeral=True)
    
    # Validate level
    if level < 1 or level > 100:
        await interaction.followup.send("❌ Level must be between 1 and 100", ephemeral=True)
        return

    try:
        # Get tournament roles
        joined_role_id = TOURNAMENT_ROLES.get(f"joined_{tournament_type.value}")
        round1_role_id = TOURNAMENT_ROLES.get(f"round1_{tournament_type.value}")
        
        if joined_role_id.startswith("JOINED_") or round1_role_id.startswith("ROUND1_"):
            await interaction.followup.send(f"❌ Tournament role IDs not configured. Please update TOURNAMENT_ROLES in the code.", ephemeral=True)
            return
        
        # Get role objects
        joined_role = discord.utils.get(interaction.guild.roles, id=int(joined_role_id))
        round1_role = discord.utils.get(interaction.guild.roles, id=int(round1_role_id))
        
        if not joined_role or not round1_role:
            await interaction.followup.send(f"❌ Tournament roles not found. Please check role configuration.", ephemeral=True)
            return
        
        # Check if user already has Joined role
        if joined_role in interaction.user.roles:
            await interaction.followup.send(f"❌ You have already checked in for {tournament_type.value.title()} tournament!", ephemeral=True)
            return
        
        # Add Joined role and Round1 role
        await interaction.user.add_roles(joined_role, round1_role)
        
        # Create check-in embed
        embed = discord.Embed(
            title="📅 Sunday Check-In",
            description=f"**Player:** {interaction.user.display_name}\n**Discord:** {interaction.user.mention}\n**Username:** {interaction.user.name}\n**Ingame Level:** {level}\n**Tournament:** {tournament_type.value.title()}",
            color=discord.Color.blue(),
            timestamp=discord.utils.utcnow()
        )
        
        embed.add_field(
            name="📊 Check-In Details",
            value=f"**Date:** {datetime.datetime.now().strftime('%A, %B %d, %Y')}\n**Time:** {datetime.datetime.now().strftime('%H:%M UTC')}\n**Status:** ✅ Checked In\n**Roles Added:** {joined_role.mention}, {round1_role.mention}",
            inline=False
        )
        
        embed.set_footer(text="Sunday Check-In • 😈The Devil's Spot😈")
        
        # Send confirmation to user
        await interaction.followup.send("✅ Sunday check-in completed successfully! You are now registered for the tournament.", ephemeral=True)
        
        # Log to support channel
        details = f"Sunday Check-In {tournament_type.value.title()} Tournament (Level: {level})"
        await log_to_support_channel(interaction.user, details)
        
    except discord.Forbidden:
        await interaction.followup.send("❌ Bot doesn't have permission to assign roles.", ephemeral=True)
    except Exception as e:
        await interaction.followup.send(f"❌ An error occurred during check-in: {str(e)}", ephemeral=True)
        print(f"Error in sunday_check_in command: {e}")

@tree.command(name="saturday-check-in", description="Saturday check-in for players")
@app_commands.describe(
    level="Player's ingame level",
    tournament_type="Tournament type to join"
)
@app_commands.choices(
    tournament_type=[
        app_commands.Choice(name="Main Tournament", value="main"),
        app_commands.Choice(name="Parallel Tournament", value="parallel")
    ]
)
async def saturday_check_in(interaction: discord.Interaction, level: int, tournament_type: app_commands.Choice[str]):
    """Saturday check-in command for players"""
    
    await interaction.response.defer(ephemeral=True)
    
    # Validate level
    if level < 1 or level > 100:
        await interaction.followup.send("❌ Level must be between 1 and 100", ephemeral=True)
        return
    
    try:
        # Get tournament roles
        joined_role_id = TOURNAMENT_ROLES.get(f"joined_{tournament_type.value}")
        round1_role_id = TOURNAMENT_ROLES.get(f"round1_{tournament_type.value}")
        
        if joined_role_id.startswith("JOINED_") or round1_role_id.startswith("ROUND1_"):
            await interaction.followup.send(f"❌ Tournament role IDs not configured. Please update TOURNAMENT_ROLES in the code.", ephemeral=True)
            return
        
        # Get role objects
        joined_role = discord.utils.get(interaction.guild.roles, id=int(joined_role_id))
        round1_role = discord.utils.get(interaction.guild.roles, id=int(round1_role_id))
        
        if not joined_role or not round1_role:
            await interaction.followup.send(f"❌ Tournament roles not found. Please check role configuration.", ephemeral=True)
            return
        
        # Check if user already has Joined role
        if joined_role in interaction.user.roles:
            await interaction.followup.send(f"❌ You have already checked in for {tournament_type.value.title()} tournament!", ephemeral=True)
            return
        
        # Add Joined role and Round1 role
        await interaction.user.add_roles(joined_role, round1_role)
        
        # Create check-in embed
        embed = discord.Embed(
            title="📅 Saturday Check-In",
            description=f"**Player:** {interaction.user.display_name}\n**Discord:** {interaction.user.mention}\n**Username:** {interaction.user.name}\n**Ingame Level:** {level}\n**Tournament:** {tournament_type.value.title()}",
            color=discord.Color.green(),
            timestamp=discord.utils.utcnow()
        )
        
        embed.add_field(
            name="📊 Check-In Details",
            value=f"**Date:** {datetime.datetime.now().strftime('%A, %B %d, %Y')}\n**Time:** {datetime.datetime.now().strftime('%H:%M UTC')}\n**Status:** ✅ Checked In\n**Roles Added:** {joined_role.mention}, {round1_role.mention}",
            inline=False
        )
        
        embed.set_footer(text="Saturday Check-In • 😈The Devil's Spot😈")
        
        # Send confirmation to user
        await interaction.followup.send("✅ Saturday check-in completed successfully! You are now registered for the tournament.", ephemeral=True)
        
        # Log to support channel
        details = f"Saturday Check-In {tournament_type.value.title()} Tournament (Level: {level})"
        await log_to_support_channel(interaction.user, details)
        
    except discord.Forbidden:
        await interaction.followup.send("❌ Bot doesn't have permission to assign roles.", ephemeral=True)
    except Exception as e:
        await interaction.followup.send(f"❌ An error occurred during check-in: {str(e)}", ephemeral=True)
        print(f"Error in saturday_check_in command: {e}")

@tree.command(name="remove-joined-roles", description="Remove Joined roles after check-in period ends")
@app_commands.describe(
    tournament_type="Tournament type to remove roles from"
)
@app_commands.choices(
    tournament_type=[
        app_commands.Choice(name="Main Tournament", value="main"),
        app_commands.Choice(name="Parallel Tournament", value="parallel"),
        app_commands.Choice(name="Both Tournaments", value="both")
    ]
)
async def remove_joined_roles(interaction: discord.Interaction, tournament_type: app_commands.Choice[str]):
    """Remove Joined roles after check-in period ends"""
    
    await interaction.response.defer(ephemeral=True)
    
    # Check permissions
    if not has_event_result_permission(interaction):
        await interaction.followup.send("❌ You need **Commander**, **Main Judge**, **Super Admin**, or **Admin** role to use this command.", ephemeral=True)
        return
    
    try:
        roles_to_remove = []
        
        if tournament_type.value in ["main", "both"]:
            main_joined_id = TOURNAMENT_ROLES.get("joined_main")
            if not main_joined_id.startswith("JOINED_"):
                main_joined_role = discord.utils.get(interaction.guild.roles, id=int(main_joined_id))
                if main_joined_role:
                    roles_to_remove.append(main_joined_role)
        
        if tournament_type.value in ["parallel", "both"]:
            parallel_joined_id = TOURNAMENT_ROLES.get("joined_parallel")
            if not parallel_joined_id.startswith("JOINED_"):
                parallel_joined_role = discord.utils.get(interaction.guild.roles, id=int(parallel_joined_id))
                if parallel_joined_role:
                    roles_to_remove.append(parallel_joined_role)
        
        if not roles_to_remove:
            await interaction.followup.send("❌ Tournament role IDs not configured. Please update TOURNAMENT_ROLES in the code.", ephemeral=True)
            return
        
        # Find all members with these roles
        total_removed = 0
        for role in roles_to_remove:
            for member in role.members:
                try:
                    await member.remove_roles(role)
                    total_removed += 1
                except discord.Forbidden:
                    print(f"Error: Bot doesn't have permission to remove role {role.name} from {member.display_name}")
                except Exception as e:
                    print(f"Error removing role from {member.display_name}: {e}")
        
        # Create confirmation embed
        embed = discord.Embed(
            title="🧹 Joined Roles Cleanup",
            description=f"**Tournament Type:** {tournament_type.value.title()}\n**Roles Removed:** {len(roles_to_remove)}\n**Total Members Affected:** {total_removed}",
            color=discord.Color.orange(),
            timestamp=discord.utils.utcnow()
        )
        
        embed.add_field(
            name="📋 Removed Roles",
            value="\n".join([f"• {role.name}" for role in roles_to_remove]),
            inline=False
        )
        
        embed.add_field(
            name="👨‍⚖️ Staff",
            value=f"**Cleaned up by:** {interaction.user.mention}",
            inline=False
        )
        
        embed.set_footer(text="Tournament Cleanup • 😈The Devil's Spot😈")
        
        # Send to channel
        await interaction.channel.send(embed=embed)
        
        # Send confirmation to user
        await interaction.followup.send(f"✅ Successfully removed Joined roles for {tournament_type.value.title()} tournament from {total_removed} members.", ephemeral=True)
        
        # Log to support channel
        details = f"Removed Joined roles for {tournament_type.value.title()} tournament"
        await log_to_support_channel(interaction.user, details)
        
    except Exception as e:
        await interaction.followup.send(f"❌ An error occurred: {str(e)}", ephemeral=True)
        print(f"Error in remove_joined_roles command: {e}")

# ===========================================================================================
# BOT STARTUP
# ===========================================================================================

if __name__ == "__main__":
    # Get Discord token from environment
    token = os.environ.get("DISCORD_TOKEN")
    
    if not token:
        for key, value in os.environ.items():
            if 'DISCORD' in key and 'TOKEN' in key:
                token = value
                break
    
    if not token:
        print("❌ Discord token not found in environment variables.")
        print("Please set your Discord bot token in the DISCORD_TOKEN environment variable.")
        print("You can also create a .env file with: DISCORD_TOKEN=your_token_here")
        exit(1)
    
    try:
        print("🚀 Starting Discord bot...")
        print("📡 Connecting to Discord...")
        bot.run(token, log_handler=None)
    except discord.LoginFailure:
        print("❌ Invalid Discord token. Please check your bot token.")
        exit(1)
    except discord.HTTPException as e:
        print(f"❌ HTTP error connecting to Discord: {e}")
        exit(1)
    except Exception as e:
        print(f"❌ Error starting bot: {e}")
        exit(1)

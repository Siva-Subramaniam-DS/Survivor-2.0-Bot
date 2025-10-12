"""
Quick test script to verify credentials.json is working correctly
Run this before deploying to Railway!
"""

import os
import sys

print("🔍 Testing credentials.json setup...\n")

# Test 1: Check if file exists
print("1️⃣ Checking if credentials.json exists...")
if os.path.exists("credentials.json"):
    print("   ✅ credentials.json found!")
else:
    print("   ❌ credentials.json NOT found!")
    print("   💡 Make sure it's in the same folder as app.py")
    sys.exit(1)

# Test 2: Check if it's valid JSON
print("\n2️⃣ Checking if credentials.json is valid JSON...")
try:
    import json
    with open("credentials.json", "r") as f:
        creds_data = json.load(f)
    print("   ✅ Valid JSON format!")
except json.JSONDecodeError as e:
    print(f"   ❌ Invalid JSON format: {e}")
    sys.exit(1)
except Exception as e:
    print(f"   ❌ Error reading file: {e}")
    sys.exit(1)

# Test 3: Check required fields
print("\n3️⃣ Checking required fields...")
required_fields = ["type", "project_id", "private_key", "client_email"]
missing_fields = []
for field in required_fields:
    if field in creds_data:
        print(f"   ✅ {field}: Found")
    else:
        print(f"   ❌ {field}: Missing")
        missing_fields.append(field)

if missing_fields:
    print(f"\n   ⚠️ Missing required fields: {', '.join(missing_fields)}")
    sys.exit(1)

# Test 4: Display service account email
print("\n4️⃣ Service Account Email:")
client_email = creds_data.get("client_email", "NOT FOUND")
print(f"   📧 {client_email}")
print("\n   ⚠️ IMPORTANT: You MUST share your Google Sheet with this email!")
print(f"   📋 Copy this email: {client_email}")

# Test 5: Try to initialize Google Sheets client
print("\n5️⃣ Testing Google Sheets connection...")
try:
    import gspread
    from google.oauth2.service_account import Credentials
    
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = Credentials.from_service_account_file("credentials.json", scopes=scope)
    client = gspread.authorize(creds)
    print("   ✅ Google Sheets client initialized successfully!")
    
    # Test 6: Try to access the spreadsheet
    print("\n6️⃣ Testing access to your spreadsheet...")
    try:
        spreadsheet_id = "1PrULRObdldtnsCiPp1JAdGwzbgvj55mBalfLxfSTj3M"
        spreadsheet = client.open_by_key(spreadsheet_id)
        print(f"   ✅ Successfully accessed spreadsheet: {spreadsheet.title}")
        
        # Try to access the worksheet
        try:
            worksheet = spreadsheet.worksheet("Give Sheet - H")
            print(f"   ✅ Successfully accessed worksheet: {worksheet.title}")
            print(f"   📊 Worksheet has {worksheet.row_count} rows and {worksheet.col_count} columns")
        except gspread.WorksheetNotFound:
            print("   ⚠️ Worksheet 'Give Sheet - H' not found!")
            print("   💡 Available worksheets:")
            for ws in spreadsheet.worksheets():
                print(f"      - {ws.title}")
        
    except gspread.exceptions.APIError as e:
        print(f"   ❌ API Error: {e}")
        print("   💡 Make sure you've shared the sheet with the service account email!")
    except Exception as e:
        print(f"   ❌ Error accessing spreadsheet: {e}")
        
except ImportError as e:
    print(f"   ⚠️ Missing required packages: {e}")
    print("   💡 Run: pip install gspread google-auth")
except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n" + "="*60)
print("🎉 Test complete!")
print("="*60)
print("\n📝 Next Steps:")
print("1. If you see any ❌ errors above, fix them first")
print("2. Make sure you've shared the Google Sheet with the service account email")
print("3. Add your bot token to .env file: DISCORD_TOKEN=your_token")
print("4. Run your bot: python app.py")
print("\n🚀 For Railway deployment:")
print("1. Set DISCORD_TOKEN in Railway environment variables")
print("2. Set GOOGLE_CREDENTIALS in Railway environment variables")
print("   (Copy the entire content of credentials.json)")


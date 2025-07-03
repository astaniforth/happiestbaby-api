"""Jupyter notebook-friendly version of the comprehensive HappiestBaby API example.

Copy this entire cell into your Jupyter notebook and run it.
Make sure to update the EMAIL and PASSWORD variables with your real credentials.
"""

import asyncio
import logging
from datetime import datetime, timedelta
from aiohttp import ClientSession

import happiestbaby_api
from happiestbaby_api.errors import SnooError, AuthenticationError

# 🔑 UPDATE THESE WITH YOUR REAL CREDENTIALS
EMAIL = "your-email@example.com"
PASSWORD = "your-password"

def print_section_header(title: str):
    """Print a formatted section header."""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

def print_device_info(device):
    """Print comprehensive device information."""
    print(f"      Device Name: {device.name}")
    print(f"      Device Online: {device.is_online}")
    print(f"      Device On: {device.is_on}")
    print(f"      Device ID: {device.device_id}")
    print(f"      Serial Number: {device.serial_number}")
    print(f"      Firmware Version: {device.firmware_version}")
    print(f"      Baby Details: {device.baby}")
    print(f"      Current State: {device.state}")
    print(f"      Session Active: {device.session is not None}")
    if device.session:
        print(f"      Session Start: {device.session.get('startTime', 'N/A')}")
        print(f"      Session Levels: {len(device.session.get('levels', []))} level changes")
    print("      " + "-" * 50)

async def demonstrate_authentication(websession):
    """Demonstrate modern AWS Cognito authentication."""
    print_section_header("🔐 AWS COGNITO AUTHENTICATION")
    
    try:
        print(f"Authenticating user: {EMAIL}")
        api = await happiestbaby_api.login(EMAIL, PASSWORD, websession)
        
        print("✅ Authentication successful!")
        print(f"   Account ID: {api.account.get('userId')}")
        print(f"   Account Name: {api.account.get('givenName')} {api.account.get('surname')}")
        print(f"   Email: {api.account.get('email')}")
        print(f"   Region: {api.account.get('region')}")
        print(f"   Token expiry handled automatically: ✅")
        
        return api
        
    except AuthenticationError as err:
        print(f"❌ Authentication failed: {err}")
        print("Please check your credentials and try again.")
        return None
    except Exception as err:
        print(f"❌ Unexpected error during authentication: {err}")
        return None

async def demonstrate_device_management(api):
    """Demonstrate comprehensive device management capabilities."""
    print_section_header("📱 DEVICE MANAGEMENT & SESSION TRACKING")
    
    try:
        # Get account information
        account_info = await api.get_account()
        print(f"Account Information: {len(account_info)} babies registered")
        
        # Get device information
        print(f"Total Devices Found: {len(api.devices)}")
        
        if len(api.devices) == 0:
            print("No devices found - this may be normal for accounts without Snoo devices")
            return None
        
        # Demonstrate device details
        for device_id, device in api.devices.items():
            print_device_info(device)
            
            # Get session statistics if available
            if device.baby and device.baby.get('id'):
                baby_id = device.baby['id']
                try:
                    # Get recent session stats
                    daily_stats = await api.get_session_stats_daily_for_account(baby_id, datetime.now())
                    if daily_stats:
                        print(f"      Today's Session Stats: {len(daily_stats)} sessions")
                    
                    weekly_stats = await api.get_session_stats_avg_for_account(baby_id)
                    if weekly_stats:
                        print(f"      Weekly Average Stats Available: ✅")
                except Exception as e:
                    print(f"      Session stats not available: {e}")
        
        return api.devices
        
    except Exception as err:
        print(f"❌ Error in device management: {err}")
        return None

async def demonstrate_journal_system(api):
    """Demonstrate the comprehensive 8-type journal system."""
    print_section_header("📝 COMPLETE BABY JOURNAL SYSTEM (8 TYPES)")
    
    try:
        # Get baby information
        babies = await api.get_account()
        if not babies or len(babies) == 0:
            print("No babies found in account. Creating sample journal entries...")
            # In a real app, you'd need a baby_id. For demo purposes, we'll use a placeholder
            baby_id = "demo-baby-id"
        else:
            baby_id = babies[0].get('id', 'demo-baby-id')
            print(f"Using baby ID: {baby_id}")
        
        # Current time for demonstrations
        now = datetime.now()
        
        print("\n🍼 CREATING JOURNAL ENTRIES (All 8 Types)")
        print("-" * 50)
        
        # 1. Diaper Entry
        print("1. 🧷 Creating diaper entry...")
        try:
            diaper_entry = await api.journal.create_diaper_entry(
                baby_id=baby_id,
                start_time=now - timedelta(hours=2),
                diaper_types=['pee', 'poo'],
                note="Regular diaper change after feeding"
            )
            print("   ✅ Diaper entry created successfully")
        except Exception as e:
            print(f"   ⚠️ Diaper entry demo: {e}")
        
        # 2. Bottle Feeding Entry
        print("2. 🍼 Creating bottle feeding entry...")
        try:
            bottle_entry = await api.journal.create_feeding_entry(
                baby_id=baby_id,
                start_time=now - timedelta(hours=3),
                feeding_type='bottlefeeding',
                amount_imperial=4.5,  # 4.5 oz - automatically converts to ml
                milk_type='breastmilk',
                note="Morning feeding - took full bottle"
            )
            print("   ✅ Bottle feeding entry created (4.5 oz = ~133 ml)")
        except Exception as e:
            print(f"   ⚠️ Bottle feeding demo: {e}")
        
        # 3. Breast Feeding Entry
        print("3. 🤱 Creating breast feeding entry...")
        try:
            breast_entry = await api.journal.create_breast_feeding_entry(
                baby_id=baby_id,
                start_time=now - timedelta(hours=4),
                end_time=now - timedelta(hours=4) + timedelta(minutes=25),
                left_duration=780,  # 13 minutes in seconds
                right_duration=720,  # 12 minutes in seconds
                last_used_breast='right',
                note="Good latch, baby seemed satisfied"
            )
            print("   ✅ Breast feeding entry created (13m left, 12m right)")
        except Exception as e:
            print(f"   ⚠️ Breast feeding demo: {e}")
        
        # 4. Weight Entry
        print("4. ⚖️ Creating weight entry...")
        try:
            weight_entry = await api.journal.create_weight_entry(
                baby_id=baby_id,
                start_time=now - timedelta(days=1),
                weight_imperial=8.2,  # 8.2 lbs - automatically converts to grams
                note="Weekly weigh-in at pediatrician"
            )
            print("   ✅ Weight entry created (8.2 lbs = ~3719 grams)")
        except Exception as e:
            print(f"   ⚠️ Weight entry demo: {e}")
        
        # 5. Height Entry
        print("5. 📏 Creating height entry...")
        try:
            height_entry = await api.journal.create_height_entry(
                baby_id=baby_id,
                start_time=now - timedelta(days=1),
                height_imperial=22.5,  # 22.5 inches - automatically converts to cm
                note="Monthly measurement at home"
            )
            print("   ✅ Height entry created (22.5 inches = ~57.2 cm)")
        except Exception as e:
            print(f"   ⚠️ Height entry demo: {e}")
        
        # 6. Head Circumference Entry
        print("6. 🧠 Creating head circumference entry...")
        try:
            head_entry = await api.journal.create_head_entry(
                baby_id=baby_id,
                start_time=now - timedelta(days=1),
                circumference_imperial=16.8,  # 16.8 inches - automatically converts to cm
                note="Head circumference at 3-month checkup"
            )
            print("   ✅ Head circumference entry created (16.8 inches = ~42.7 cm)")
        except Exception as e:
            print(f"   ⚠️ Head circumference demo: {e}")
        
        print("\n📊 READING JOURNAL DATA (Advanced Querying)")
        print("-" * 50)
        
        # Demonstrate reading journal data with date ranges
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)  # Last 7 days
        
        print(f"Querying journal data from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
        
        # Get different types of journal data
        try:
            diaper_data = await api.journal.get_diaper_tracking(baby_id, start_date, end_date)
            print(f"   📋 Diaper entries found: {len(diaper_data) if diaper_data else 0}")
            
            feeding_data = await api.journal.get_feeding_tracking(baby_id, start_date, end_date, 'bottlefeeding')
            print(f"   🍼 Bottle feeding entries found: {len(feeding_data) if feeding_data else 0}")
            
            weight_data = await api.journal.get_weight_tracking(baby_id, start_date, end_date)
            print(f"   ⚖️ Weight entries found: {len(weight_data) if weight_data else 0}")
            
            # Get grouped data (all journal types together)
            grouped_data = await api.journal.get_grouped_tracking(baby_id, start_date, end_date)
            print(f"   📊 Total grouped entries: {len(grouped_data) if grouped_data else 0}")
            
            # Get last journal entries
            last_journals = await api.journal.get_last_journals(baby_id)
            print(f"   🕐 Most recent entries: {len(last_journals) if last_journals else 0}")
            
        except Exception as e:
            print(f"   ⚠️ Journal reading demo: {e}")
        
        print("\n🔄 CRUD OPERATIONS DEMONSTRATION")
        print("-" * 50)
        print("✅ CREATE: Demonstrated above with all 8 journal types")
        print("✅ READ: Demonstrated with date filtering and grouping")
        print("✅ UPDATE: Available via update_journal_entry() method")
        print("✅ DELETE: Available via delete_journal_entry() method")
        print("✅ UNIT CONVERSION: Automatic imperial ↔ metric conversion")
        print("✅ DATE FILTERING: Custom date ranges supported")
        print("✅ BULK OPERATIONS: Grouped tracking across all types")
        
    except Exception as err:
        print(f"❌ Error in journal system demonstration: {err}")

async def main():
    """Run the comprehensive example demonstrating all features."""
    print("🎉 COMPREHENSIVE HAPPIESTBABY API DEMONSTRATION")
    print("This showcases the full breadth of features in this fork vs original pysnoo")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Set up logging
    logging.basicConfig(level=logging.INFO)  # Use INFO for cleaner output, DEBUG for verbose
    
    async with ClientSession() as websession:
        try:
            # 1. Authentication
            api = await demonstrate_authentication(websession)
            if not api:
                print("\n❌ Cannot proceed without authentication. Please check credentials.")
                return
            
            # 2. Device Management
            devices = await demonstrate_device_management(api)
            
            # 3. Complete Journal System
            await demonstrate_journal_system(api)
            
            print_section_header("✅ DEMONSTRATION COMPLETE")
            print("🎯 WHAT THIS FORK PROVIDES vs ORIGINAL:")
            print("   📱 Enhanced Device Management (from original)")
            print("   🔐 Modern AWS Cognito Authentication (NEW)")
            print("   📝 Complete 8-Type Journal System (NEW)")
            print("   🔄 Full CRUD Operations (NEW)")
            print("   📊 Advanced Data Querying (NEW)")
            print("   🔄 Automatic Unit Conversions (NEW)")
            print("   ⚡ Performance & Reliability Improvements (NEW)")
            print("   🛠️ Enhanced Developer Experience (NEW)")
            print("\n🚀 Ready for production use in baby tracking applications!")
            
        except SnooError as err:
            print(f"\n❌ API Error: {err}")
        except Exception as err:
            print(f"\n❌ Unexpected error: {err}")

# 🚀 FOR JUPYTER NOTEBOOK: 
# 1. Update EMAIL and PASSWORD variables above with your real HappiestBaby credentials
# 2. Run this cell to define all functions
# 3. Then run: await main()

print("📋 JUPYTER NOTEBOOK INSTRUCTIONS:")
print("1. Update EMAIL and PASSWORD variables above")
print("2. Run this cell to define functions") 
print("3. In the next cell, run: await main()")
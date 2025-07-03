#!/usr/bin/env python3
"""
Example usage of the journal functionality in pysnooapi.

This demonstrates how to use the new journal features to track
baby activities like feeding, diaper changes, and growth measurements.
"""

import asyncio
import os
from datetime import datetime, timedelta
from happiestbaby_api import login, JOURNAL_TYPES

async def main():
    """Example of using journal functionality."""
    
    # Get credentials from environment variables for security
    username = os.getenv('SNOO_USERNAME')
    password = os.getenv('SNOO_PASSWORD')
    
    if not username or not password:
        print("Please set SNOO_USERNAME and SNOO_PASSWORD environment variables")
        return
    
    try:
        # Login to the API
        print("Logging in to Snoo API...")
        api = await login(username, password)
        print("Login successful!")
        
        # Get baby information
        babies = await api.get_babies_v10()
        if not babies:
            print("No babies found")
            return
        
        baby = babies[0]  # Use first baby
        baby_id = baby['_id']
        print(f"Found baby: {baby.get('babyName', 'Unknown')}")
        
        # Get journal data for the last 7 days
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=7)
        
        print(f"\nGetting journal data from {start_date.date()} to {end_date.date()}")
        
        # Get grouped activity tracking
        print("\n=== Recent Activity Summary ===")
        grouped_data = await api.journal.get_grouped_tracking(
            baby_id, start_date, end_date, "activity"
        )
        
        if grouped_data:
            print(f"Found {len(grouped_data)} activity entries")
            for entry in grouped_data[-5:]:  # Show last 5 entries
                entry_type = entry.get('type', 'unknown')
                start_time = entry.get('startTime', 'unknown')
                print(f"  - {entry_type}: {start_time}")
        
        # Get diaper changes
        print("\n=== Diaper Changes ===")
        diaper_data = await api.journal.get_diaper_tracking(
            baby_id, start_date, end_date
        )
        
        if diaper_data:
            print(f"Found {len(diaper_data)} diaper changes")
            for entry in diaper_data[-3:]:  # Show last 3
                types = entry.get('data', {}).get('types', [])
                start_time = entry.get('startTime', 'unknown')
                print(f"  - {', '.join(types)}: {start_time}")
        
        # Get feeding data
        print("\n=== Bottle Feeding ===")
        feeding_data = await api.journal.get_feeding_tracking(
            baby_id, start_date, end_date, JOURNAL_TYPES['BOTTLE_FEEDING']
        )
        
        if feeding_data:
            print(f"Found {len(feeding_data)} bottle feedings")
            for entry in feeding_data[-3:]:  # Show last 3
                data = entry.get('data', {})
                amount = data.get('amountImperial', 'unknown')
                milk_type = data.get('type', 'unknown')
                start_time = entry.get('startTime', 'unknown')
                print(f"  - {amount}oz {milk_type}: {start_time}")
        
        # Get weight tracking
        print("\n=== Weight Tracking ===")
        weight_data = await api.journal.get_weight_tracking(
            baby_id, start_date, end_date
        )
        
        if weight_data:
            print(f"Found {len(weight_data)} weight measurements")
            for entry in weight_data:
                data = entry.get('data', {})
                weight_oz = data.get('weightImperial', 'unknown')
                weight_g = data.get('weightMetric', 'unknown')
                start_time = entry.get('startTime', 'unknown')
                print(f"  - {weight_oz}oz ({weight_g}g): {start_time}")
        
        # Get latest journals
        print("\n=== Latest Journal Entries ===")
        latest = await api.journal.get_last_journals(baby_id)
        
        if latest:
            print(f"Found {len(latest)} recent entries")
            for entry in latest[-5:]:
                entry_type = entry.get('type', 'unknown')
                start_time = entry.get('startTime', 'unknown')
                print(f"  - {entry_type}: {start_time}")
        
        # Example of creating a new journal entry (commented out for safety)
        """
        # Create a diaper change entry
        new_diaper = await api.journal.create_diaper_entry(
            baby_id=baby_id,
            start_time=datetime.utcnow(),
            diaper_types=['pee'],
            note="Example diaper change"
        )
        print(f"Created diaper entry: {new_diaper}")
        
        # Create a feeding entry
        new_feeding = await api.journal.create_feeding_entry(
            baby_id=baby_id,
            start_time=datetime.utcnow(),
            feeding_type=JOURNAL_TYPES['BOTTLE_FEEDING'],
            amount_imperial=4.0,
            amount_metric=118.29,
            milk_type='breastmilk',
            note="Example feeding"
        )
        print(f"Created feeding entry: {new_feeding}")
        """
        
        print("\nJournal data retrieval complete!")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
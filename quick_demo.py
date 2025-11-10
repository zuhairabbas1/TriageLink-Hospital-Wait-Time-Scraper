"""
Quick Test Script - For Interview Demonstration
This version collects just 2 data points (5 minutes apart) for quick demo
"""

import requests
import pandas as pd
from datetime import datetime
import time

def quick_demo():
    """
    Quick demonstration version that collects 2 data points 5 minutes apart.
    Perfect for showing during the interview.
    """
    print("=" * 60)
    print("HOSPITAL WAIT TIME SCRAPER - QUICK DEMO")
    print("=" * 60)
    print("This demo will collect 2 data snapshots, 5 minutes apart")
    print("In production, this runs for 72 hours at 30-minute intervals")
    print("=" * 60)
    
    url = "https://howlongwilliwait.com/sample.json"
    all_records = []
    
    for snapshot in range(2):
        print(f"\n📊 Collecting Snapshot {snapshot + 1}/2...")
        print(f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        try:
            # Fetch data
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Get timestamp
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Process each hospital
            for hospital, wait_time in data.items():
                record = {
                    'Timestamp': timestamp,
                    'Hospital Name': hospital,
                    'Wait Time': wait_time if wait_time else "Not available"
                }
                all_records.append(record)
            
            print(f"✅ Successfully collected data for {len(data)} hospitals")
            
        except Exception as e:
            print(f"❌ Error: {e}")
        
        # Wait 5 minutes for next snapshot (unless last iteration)
        if snapshot < 1:
            print("\n⏳ Waiting 5 minutes for next snapshot...")
            print("   (In production: 30 minutes)")
            time.sleep(300)  # 5 minutes = 300 seconds
    
    # Save to Excel
    print("\n" + "=" * 60)
    print("💾 Saving to Excel...")
    
    df = pd.DataFrame(all_records)
    output_file = "demo_hospital_wait_times.xlsx"
    
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Wait Times')
        worksheet = writer.sheets['Wait Times']
        
        # Auto-adjust columns
        for idx, col in enumerate(df.columns):
            max_length = max(df[col].astype(str).apply(len).max(), len(col)) + 2
            worksheet.column_dimensions[chr(65 + idx)].width = max_length
    
    print(f"✅ Demo complete! Data saved to: {output_file}")
    print(f"📊 Total records collected: {len(all_records)}")
    print("=" * 60)
    
    # Show sample data
    print("\n📋 Sample Data Preview:")
    print(df.head(10).to_string(index=False))

if __name__ == "__main__":
    quick_demo()
"""
Hospital Wait Time Data Collection Script
Author: Zuhair
Purpose: Collect ER wait time data from howlongwilliwait.com every 30 minutes
For: TriageLink Interview - Riipen Project
"""

import requests
import pandas as pd
from datetime import datetime
import time
import json
import os

class HospitalWaitTimeScraper:
    """
    A class to scrape hospital wait time data and save it to Excel.
    """
    
    def __init__(self, url, output_file='hospital_wait_times.xlsx'):
        """
        Initialize the scraper with the data source URL and output file name.
        
        Args:
            url (str): The API endpoint URL for hospital data
            output_file (str): Name of the Excel file to save data
        """
        self.url = url
        self.output_file = output_file
        self.data_records = []
        
    def fetch_data(self):
        """
        Fetch hospital wait time data from the API.
        
        Returns:
            dict: Hospital data as a dictionary, or None if request fails
        """
        try:
            response = requests.get(self.url, timeout=10)
            response.raise_for_status()  # Raise exception for bad status codes
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None
    
    def parse_wait_time(self, wait_time_str):
        """
        Parse wait time string into minutes for easier analysis.
        Handles formats like "2 hr 12 min", "Not available", "1 hr or less to1 hr 9 min"
        
        Args:
            wait_time_str (str): Raw wait time string from API
            
        Returns:
            str: Original wait time string (kept as string for clarity in Excel)
        """
        # For this assignment, we keep the original format for readability
        # In a production system, we would convert to numerical values
        return wait_time_str if wait_time_str else "Not available"
    
    def collect_single_snapshot(self):
        """
        Collect a single snapshot of hospital wait times with timestamp.
        
        Returns:
            bool: True if successful, False otherwise
        """
        print(f"Collecting data at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        data = self.fetch_data()
        if data is None:
            print("Failed to fetch data")
            return False
        
        # Get current timestamp
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Process each hospital
        for hospital_name, wait_time in data.items():
            record = {
                'Timestamp': timestamp,
                'Hospital Name': hospital_name,
                'Wait Time': self.parse_wait_time(wait_time)
            }
            self.data_records.append(record)
        
        print(f"Successfully collected data for {len(data)} hospitals")
        return True
    
    def save_to_excel(self):
        """
        Save all collected data to an Excel spreadsheet.
        Creates a well-formatted Excel file with proper headers.
        """
        if not self.data_records:
            print("No data to save")
            return
        
        # Convert to DataFrame
        df = pd.DataFrame(self.data_records)
        
        # Create Excel writer with formatting
        with pd.ExcelWriter(self.output_file, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Wait Times')
            
            # Get the worksheet to apply formatting
            worksheet = writer.sheets['Wait Times']
            
            # Auto-adjust column widths
            for idx, col in enumerate(df.columns):
                max_length = max(
                    df[col].astype(str).apply(len).max(),
                    len(col)
                ) + 2
                worksheet.column_dimensions[chr(65 + idx)].width = max_length
        
        print(f"Data saved to {self.output_file}")
        print(f"Total records: {len(self.data_records)}")
    
    def run_collection(self, duration_hours=72, interval_minutes=30):
        """
        Run the data collection process for a specified duration.
        
        Args:
            duration_hours (int): How many hours to collect data (default: 72 = 3 days)
            interval_minutes (int): Interval between collections in minutes (default: 30)
        """
        print(f"Starting data collection for {duration_hours} hours")
        print(f"Collection interval: {interval_minutes} minutes")
        print(f"Output file: {self.output_file}")
        print("-" * 60)
        
        total_iterations = (duration_hours * 60) // interval_minutes
        interval_seconds = interval_minutes * 60
        
        for iteration in range(total_iterations):
            print(f"\nIteration {iteration + 1}/{total_iterations}")
            
            # Collect data
            success = self.collect_single_snapshot()
            
            # Save to Excel after each collection (in case script stops)
            if success:
                self.save_to_excel()
            
            # Wait for next interval (unless it's the last iteration)
            if iteration < total_iterations - 1:
                print(f"Waiting {interval_minutes} minutes until next collection...")
                time.sleep(interval_seconds)
        
        print("\n" + "=" * 60)
        print("Data collection completed!")
        print(f"Final data saved to {self.output_file}")
        print("=" * 60)


def main():
    """
    Main function to run the hospital wait time scraper.
    """
    # Configuration
    API_URL = "https://howlongwilliwait.com/sample.json"
    OUTPUT_FILE = "hospital_wait_times.xlsx"
    
    # Create scraper instance
    scraper = HospitalWaitTimeScraper(API_URL, OUTPUT_FILE)
    
    # Run collection for 3 days (72 hours) at 30-minute intervals
    # Note: For testing, you can reduce duration_hours to 1 or 2
    scraper.run_collection(duration_hours=72, interval_minutes=30)


if __name__ == "__main__":
    main()
# Hospital Wait Time Data Collection Script

**Author:** Zuhair  
**Project:** TriageLink Interview Assignment  
**Date:** November 2025

## Project Overview

This Python script automatically collects emergency room wait time data from howlongwilliwait.com every 30 minutes and saves it to an Excel spreadsheet. This is designed to support TriageLink's mission of helping patients find faster access to healthcare.

## Features

- ✅ Fetches real-time hospital wait time data from API
- ✅ Collects data every 30 minutes automatically
- ✅ Saves data to a well-formatted Excel spreadsheet
- ✅ Handles errors gracefully (network issues, missing data)
- ✅ Timestamps each data snapshot
- ✅ Runs continuously for 72 hours (3 days)
- ✅ Auto-saves after each collection to prevent data loss

## Technical Stack

- **Python 3.8+**
- **Libraries:**
  - `requests` - HTTP requests to fetch data
  - `pandas` - Data manipulation and Excel export
  - `openpyxl` - Excel file formatting

## Installation

### Step 1: Install Python
Make sure you have Python 3.8 or higher installed.

### Step 2: Install Required Libraries
```bash
pip install -r requirements.txt
```

Or install individually:
```bash
pip install requests pandas openpyxl
```

## Usage

### Basic Usage
```bash
python hospital_wait_time_scraper.py
```

The script will:
1. Start collecting data immediately
2. Fetch data every 30 minutes
3. Save to `hospital_wait_times.xlsx`
4. Run for 72 hours (3 days) by default

### Customizing Duration and Interval

To modify the collection settings, edit the `main()` function in the script:

```python
# Example: Collect for 24 hours instead of 72
scraper.run_collection(duration_hours=24, interval_minutes=30)

# Example: Collect every 15 minutes
scraper.run_collection(duration_hours=72, interval_minutes=15)
```

## Output Format

The Excel file contains three columns:

| Timestamp | Hospital Name | Wait Time |
|-----------|--------------|-----------|
| 2025-11-09 14:30:00 | Toronto General (University Health Network) | 2 hr 12 min |
| 2025-11-09 14:30:00 | Sunnybrook | 8 hr 25 min |
| 2025-11-09 15:00:00 | Toronto General (University Health Network) | 2 hr 15 min |

## Code Architecture

### Class Structure

**HospitalWaitTimeScraper**
- `__init__()` - Initialize with URL and output file
- `fetch_data()` - GET request to API endpoint
- `parse_wait_time()` - Parse wait time strings
- `collect_single_snapshot()` - Collect data at one point in time
- `save_to_excel()` - Save all data to Excel with formatting
- `run_collection()` - Main loop for continuous collection

## Error Handling

The script handles:
- Network timeouts
- Invalid API responses
- Missing data fields
- File system errors

## Why This Approach?

1. **Reliability:** Auto-saves after each collection to prevent data loss
2. **Scalability:** Easy to modify interval and duration
3. **Maintainability:** Clean object-oriented design with clear functions
4. **Production-Ready:** Proper error handling and logging

## Future Enhancements

For a production system, consider:
- Database storage (PostgreSQL, MongoDB)
- Cloud deployment (AWS Lambda, Azure Functions)
- Real-time dashboard integration
- Wait time prediction using historical data
- Multi-source data aggregation
- Alert system for unusual wait times

## Relevance to TriageLink

This script demonstrates:
- ✅ Data collection from healthcare APIs
- ✅ Automated data pipeline creation
- ✅ Real-world healthcare data handling
- ✅ Foundation for predictive modeling
- ✅ Data preparation for visualization dashboards

The collected data can be used to:
- Train ML models for wait time prediction
- Identify patterns by time of day/day of week
- Support real-time triage decision-making
- Improve patient communication and experience

## Testing

For quick testing during the interview, modify to collect for 1 hour:

```python
scraper.run_collection(duration_hours=1, interval_minutes=30)
```

This will collect 2 data points in 30 minutes.

## Contact

**Zuhair**  
Mathematics Student, Queen's University  
# Offline Fleet Management System

## Overview

This Fleet Management System is designed to work completely **offline** - no internet connection required! All your business data stays on your local computer, giving you complete control and privacy.

## What Works Offline

✅ **Complete Vehicle Fleet Management**
- Add, edit, and track all your vehicles
- Record maintenance history and costs
- Schedule upcoming maintenance

✅ **Tool & Equipment Hire Management**  
- Manage your rental equipment inventory
- Process customer rentals and returns
- Track rental revenue and equipment status

✅ **Data Analytics & Reports**
- View dashboard with charts and metrics
- Export all data to CSV files
- Generate business reports

✅ **Data Import/Export**
- Import existing data from CSV files
- Export for backup or external use
- Transfer data between systems

## How It Stores Your Data

Your business data is stored in simple CSV files on your computer:

```
data/
├── vehicles.csv        (Your vehicle fleet)
├── maintenance.csv     (Service records)
├── equipment.csv       (Tools and equipment)
└── rentals.csv        (Rental transactions)
```

These files are:
- **Human readable** - Open with Excel or any spreadsheet program
- **Portable** - Copy to USB drive or backup easily
- **Standard format** - Compatible with other business software

## Setting Up for Offline Use

### 1. Install Python (One-time setup)
If Python isn't installed on your computer:
- Download from [python.org](https://python.org) 
- Choose version 3.11 or newer
- During installation, check "Add Python to PATH"

### 2. Download the Application
- Save all the application files to a folder like `FleetManagement`
- Make sure you have all these files:
  ```
  FleetManagement/
  ├── app.py
  ├── pages/
  │   ├── 1_Vehicle_Inventory.py
  │   ├── 2_Maintenance_Records.py
  │   ├── 3_Dashboard.py
  │   └── 4_Tool_Hire.py
  ├── utils/
  │   ├── data_manager.py
  │   └── validators.py
  └── .streamlit/
      └── config.toml
  ```

### 3. Install Required Libraries (One-time setup)
Open Command Prompt or Terminal in your FleetManagement folder and run:
```bash
pip install streamlit pandas plotly
```

### 4. Run Your Fleet Management System
In the same folder, run:
```bash
streamlit run app.py
```

The system will start and open in your web browser at `http://localhost:8501`

## Daily Usage

1. **Start the application** - Run `streamlit run app.py`
2. **Use your browser** - Navigate to the local web address
3. **Manage your business** - Add vehicles, log maintenance, process rentals
4. **Stop when done** - Close browser and press Ctrl+C in terminal

## Backup Your Data

**Important**: Regularly backup your `data/` folder to:
- External USB drive
- Cloud storage (Dropbox, Google Drive, etc.)
- Another computer
- Email the CSV files to yourself

## Business Benefits of Offline Operation

### ✅ **Data Privacy & Security**
- Your sensitive business data never leaves your computer
- No cloud storage fees or privacy concerns
- Complete control over who can access your information

### ✅ **Reliability**
- Works without internet connection
- No downtime from server issues
- No monthly subscription fees

### ✅ **Speed**
- Instant response since everything runs locally
- No waiting for internet uploads/downloads
- Fast searches and reports

### ✅ **Cost Effective**
- No monthly software fees
- No per-user license costs
- No cloud storage charges

## Troubleshooting

### "Command not found" or "streamlit not recognized"
- Make sure Python is installed correctly
- Try `python -m streamlit run app.py` instead

### Data disappeared
- Check if the `data/` folder exists
- CSV files might be corrupted - restore from backup
- Restart the application

### Application won't start
- Check if another program is using port 8501
- Try closing and reopening Command Prompt/Terminal
- Make sure all files are in the correct locations

## Advanced Features

### Multi-Computer Setup
1. Copy the entire FleetManagement folder to another computer
2. Install Python and required libraries
3. Your data will be available on both computers
4. Manually sync the `data/` folder between computers as needed

### Network Access (Optional)
To access from other devices on your network:
1. Edit `.streamlit/config.toml`
2. Change `address = "0.0.0.0"`
3. Access from other devices using your computer's IP address

### Scheduled Backups
Set up automatic backups using:
- Windows Task Scheduler
- macOS Automator
- Linux cron jobs

## Support

For help with:
- **Technical issues**: Check Python and library installations
- **Business questions**: Refer to the application's built-in help
- **Data recovery**: Restore from your most recent backup

Remember: This system is designed to be simple and reliable for your business needs while keeping everything under your complete control.
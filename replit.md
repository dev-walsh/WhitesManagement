# Whites Management System

## Overview

The Whites Management System is a Streamlit-based web application designed for managing vehicle fleets, machinery inventory, tool rentals, and maintenance records. The system is built as a multi-page application with a centralized data management approach using CSV files for data persistence.

## User Preferences

Preferred communication style: Simple, everyday language.
UI Design: Modern, sleek dark theme with mobile-responsive design.
Color Scheme: Dark gradients with blue accents and professional styling.
Navigation: Single-page layout with tabs instead of sidebar navigation.
Export buttons: Blue gradient styling (#2196f3 to #1976d2) consistent across all sections.
Testing: Full CRUD operations testing with comprehensive validation before deployment.

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit web framework
- **UI Pattern**: Single-page application with tabbed navigation
- **Layout**: Wide layout with integrated tab-based navigation
- **Visualization**: Plotly for charts and graphs on dashboard and statistics pages
- **Design System**: Modern dark theme with gradient backgrounds and mobile-responsive design
- **Color Palette**: Dark blue gradients (#1a1a2e to #0f3460) with light blue accents (#2196f3)
- **Mobile Support**: Responsive design with optimized touch targets and mobile-first approach

### Backend Architecture
- **Data Layer**: CSV-based file storage system
- **Business Logic**: Centralized DataManager class for all data operations
- **Validation**: Input validation utilities for data integrity
- **Session Management**: Streamlit's built-in session state and caching

### Application Structure
The application follows a page-based architecture:
- Main application entry point (`app.py`)
- Individual pages in `/pages/` directory
- Shared utilities in `/utils/` directory
- Data storage in `/data/` directory (CSV files)

## Key Components

### Core Pages
1. **Vehicle Inventory** (`pages/1_Vehicle_Inventory.py`) - Road vehicle management
2. **Maintenance Records** (`pages/2_Maintenance_Records.py`) - Service and repair tracking
3. **Dashboard** (`pages/3_Dashboard.py`) - Visual overview with charts
4. **Tool Hire** (`pages/4_Tool_Hire.py`) - Equipment rental management
5. **Statistics** (`pages/5_Statistics.py`) - Analytics and reporting
6. **Machine Inventory** (`pages/6_Machine_Inventory.py`) - Plant machinery management

### Utility Modules
- **DataManager** (`utils/data_manager.py`) - Centralized data operations for all CSV files
- **Validators** (`utils/validators.py`) - Input validation functions for weights, years, and license plates

### Navigation System
- Consistent sidebar navigation across all pages
- Current page highlighting with disabled buttons
- Organized sections for different functional areas

## Data Flow

### Data Storage
The system uses a simple file-based approach:
- **vehicles.csv** - Road vehicle inventory
- **machines.csv** - Plant machinery inventory
- **maintenance.csv** - Maintenance and service records
- **equipment.csv** - Tool and equipment inventory
- **rentals.csv** - Rental transaction records

### Data Management Pattern
1. **Initialization**: DataManager ensures data directory and CSV files exist with proper headers
2. **Loading**: Data is loaded from CSV files using pandas
3. **Caching**: Streamlit's `@st.cache_resource` decorator caches the DataManager instance
4. **Persistence**: All changes are written back to CSV files immediately

### Validation Layer
Input validation occurs at the utility level:
- Weight validation (positive numbers in tonnes)
- Year validation (1900 to current year + 1)
- License plate validation (alphanumeric, 2-8 characters)

## External Dependencies

### Core Dependencies
- **streamlit** (≥1.28.0) - Web application framework
- **pandas** (≥2.0.0) - Data manipulation and CSV handling
- **plotly** (≥5.15.0) - Interactive charts and visualizations
- **xlsxwriter** (≥3.1.0) - Excel export functionality

### System Dependencies
- Python 3.11+ (based on error traces)
- File system access for CSV storage
- No external database requirements

## Deployment Strategy

### AWS Deployment Package
The repository includes a complete AWS deployment package (`aws-whitesaggs-admin/`) designed for EC2 deployment:

**Target Environment**:
- Domain: whitesaggs.com/admin (subdirectory routing)
- Platform: AWS EC2 with Ubuntu 22.04 LTS
- Web Server: Nginx reverse proxy
- SSL: Let's Encrypt automation

**Infrastructure Options**:
- CloudFormation templates for one-click deployment
- Terraform configurations for infrastructure as code
- Manual deployment scripts and documentation

**Security Considerations**:
- AWS Security Group configuration for web traffic
- SSH access restricted to specific IP ranges
- SSL certificate automation for HTTPS

**Backup Strategy**:
- Local CSV file backups
- Optional S3 integration for cloud backups
- Automated backup scheduling

### Local Development
The system is designed to run locally with minimal setup:
- Direct Streamlit execution (`streamlit run app.py`)
- Automatic CSV file and directory creation
- No database setup required

The architecture prioritizes simplicity and ease of deployment while maintaining data integrity through validation and proper file management. The AWS deployment package provides enterprise-ready hosting options with proper security and backup strategies.

## Recent Changes (July 16, 2025)

### Testing and Validation Complete
- **Full CRUD Operations Testing**: All Create, Read, Update, Delete operations tested with comprehensive fake data
- **Data Integrity**: Tested vehicles, machines, equipment, maintenance, and rental operations
- **Edge Case Testing**: Validated system behavior with missing fields, large datasets, and boundary conditions
- **Dynamic Data Reloading**: Fixed issue where new additions didn't appear immediately in UI
- **Equipment Categories**: Enhanced category options to include Construction, Power Tools, Access Equipment
- **Export Button Styling**: Fixed CSS specificity issues to ensure consistent blue gradient styling
- **System Info Cleanup**: Removed all system information messages and test data
- **Deployment Ready**: System cleaned and prepared for production deployment

### System Status
- All CRUD operations verified working correctly
- Data persistence confirmed across all modules
- CSV files properly initialized with headers
- UI responsiveness and styling consistent
- Export functionality fully operational
- Login system with 24-hour session timeout active
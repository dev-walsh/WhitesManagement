# Fleet Management System

## Overview

This is a comprehensive Streamlit-based Fleet Management System designed for complete business operations. The application manages vehicle inventory, maintenance records, and tool/equipment hire operations. All data is stored locally in CSV files, making it fully operational offline without any internet connection required.

## User Preferences

Preferred communication style: Simple, everyday language.
Business requirement: Complete offline operation for business use with tool hire functionality.

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit - chosen for rapid development of data-driven web applications
- **Multi-page Structure**: Uses Streamlit's native page system with a main app.py and separate page modules
- **Layout**: Wide layout with sidebar navigation for optimal data presentation
- **Visualization**: Plotly integration for interactive charts and graphs

### Backend Architecture
- **Data Layer**: CSV-based file storage system managed through a centralized DataManager class
- **Business Logic**: Utility modules for data validation and management operations
- **Session Management**: Streamlit's built-in caching system for performance optimization

### Data Storage
- **Primary Storage**: CSV files (vehicles.csv, maintenance.csv, equipment.csv, rentals.csv) stored in a local /data directory
- **Data Structure**: 
  - Vehicles: ID, Whites ID, make, model, year, weight, license plate, vehicle type, status (On Hire/Off Hire), mileage, defects, notes
  - Maintenance: ID, vehicle ID, date, type, description, cost (£), mileage, service provider, next due mileage
  - Equipment: ID, name, category, brand, model, serial number, daily rate (£), weekly rate (£), purchase price (£), status, notes
  - Rentals: ID, equipment ID, customer details, start/return dates, rental rate (£), deposit (£), status
- **Data Persistence**: File-based system with automatic directory and file creation

## Key Components

### 1. Main Application (app.py)
- **Purpose**: Entry point and dashboard overview
- **Features**: Quick statistics display, navigation hub
- **Caching**: Uses @st.cache_resource for DataManager singleton

### 2. Vehicle Inventory Management (pages/1_Vehicle_Inventory.py)
- **Purpose**: CRUD operations for vehicle records
- **Features**: Add vehicles, view inventory, search/filter functionality, import/export capabilities
- **Validation**: VIN and year validation through utility functions

### 3. Maintenance Records (pages/2_Maintenance_Records.py)
- **Purpose**: Track and manage vehicle maintenance activities
- **Features**: Log maintenance, view history, upcoming due dates, filtering options
- **Dependencies**: Requires existing vehicles before maintenance can be logged

### 4. Dashboard (pages/3_Dashboard.py)
- **Purpose**: Data visualization and analytics for both fleet and equipment
- **Features**: Key metrics display, interactive charts using Plotly
- **Analytics**: Fleet status overview, maintenance trends, equipment rental revenue, equipment utilization

### 5. Tool & Equipment Hire (pages/4_Tool_Hire.py)
- **Purpose**: Complete equipment rental management system
- **Features**: Equipment inventory, rental processing, customer management, return processing
- **Business Functions**: Daily/weekly rental rates, security deposits, equipment status tracking, overdue rental alerts

### 6. Data Management Layer (utils/data_manager.py)
- **Purpose**: Centralized data operations and CSV file management for all business functions
- **Features**: File creation, data loading/saving, directory management, equipment and rental operations
- **Data Files**: vehicles.csv, maintenance.csv, equipment.csv, rentals.csv
- **Error Handling**: Graceful handling of missing files and empty data scenarios

### 7. Validation Layer (utils/validators.py)
- **Purpose**: Data validation for vehicle and equipment information
- **Features**: Weight validation (tonnes), year validation, license plate validation, cost validation
- **Standards**: Customized for UK business requirements with £ currency

## Data Flow

1. **User Interaction**: Users interact through Streamlit web interface
2. **Data Validation**: Input validation occurs at the utility layer
3. **Data Processing**: DataManager handles all CSV file operations
4. **State Management**: Streamlit manages session state and caching
5. **Data Persistence**: All changes are immediately written to CSV files
6. **Visualization**: Dashboard pulls data for real-time analytics display

## External Dependencies

### Python Packages
- **streamlit**: Web application framework
- **pandas**: Data manipulation and analysis
- **plotly**: Interactive visualization library
- **datetime**: Date and time handling (built-in)
- **os/sys**: File system operations (built-in)
- **uuid**: Unique identifier generation (built-in)
- **re**: Regular expressions for validation (built-in)

### Data Dependencies
- Local file system access for CSV storage
- No external databases or APIs required
- **Offline Operation**: Complete functionality without internet connection

## Deployment Strategy

### Current Architecture
- **Type**: Single-machine deployment suitable for small to medium fleets
- **Storage**: Local file system with CSV files
- **Scalability**: Limited by single-machine resources and file-based storage

### Deployment Considerations
- Requires Python environment with Streamlit
- Data directory must be writable for CSV file operations
- Session state is maintained per user session
- No authentication or multi-user management implemented

### Future Scalability Options
- Database migration path available (structure supports SQL database integration)
- Multi-user authentication can be added
- Cloud deployment possible with data migration strategy
- API layer can be introduced for external integrations

### Performance Characteristics
- **Strengths**: Simple setup, no database overhead, fast for small datasets
- **Limitations**: File locking issues with concurrent users, limited query capabilities
- **Optimization**: Pandas caching reduces file read operations

## Recent Updates (July 2025)

### UI/UX Improvements
- **Enhanced Styling**: Added professional CSS styling across all pages with consistent color scheme (#1f77b4)
- **Improved Typography**: Better font spacing, sizing, and hierarchy with centered headers
- **Card-Based Layout**: Implemented card-based design for vehicles, equipment, and maintenance records
- **Section Headers**: Added styled section headers with bottom borders for better visual separation
- **Status Badges**: Color-coded status indicators for vehicles, equipment, and maintenance priorities
- **Form Styling**: Enhanced form sections with background colors and rounded corners
- **Responsive Design**: Improved spacing and layout for better user experience
- **Visual Hierarchy**: Clear distinction between headers, sub-headers, and content sections
- **Professional Color Scheme**: 
  - Primary: #1f77b4 (Blue)
  - Success: #28a745 (Green)
  - Warning: #ffc107 (Yellow)
  - Danger: #dc3545 (Red)
  - Info: #17a2b8 (Cyan)

### Enhanced User Experience
- **Consistent Navigation**: Standardized sidebar navigation across all pages
- **Better Data Formatting**: Currency formatting for all financial fields (£)
- **Improved Filtering**: Enhanced filter sections with card-based styling
- **Visual Feedback**: Better visual cues for different states and actions
- **Professional Appearance**: Overall more polished and business-ready interface
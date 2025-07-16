import streamlit as st
import pandas as pd
from datetime import datetime, date
import os
from utils.data_manager import DataManager
from login import check_password, show_logout_button, get_current_user

# Configure the page
st.set_page_config(
    page_title="Whites Management",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize data manager
@st.cache_resource
def get_data_manager():
    return DataManager()

def create_sidebar(vehicles_df, maintenance_df, equipment_df, rentals_df):
    """Create modern dark sidebar with sleek navigation and export options"""
    with st.sidebar:
        # Modern sidebar CSS
        st.markdown("""
        <style>
        .sidebar-header {
            background: linear-gradient(135deg, #2196f3 0%, #1976d2 100%);
            color: white;
            padding: 1.5rem;
            border-radius: 12px;
            text-align: center;
            margin-bottom: 2rem;
            font-size: 1.5rem;
            font-weight: 700;
            box-shadow: 0 8px 32px rgba(33, 150, 243, 0.3);
        }
        
        .nav-section {
            background: rgba(255, 255, 255, 0.03);
            border-radius: 12px;
            padding: 1.5rem;
            margin: 1rem 0;
            border: 1px solid rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
        }
        
        .nav-title {
            color: #64b5f6;
            font-size: 1.1rem;
            font-weight: 600;
            margin-bottom: 1rem;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid #2196f3;
        }
        
        .current-user {
            background: rgba(255, 255, 255, 0.02);
            color: #e0e6ed;
            padding: 1rem;
            border-radius: 8px;
            margin-bottom: 1rem;
            border: 1px solid rgba(255, 255, 255, 0.1);
            text-align: center;
            font-size: 0.9rem;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Sidebar Header
        st.markdown('<div class="sidebar-header">🚗 Whites Management</div>', unsafe_allow_html=True)
        
        # Current User Display
        current_user = get_current_user()
        if current_user:
            st.markdown(f'<div class="current-user">👤 Welcome, {current_user}</div>', unsafe_allow_html=True)
        
        # Navigation Section
        st.markdown('<div class="nav-section">', unsafe_allow_html=True)
        st.markdown('<div class="nav-title">📍 Navigation</div>', unsafe_allow_html=True)
        
        # Main Navigation
        if st.button("🚗 Vehicle Inventory", use_container_width=True):
            st.switch_page("pages/1_Vehicle_Inventory.py")
        if st.button("🏗️ Machine Inventory", use_container_width=True):
            st.switch_page("pages/6_Machine_Inventory.py")
        if st.button("⚙️ Tool Hire", use_container_width=True):
            st.switch_page("pages/4_Tool_Hire.py")
        if st.button("📊 Dashboard", use_container_width=True):
            st.switch_page("pages/3_Dashboard.py")
        if st.button("📈 Statistics", use_container_width=True):
            st.switch_page("pages/5_Statistics.py")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Maintenance & Reports Section
        st.markdown('<div class="nav-section">', unsafe_allow_html=True)
        st.markdown('<div class="nav-title">🔧 Maintenance & Records</div>', unsafe_allow_html=True)
        if st.button("🔧 Maintenance Records", use_container_width=True):
            st.switch_page("pages/2_Maintenance_Records.py")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Home Section
        st.markdown('<div class="nav-section">', unsafe_allow_html=True)
        st.markdown('<div class="nav-title">🏠 Home</div>', unsafe_allow_html=True)
        if st.button("🏠 Home", use_container_width=True):
            st.switch_page("app.py")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Export Section
        st.markdown("### 📥 Export Data")
        
        # Create Excel export functions
        def create_excel_export(dataframes, filename):
            import io
            import pandas as pd
            
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                for sheet_name, df in dataframes.items():
                    if not df.empty:
                        df.to_excel(writer, sheet_name=sheet_name, index=False)
            
            return output.getvalue()
        
        # Individual CSV exports
        st.markdown("**CSV Format**")
        
        if not vehicles_df.empty:
            csv_vehicles = vehicles_df.to_csv(index=False)
            st.download_button(
                label="🚗 Vehicles CSV",
                data=csv_vehicles,
                file_name=f"vehicles_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        if not maintenance_df.empty:
            csv_maintenance = maintenance_df.to_csv(index=False)
            st.download_button(
                label="🔧 Maintenance CSV",
                data=csv_maintenance,
                file_name=f"maintenance_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        if not equipment_df.empty:
            csv_equipment = equipment_df.to_csv(index=False)
            st.download_button(
                label="⚙️ Equipment CSV",
                data=csv_equipment,
                file_name=f"equipment_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        if not rentals_df.empty:
            csv_rentals = rentals_df.to_csv(index=False)
            st.download_button(
                label="💰 Rentals CSV",
                data=csv_rentals,
                file_name=f"rentals_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        # Excel exports
        st.markdown("**Excel Format**")
        
        # Individual Excel exports
        if not vehicles_df.empty:
            excel_vehicles = create_excel_export({"Vehicles": vehicles_df}, "vehicles.xlsx")
            st.download_button(
                label="🚗 Vehicles Excel",
                data=excel_vehicles,
                file_name=f"vehicles_{datetime.now().strftime('%Y%m%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
        
        if not maintenance_df.empty:
            excel_maintenance = create_excel_export({"Maintenance": maintenance_df}, "maintenance.xlsx")
            st.download_button(
                label="🔧 Maintenance Excel",
                data=excel_maintenance,
                file_name=f"maintenance_{datetime.now().strftime('%Y%m%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
        
        if not equipment_df.empty:
            excel_equipment = create_excel_export({"Equipment": equipment_df}, "equipment.xlsx")
            st.download_button(
                label="⚙️ Equipment Excel",
                data=excel_equipment,
                file_name=f"equipment_{datetime.now().strftime('%Y%m%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
        
        if not rentals_df.empty:
            excel_rentals = create_excel_export({"Rentals": rentals_df}, "rentals.xlsx")
            st.download_button(
                label="💰 Rentals Excel",
                data=excel_rentals,
                file_name=f"rentals_{datetime.now().strftime('%Y%m%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
        
        # Combined exports
        st.markdown("**Combined Exports**")
        
        if not (vehicles_df.empty and maintenance_df.empty and equipment_df.empty and rentals_df.empty):
            # All data Excel export
            all_data = {}
            if not vehicles_df.empty:
                all_data["Vehicles"] = vehicles_df
            if not maintenance_df.empty:
                all_data["Maintenance"] = maintenance_df
            if not equipment_df.empty:
                all_data["Equipment"] = equipment_df
            if not rentals_df.empty:
                all_data["Rentals"] = rentals_df
            
            excel_all = create_excel_export(all_data, "whites_data.xlsx")
            st.download_button(
                label="📊 All Data Excel",
                data=excel_all,
                file_name=f"whites_data_{datetime.now().strftime('%Y%m%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
            
            # ZIP export
            import zipfile
            import io
            
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                if not vehicles_df.empty:
                    zip_file.writestr(f"vehicles_{datetime.now().strftime('%Y%m%d')}.csv", vehicles_df.to_csv(index=False))
                if not maintenance_df.empty:
                    zip_file.writestr(f"maintenance_{datetime.now().strftime('%Y%m%d')}.csv", maintenance_df.to_csv(index=False))
                if not equipment_df.empty:
                    zip_file.writestr(f"equipment_{datetime.now().strftime('%Y%m%d')}.csv", equipment_df.to_csv(index=False))
                if not rentals_df.empty:
                    zip_file.writestr(f"rentals_{datetime.now().strftime('%Y%m%d')}.csv", rentals_df.to_csv(index=False))
            
            st.download_button(
                label="📦 All Data ZIP",
                data=zip_buffer.getvalue(),
                file_name=f"whites_data_{datetime.now().strftime('%Y%m%d')}.zip",
                mime="application/zip",
                use_container_width=True
            )
        
        # Export Section
        st.markdown('<div class="nav-section">', unsafe_allow_html=True)
        st.markdown('<div class="nav-title">📥 Export Data</div>', unsafe_allow_html=True)
        
        # Create Excel export functions
        def create_excel_export(dataframes, filename):
            import io
            import pandas as pd
            
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                for sheet_name, df in dataframes.items():
                    if not df.empty:
                        df.to_excel(writer, sheet_name=sheet_name, index=False)
            
            return output.getvalue()
        
        # Quick export buttons
        if not vehicles_df.empty:
            excel_vehicles = create_excel_export({"Vehicles": vehicles_df}, "vehicles.xlsx")
            st.download_button(
                label="🚗 Vehicles Excel",
                data=excel_vehicles,
                file_name=f"vehicles_{datetime.now().strftime('%Y%m%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
        
        if not equipment_df.empty:
            excel_equipment = create_excel_export({"Equipment": equipment_df}, "equipment.xlsx")
            st.download_button(
                label="⚙️ Equipment Excel",
                data=excel_equipment,
                file_name=f"equipment_{datetime.now().strftime('%Y%m%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # System Info Section
        st.markdown('<div class="nav-section">', unsafe_allow_html=True)
        st.markdown('<div class="nav-title">💡 System Info</div>', unsafe_allow_html=True)
        st.info("Offline system using local CSV files. No internet required!")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Logout Section
        st.markdown('<div class="nav-section">', unsafe_allow_html=True)
        show_logout_button()
        st.markdown('</div>', unsafe_allow_html=True)

def main():
    # Check authentication first
    if not check_password():
        st.stop()
    
    # Modern Dark Theme CSS with Mobile Responsiveness
    st.markdown("""
    <style>
    /* Global Styles */
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        color: #e0e6ed;
        min-height: 100vh;
    }
    
    /* Mobile-First Responsive Design */
    @media (max-width: 768px) {
        .stApp {
            padding: 0.5rem;
        }
        
        .main-header {
            font-size: 2rem !important;
            padding: 1rem 0 !important;
        }
        
        .sub-header {
            font-size: 1rem !important;
            margin-bottom: 1.5rem !important;
        }
        
        .section-header {
            font-size: 1.4rem !important;
            margin: 1.5rem 0 1rem 0 !important;
        }
        
        .metric-card {
            padding: 1rem !important;
            margin: 0.25rem 0 !important;
        }
        
        .nav-section {
            padding: 1rem !important;
            margin: 0.5rem 0 !important;
        }
        
        .sidebar-header {
            padding: 1rem !important;
            font-size: 1.2rem !important;
        }
    }
    
    /* Main Header */
    .main-header {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #64b5f6 0%, #42a5f5 50%, #2196f3 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 0.5rem;
        padding: 1.5rem 0;
        text-shadow: 0 0 20px rgba(33, 150, 243, 0.3);
        transition: all 0.3s ease;
    }
    
    .sub-header {
        font-size: 1.3rem;
        color: #b0bec5;
        text-align: center;
        margin-bottom: 2.5rem;
        font-weight: 300;
        letter-spacing: 0.5px;
        transition: all 0.3s ease;
    }
    /* Metrics Cards */
    .metric-card {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        border-color: rgba(33, 150, 243, 0.3);
        box-shadow: 0 4px 20px rgba(33, 150, 243, 0.1);
    }
    
    /* Section Headers */
    .section-header {
        font-size: 1.8rem;
        font-weight: 700;
        color: #e0e6ed;
        margin: 2.5rem 0 1.5rem 0;
        padding: 1rem 0;
        border-bottom: 3px solid #2196f3;
        background: linear-gradient(90deg, rgba(33, 150, 243, 0.1) 0%, transparent 100%);
        border-radius: 8px 0 0 8px;
        padding-left: 1rem;
    }
    
    /* Quick Action Buttons */
    .quick-action-btn {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        text-align: center;
        transition: all 0.3s ease;
        color: #e0e6ed;
        cursor: pointer;
    }
    
    .quick-action-btn:hover {
        transform: translateY(-2px);
        border-color: rgba(33, 150, 243, 0.4);
        background: rgba(33, 150, 243, 0.1);
        box-shadow: 0 8px 24px rgba(33, 150, 243, 0.15);
    }
    
    /* Data Tables */
    .data-table {
        background: rgba(255, 255, 255, 0.02);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1.5rem 0;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
    }
    
    /* Streamlit Metrics Override */
    .stMetric {
        background: rgba(255, 255, 255, 0.03) !important;
        border-radius: 12px !important;
        padding: 1.5rem !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(10px) !important;
        transition: all 0.3s ease !important;
    }
    
    .stMetric:hover {
        transform: translateY(-2px) !important;
        border-color: rgba(33, 150, 243, 0.3) !important;
        box-shadow: 0 4px 20px rgba(33, 150, 243, 0.1) !important;
    }
    
    .stMetric > div {
        color: #e0e6ed !important;
    }
    
    .stMetric [data-testid="metric-container"] {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }
    
    /* Mobile-responsive metrics */
    @media (max-width: 768px) {
        .stMetric {
            padding: 1rem !important;
            margin: 0.5rem 0 !important;
        }
    }
    
    /* Sidebar Styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%) !important;
    }
    
    .css-1d391kg .css-17eq0hr {
        color: #e0e6ed !important;
    }
    
    /* Mobile sidebar adjustments */
    @media (max-width: 768px) {
        .css-1d391kg {
            width: 100% !important;
            max-width: 100% !important;
        }
    }
    
    /* Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, #2196f3 0%, #1976d2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 16px rgba(33, 150, 243, 0.3) !important;
        width: 100% !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 24px rgba(33, 150, 243, 0.4) !important;
    }
    
    /* Mobile button adjustments */
    @media (max-width: 768px) {
        .stButton > button {
            padding: 0.875rem 1rem !important;
            font-size: 0.9rem !important;
        }
    }
    
    /* Input Styling */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 8px !important;
        color: #e0e6ed !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #2196f3 !important;
        box-shadow: 0 0 0 2px rgba(33, 150, 243, 0.2) !important;
    }
    
    .stSelectbox > div > div > div {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 8px !important;
        color: #e0e6ed !important;
        transition: all 0.3s ease !important;
    }
    
    /* Mobile input adjustments */
    @media (max-width: 768px) {
        .stTextInput > div > div > input,
        .stSelectbox > div > div > div {
            padding: 0.75rem !important;
            font-size: 1rem !important;
        }
    }
    
    /* Data table responsiveness */
    .dataframe {
        font-size: 0.9rem !important;
    }
    
    @media (max-width: 768px) {
        .dataframe {
            font-size: 0.8rem !important;
        }
        
        .dataframe th, .dataframe td {
            padding: 0.5rem !important;
        }
    }
    
    /* Column layout adjustments for mobile */
    @media (max-width: 768px) {
        .stColumn {
            padding: 0.25rem !important;
        }
    }
    
    /* Progress bars and other components */
    .stProgress > div > div {
        background: linear-gradient(135deg, #2196f3 0%, #1976d2 100%) !important;
        border-radius: 8px !important;
    }
    
    /* Toast notifications */
    .stToast {
        background: rgba(38, 50, 56, 0.95) !important;
        border: 1px solid #546e7a !important;
        border-radius: 8px !important;
        color: #e0e6ed !important;
        backdrop-filter: blur(10px) !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="main-header">🚗 Whites Management</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Complete vehicle, maintenance, and equipment management solution</div>', unsafe_allow_html=True)
    
    # Initialize data manager
    dm = get_data_manager()
    
    # Quick stats overview with improved spacing
    st.markdown('<div class="section-header">📊 System Overview</div>', unsafe_allow_html=True)
    col1, col2, col3, col4, col5 = st.columns(5)
    
    vehicles_df = dm.load_vehicles()
    maintenance_df = dm.load_maintenance()
    equipment_df = dm.load_equipment()
    rentals_df = dm.load_rentals()
    
    with col1:
        st.metric("Total Vehicles", len(vehicles_df))
    
    with col2:
        on_hire_vehicles = len(vehicles_df[vehicles_df['status'] == 'On Hire']) if not vehicles_df.empty else 0
        st.metric("On Hire Vehicles", on_hire_vehicles)
    
    with col3:
        total_equipment = len(equipment_df)
        st.metric("Total Equipment", total_equipment)
    
    with col4:
        active_rentals = len(rentals_df[rentals_df['status'] == 'Active']) if not rentals_df.empty else 0
        st.metric("Active Rentals", active_rentals)
    
    with col5:
        if not rentals_df.empty:
            rental_revenue = rentals_df['rental_rate'].sum()
            st.metric("Total Rental Revenue", f"£{rental_revenue:,.2f}")
        else:
            st.metric("Total Rental Revenue", "£0.00")
    
    st.markdown("")
    
    # Quick actions with improved styling
    st.markdown('<div class="section-header">🚀 Quick Actions</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("➕ Add New Vehicle", use_container_width=True):
            st.switch_page("pages/1_Vehicle_Inventory.py")
    
    with col2:
        if st.button("🔧 Log Maintenance", use_container_width=True):
            st.switch_page("pages/2_Maintenance_Records.py")
    
    with col3:
        if st.button("🔧 Add Equipment", use_container_width=True):
            st.switch_page("pages/4_Tool_Hire.py")
    
    with col4:
        if st.button("📊 View Dashboard", use_container_width=True):
            st.switch_page("pages/3_Dashboard.py")
    
    st.markdown("")
    
    # Recent activity with improved styling
    st.markdown('<div class="section-header">📊 Recent Activity</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📋 Recent Maintenance")
        if not maintenance_df.empty:
            recent_maintenance = maintenance_df.sort_values('date', ascending=False).head(5)
            # Format cost column for display
            display_maintenance = recent_maintenance[['vehicle_id', 'date', 'type', 'cost']].copy()
            display_maintenance['cost'] = display_maintenance['cost'].apply(lambda x: f"£{x:,.2f}")
            st.dataframe(
                display_maintenance,
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("No maintenance records found.")
    
    with col2:
        st.markdown("### 🔧 Recent Rentals")
        if not rentals_df.empty:
            recent_rentals = rentals_df.sort_values('start_date', ascending=False).head(5)
            # Merge with equipment names
            if not equipment_df.empty:
                recent_rentals = recent_rentals.merge(
                    equipment_df[['equipment_id', 'name']], 
                    on='equipment_id', 
                    how='left'
                )
                display_rentals = recent_rentals[['customer_name', 'name', 'start_date', 'rental_rate']].copy()
                display_rentals['rental_rate'] = display_rentals['rental_rate'].apply(lambda x: f"£{x:,.2f}")
                st.dataframe(
                    display_rentals,
                    use_container_width=True,
                    hide_index=True
                )
            else:
                display_rentals = recent_rentals[['customer_name', 'start_date', 'rental_rate']].copy()
                display_rentals['rental_rate'] = display_rentals['rental_rate'].apply(lambda x: f"£{x:,.2f}")
                st.dataframe(
                    display_rentals,
                    use_container_width=True,
                    hide_index=True
                )
        else:
            st.info("No rental records found.")
    
    # Create permanent sidebar navigation
    create_sidebar(vehicles_df, maintenance_df, equipment_df, rentals_df)

if __name__ == "__main__":
    main()

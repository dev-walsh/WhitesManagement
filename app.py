import streamlit as st
import pandas as pd
from datetime import datetime, date
import os
from utils.data_manager import DataManager

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
    """Create permanent sidebar with organized navigation and export options"""
    with st.sidebar:
        st.title("🚗 Whites Management")
        
        # Navigation Section
        st.markdown("### 📍 Navigation")
        
        # Fleet Management
        st.markdown("**Fleet Management**")
        if st.button("🚗 Vehicle Inventory", use_container_width=True):
            st.switch_page("pages/1_Vehicle_Inventory.py")
        if st.button("🔧 Maintenance Records", use_container_width=True):
            st.switch_page("pages/2_Maintenance_Records.py")
        
        # Equipment & Rentals
        st.markdown("**Equipment & Rentals**")
        if st.button("⚙️ Equipment Hire", use_container_width=True):
            st.switch_page("pages/4_Tool_Hire.py")
        
        # Analytics & Reports
        st.markdown("**Analytics & Reports**")
        if st.button("📊 Dashboard", use_container_width=True):
            st.switch_page("pages/3_Dashboard.py")
        if st.button("📈 Statistics", use_container_width=True):
            st.switch_page("pages/5_Statistics.py")
        
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
        
        st.markdown("---")
        st.markdown("### 💡 System Info")
        st.info("Offline system using local CSV files. No internet required!")

def main():
    # Custom CSS for improved UI
    st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 0.5rem;
        padding: 1rem 0;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 400;
    }
    .metric-card {
        background: #f8f9fa;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 4px solid #1f77b4;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .section-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #333;
        margin: 2rem 0 1rem 0;
        border-bottom: 2px solid #1f77b4;
        padding-bottom: 0.5rem;
    }
    .quick-action-btn {
        background: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        text-align: center;
        transition: all 0.2s ease;
    }
    .quick-action-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    .data-table {
        background: white;
        border-radius: 8px;
        padding: 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    .stMetric {
        background: #f8f9fa;
        border-radius: 8px;
        padding: 1rem;
        border-left: 4px solid #1f77b4;
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

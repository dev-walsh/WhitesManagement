import streamlit as st
import pandas as pd
from datetime import datetime, date
import os
from utils.data_manager import DataManager

# Configure the page
st.set_page_config(
    page_title="Fleet Management System",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize data manager
@st.cache_resource
def get_data_manager():
    return DataManager()

def main():
    st.title("🚗 Fleet Management System")
    st.markdown("### Welcome to your Vehicle Inventory and Maintenance Tracking Tool")
    
    # Initialize data manager
    dm = get_data_manager()
    
    # Quick stats overview
    col1, col2, col3, col4 = st.columns(4)
    
    vehicles_df = dm.load_vehicles()
    maintenance_df = dm.load_maintenance()
    
    with col1:
        st.metric("Total Vehicles", len(vehicles_df))
    
    with col2:
        active_vehicles = len(vehicles_df[vehicles_df['status'] == 'Active']) if not vehicles_df.empty else 0
        st.metric("Active Vehicles", active_vehicles)
    
    with col3:
        if not maintenance_df.empty:
            recent_maintenance = len(maintenance_df[
                pd.to_datetime(maintenance_df['date']) >= pd.Timestamp.now() - pd.Timedelta(days=30)
            ])
        else:
            recent_maintenance = 0
        st.metric("Maintenance (Last 30 Days)", recent_maintenance)
    
    with col4:
        if not maintenance_df.empty:
            total_cost = maintenance_df['cost'].sum()
            st.metric("Total Maintenance Cost", f"${total_cost:,.2f}")
        else:
            st.metric("Total Maintenance Cost", "$0.00")
    
    st.markdown("---")
    
    # Quick actions
    st.subheader("🚀 Quick Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("➕ Add New Vehicle", use_container_width=True):
            st.switch_page("pages/1_Vehicle_Inventory.py")
    
    with col2:
        if st.button("🔧 Log Maintenance", use_container_width=True):
            st.switch_page("pages/2_Maintenance_Records.py")
    
    with col3:
        if st.button("📊 View Dashboard", use_container_width=True):
            st.switch_page("pages/3_Dashboard.py")
    
    st.markdown("---")
    
    # Recent activity
    st.subheader("📋 Recent Activity")
    
    if not maintenance_df.empty:
        recent_maintenance = maintenance_df.sort_values('date', ascending=False).head(5)
        st.dataframe(
            recent_maintenance[['vehicle_id', 'date', 'type', 'description', 'cost']],
            use_container_width=True
        )
    else:
        st.info("No maintenance records found. Start by adding vehicles and logging maintenance activities.")
    
    # Navigation sidebar
    with st.sidebar:
        st.title("Navigation")
        st.markdown("Use the pages in the sidebar to:")
        st.markdown("- **Vehicle Inventory**: Manage your fleet")
        st.markdown("- **Maintenance Records**: Track service history")
        st.markdown("- **Dashboard**: View analytics and reports")
        
        st.markdown("---")
        st.markdown("### Data Management")
        
        # Export all data
        if st.button("📥 Export All Data"):
            # Create a simple CSV export of all data
            if not vehicles_df.empty:
                csv_vehicles = vehicles_df.to_csv(index=False)
                st.download_button(
                    label="Download Vehicles CSV",
                    data=csv_vehicles,
                    file_name=f"vehicles_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
            
            if not maintenance_df.empty:
                csv_maintenance = maintenance_df.to_csv(index=False)
                st.download_button(
                    label="Download Maintenance CSV",
                    data=csv_maintenance,
                    file_name=f"maintenance_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )

if __name__ == "__main__":
    main()

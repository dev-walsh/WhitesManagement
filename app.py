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
    
    st.markdown("---")
    
    # Quick actions
    st.subheader("🚀 Quick Actions")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("➕ Add New Vehicle", use_container_width=True):
            st.info("Navigate to 'Vehicle Inventory' page using the sidebar menu")
    
    with col2:
        if st.button("🔧 Log Maintenance", use_container_width=True):
            st.info("Navigate to 'Maintenance Records' page using the sidebar menu")
    
    with col3:
        if st.button("🔧 Add Equipment", use_container_width=True):
            st.info("Navigate to 'Tool Hire' page using the sidebar menu")
    
    with col4:
        if st.button("📊 View Dashboard", use_container_width=True):
            st.info("Navigate to 'Dashboard' page using the sidebar menu")
    
    st.markdown("---")
    
    # Recent activity
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📋 Recent Maintenance")
        if not maintenance_df.empty:
            recent_maintenance = maintenance_df.sort_values('date', ascending=False).head(5)
            st.dataframe(
                recent_maintenance[['vehicle_id', 'date', 'type', 'cost']],
                use_container_width=True
            )
        else:
            st.info("No maintenance records found.")
    
    with col2:
        st.subheader("🔧 Recent Rentals")
        if not rentals_df.empty:
            recent_rentals = rentals_df.sort_values('start_date', ascending=False).head(5)
            # Merge with equipment names
            if not equipment_df.empty:
                recent_rentals = recent_rentals.merge(
                    equipment_df[['equipment_id', 'name']], 
                    on='equipment_id', 
                    how='left'
                )
            st.dataframe(
                recent_rentals[['customer_name', 'name', 'start_date', 'rental_rate']],
                use_container_width=True
            )
        else:
            st.info("No rental records found.")
    
    # Navigation sidebar
    with st.sidebar:
        st.title("Navigation")
        st.markdown("Use the pages in the sidebar to:")
        st.markdown("- **Vehicle Inventory**: Manage your fleet")
        st.markdown("- **Maintenance Records**: Track service history")
        st.markdown("- **Dashboard**: View analytics and reports")
        st.markdown("- **Tool Hire**: Manage equipment rentals")
        
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
            
            if not equipment_df.empty:
                csv_equipment = equipment_df.to_csv(index=False)
                st.download_button(
                    label="Download Equipment CSV",
                    data=csv_equipment,
                    file_name=f"equipment_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
            
            if not rentals_df.empty:
                csv_rentals = rentals_df.to_csv(index=False)
                st.download_button(
                    label="Download Rentals CSV",
                    data=csv_rentals,
                    file_name=f"rentals_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
        
        st.markdown("---")
        st.markdown("### 💡 Offline Mode")
        st.info("This system works completely offline using local CSV files. No internet connection required!")

if __name__ == "__main__":
    main()

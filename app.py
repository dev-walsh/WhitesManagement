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
    
    st.markdown('<div class="main-header">🚗 Fleet Management System</div>', unsafe_allow_html=True)
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

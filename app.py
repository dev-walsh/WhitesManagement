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
    initial_sidebar_state="collapsed"
)

# Initialize data manager
@st.cache_resource
def get_data_manager():
    return DataManager()

def create_horizontal_nav(current_page="Home"):
    """Create horizontal navigation menu at the top of the page"""
    st.markdown("""
    <style>
    .nav-container {
        background: linear-gradient(90deg, #1f77b4, #2c8fd4);
        padding: 0.75rem 1rem;
        border-radius: 8px;
        margin-bottom: 2rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .nav-title {
        color: white;
        font-size: 1.5rem;
        font-weight: 700;
        margin: 0;
        padding: 0;
    }
    .nav-buttons {
        display: flex;
        gap: 0.5rem;
        align-items: center;
        flex-wrap: wrap;
        margin-top: 1rem;
    }
    .nav-button {
        background: rgba(255,255,255,0.2);
        border: 1px solid rgba(255,255,255,0.3);
        color: white;
        padding: 0.4rem 0.8rem;
        border-radius: 5px;
        text-decoration: none;
        font-weight: 500;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    .nav-button:hover {
        background: rgba(255,255,255,0.3);
        transform: translateY(-1px);
    }
    .nav-button.active {
        background: white;
        color: #1f77b4;
        font-weight: 600;
    }
    </style>
    """, unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="nav-container">', unsafe_allow_html=True)
        st.markdown('<h1 class="nav-title">🚗 Whites Management</h1>', unsafe_allow_html=True)
        
        col1, col2, col3, col4, col5, col6, col7 = st.columns([1,1,1,1,1,1,1])
        
        with col1:
            if current_page == "Home":
                st.button("🏠 Home", key="nav_home", disabled=True, use_container_width=True)
            else:
                if st.button("🏠 Home", key="nav_home", use_container_width=True):
                    st.rerun()
        
        with col2:
            if current_page == "Vehicle Inventory":
                st.button("🚗 Vehicles", key="nav_vehicles", disabled=True, use_container_width=True)
            else:
                if st.button("🚗 Vehicles", key="nav_vehicles", use_container_width=True):
                    st.switch_page("pages/1_Vehicle_Inventory.py")
        
        with col3:
            if current_page == "Machine Inventory":
                st.button("🏗️ Machines", key="nav_machines", disabled=True, use_container_width=True)
            else:
                if st.button("🏗️ Machines", key="nav_machines", use_container_width=True):
                    st.switch_page("pages/6_Machine_Inventory.py")
        
        with col4:
            if current_page == "Tool Hire":
                st.button("⚙️ Tool Hire", key="nav_tools", disabled=True, use_container_width=True)
            else:
                if st.button("⚙️ Tool Hire", key="nav_tools", use_container_width=True):
                    st.switch_page("pages/4_Tool_Hire.py")
        
        with col5:
            if current_page == "Dashboard":
                st.button("📊 Dashboard", key="nav_dashboard", disabled=True, use_container_width=True)
            else:
                if st.button("📊 Dashboard", key="nav_dashboard", use_container_width=True):
                    st.switch_page("pages/3_Dashboard.py")
        
        with col6:
            if current_page == "Statistics":
                st.button("📈 Statistics", key="nav_stats", disabled=True, use_container_width=True)
            else:
                if st.button("📈 Statistics", key="nav_stats", use_container_width=True):
                    st.switch_page("pages/5_Statistics.py")
        
        with col7:
            if current_page == "Maintenance":
                st.button("🔧 Maintenance", key="nav_maintenance", disabled=True, use_container_width=True)
            else:
                if st.button("🔧 Maintenance", key="nav_maintenance", use_container_width=True):
                    st.switch_page("pages/2_Maintenance_Records.py")
        
        st.markdown('</div>', unsafe_allow_html=True)

def main():
    # Custom CSS for improved UI
    st.markdown("""
    <style>
    /* Keep sidebar collapsed but functional */
    section[data-testid="stSidebar"] {
        width: 0px;
        min-width: 0px;
        max-width: 0px;
    }
    section[data-testid="stSidebar"] > div {
        width: 0px;
        min-width: 0px;
        max-width: 0px;
        padding: 0px;
    }
    /* Adjust main content area */
    .main .block-container {
        padding-left: 2rem;
        padding-right: 2rem;
        max-width: none;
    }
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
    
    # Create horizontal navigation
    create_horizontal_nav("Home")
    
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

if __name__ == "__main__":
    main()

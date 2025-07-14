import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date, timedelta
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.data_manager import DataManager

st.set_page_config(
    page_title="Dashboard", 
    page_icon="📊", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize data manager
@st.cache_resource
def get_data_manager():
    return DataManager()

def create_horizontal_nav(current_page="Dashboard"):
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
                    st.info("🏠 Please use the sidebar navigation to go to the Home page.")
        
        with col2:
            if current_page == "Vehicle Inventory":
                st.button("🚗 Vehicles", key="nav_vehicles", disabled=True, use_container_width=True)
            else:
                if st.button("🚗 Vehicles", key="nav_vehicles", use_container_width=True):
                    st.info("🚗 Please use the sidebar navigation to go to the Vehicle Inventory page.")
        
        with col3:
            if current_page == "Machine Inventory":
                st.button("🏗️ Machines", key="nav_machines", disabled=True, use_container_width=True)
            else:
                if st.button("🏗️ Machines", key="nav_machines", use_container_width=True):
                    st.info("🏗️ Please use the sidebar navigation to go to the Machine Inventory page.")
        
        with col4:
            if current_page == "Tool Hire":
                st.button("⚙️ Tool Hire", key="nav_tools", disabled=True, use_container_width=True)
            else:
                if st.button("⚙️ Tool Hire", key="nav_tools", use_container_width=True):
                    st.info("⚙️ Please use the sidebar navigation to go to the Tool Hire page.")
        
        with col5:
            if current_page == "Dashboard":
                st.button("📊 Dashboard", key="nav_dashboard", disabled=True, use_container_width=True)
            else:
                if st.button("📊 Dashboard", key="nav_dashboard", use_container_width=True):
                    st.info("📊 Please use the sidebar navigation to go to the Dashboard page.")
        
        with col6:
            if current_page == "Statistics":
                st.button("📈 Statistics", key="nav_stats", disabled=True, use_container_width=True)
            else:
                if st.button("📈 Statistics", key="nav_stats", use_container_width=True):
                    st.info("📈 Please use the sidebar navigation to go to the Statistics page.")
        
        with col7:
            if current_page == "Maintenance":
                st.button("🔧 Maintenance", key="nav_maintenance", disabled=True, use_container_width=True)
            else:
                if st.button("🔧 Maintenance", key="nav_maintenance", use_container_width=True):
                    st.info("🔧 Please use the sidebar navigation to go to the Maintenance Records page.")
        
        st.markdown('</div>', unsafe_allow_html=True)

def main():
    # Custom CSS for dashboard styling
    st.markdown("""
    <style>
    /* Hide sidebar completely */
    .css-1d391kg, .css-1rs6os, .stSidebar {
        display: none !important;
    }
    section[data-testid="stSidebar"] {
        display: none !important;
    }
    .css-1y4p8pa {
        display: none !important;
    }
    /* Adjust main content area */
    .main .block-container {
        padding-left: 2rem;
        padding-right: 2rem;
        max-width: none;
    }
    .dashboard-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f77b4;
        margin-bottom: 1rem;
        text-align: center;
    }
    .metric-container {
        background: white;
        border-radius: 8px;
        padding: 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border-left: 4px solid #1f77b4;
    }
    .chart-container {
        background: white;
        border-radius: 8px;
        padding: 1.5rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    .section-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #333;
        margin: 2rem 0 1rem 0;
        border-bottom: 2px solid #1f77b4;
        padding-bottom: 0.5rem;
    }
    .warning-card {
        background: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem 0;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Create horizontal navigation
    create_horizontal_nav("Dashboard")
    
    dm = get_data_manager()
    vehicles_df = dm.load_vehicles()
    maintenance_df = dm.load_maintenance()
    equipment_df = dm.load_equipment()
    rentals_df = dm.load_rentals()
    
    if vehicles_df.empty and equipment_df.empty:
        st.markdown('<div class="warning-card">', unsafe_allow_html=True)
        st.warning("No data available. Please add vehicles and equipment first.")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("➕ Add Vehicles"):
                st.info("Navigate to 'Vehicle Inventory' page using the sidebar menu")
        with col2:
            if st.button("🔧 Add Equipment"):
                st.info("Navigate to 'Tool Hire' page using the sidebar menu")
        with col3:
            if st.button("📊 Log Maintenance"):
                st.info("Navigate to 'Maintenance Records' page using the sidebar menu")
        st.markdown('</div>', unsafe_allow_html=True)
        return
    
    # Key Metrics Row
    st.markdown('<div class="section-header">📈 Key Metrics</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        total_vehicles = len(vehicles_df)
        st.metric("Total Vehicles", total_vehicles)
    
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
        if not maintenance_df.empty:
            total_cost = maintenance_df['cost'].sum()
            st.metric("Maintenance Cost", f"£{total_cost:,.0f}")
        else:
            st.metric("Maintenance Cost", "£0")
    
    with col6:
        if not rentals_df.empty:
            total_revenue = rentals_df['rental_rate'].sum()
            st.metric("Rental Revenue", f"£{total_revenue:,.0f}")
        else:
            st.metric("Rental Revenue", "£0")
    
    st.markdown("---")
    
    # Charts Row 1
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🚗 Fleet Status Distribution")
        if not vehicles_df.empty:
            status_counts = vehicles_df['status'].value_counts()
            fig_status = px.pie(
                values=status_counts.values,
                names=status_counts.index,
                title="Vehicle Status Distribution"
            )
            fig_status.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_status, use_container_width=True)
        else:
            st.info("No vehicle data available")
    
    with col2:
        st.subheader("🏭 Fleet by Manufacturer")
        if not vehicles_df.empty:
            make_counts = vehicles_df['make'].value_counts().head(10)
            fig_make = px.bar(
                x=make_counts.values,
                y=make_counts.index,
                orientation='h',
                title="Top 10 Manufacturers",
                labels={'x': 'Number of Vehicles', 'y': 'Manufacturer'}
            )
            fig_make.update_layout(yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig_make, use_container_width=True)
        else:
            st.info("No vehicle data available")
    
    # Charts Row 2
    if not maintenance_df.empty:
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("💰 Maintenance Costs Over Time")
            
            # Prepare data for time series
            maintenance_df_copy = maintenance_df.copy()
            maintenance_df_copy['date'] = pd.to_datetime(maintenance_df_copy['date'])
            maintenance_df_copy['year_month'] = maintenance_df_copy['date'].dt.to_period('M')
            
            monthly_costs = maintenance_df_copy.groupby('year_month')['cost'].sum().reset_index()
            monthly_costs['year_month'] = monthly_costs['year_month'].astype(str)
            
            fig_costs = px.line(
                monthly_costs,
                x='year_month',
                y='cost',
                title="Monthly Maintenance Costs",
                labels={'cost': 'Cost ($)', 'year_month': 'Month'}
            )
            fig_costs.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig_costs, use_container_width=True)
        
        with col2:
            st.subheader("🔧 Maintenance Types")
            
            type_counts = maintenance_df['type'].value_counts()
            fig_types = px.bar(
                x=type_counts.index,
                y=type_counts.values,
                title="Maintenance Types Frequency",
                labels={'x': 'Maintenance Type', 'y': 'Count'}
            )
            fig_types.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig_types, use_container_width=True)
    
    # Vehicle Age and Mileage Analysis
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📅 Fleet Age Distribution")
        if not vehicles_df.empty:
            current_year = datetime.now().year
            vehicles_df_copy = vehicles_df.copy()
            vehicles_df_copy['age'] = current_year - vehicles_df_copy['year']
            
            fig_age = px.histogram(
                vehicles_df_copy,
                x='age',
                title="Vehicle Age Distribution",
                labels={'age': 'Age (Years)', 'count': 'Number of Vehicles'},
                nbins=15
            )
            st.plotly_chart(fig_age, use_container_width=True)
        else:
            st.info("No vehicle data available")
    
    with col2:
        st.subheader("🛣️ Mileage Distribution")
        if not vehicles_df.empty:
            fig_mileage = px.histogram(
                vehicles_df,
                x='mileage',
                title="Vehicle Mileage Distribution",
                labels={'mileage': 'Mileage', 'count': 'Number of Vehicles'},
                nbins=15
            )
            st.plotly_chart(fig_mileage, use_container_width=True)
        else:
            st.info("No vehicle data available")
    
    # Maintenance Analysis by Vehicle
    if not maintenance_df.empty and not vehicles_df.empty:
        st.markdown("---")
        st.subheader("🚙 Maintenance Analysis by Vehicle")
        
        # Merge maintenance with vehicle data
        maintenance_vehicle = maintenance_df.merge(vehicles_df, on='vehicle_id', how='left')
        maintenance_vehicle['vehicle_name'] = (
            maintenance_vehicle['year'].astype(str) + ' ' + 
            maintenance_vehicle['make'] + ' ' + 
            maintenance_vehicle['model'] + ' (' + 
            maintenance_vehicle['license_plate'] + ')'
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Top 10 vehicles by maintenance cost
            vehicle_costs = maintenance_vehicle.groupby('vehicle_name')['cost'].sum().sort_values(ascending=False).head(10)
            
            fig_vehicle_costs = px.bar(
                x=vehicle_costs.values,
                y=vehicle_costs.index,
                orientation='h',
                title="Top 10 Vehicles by Maintenance Cost",
                labels={'x': 'Total Cost ($)', 'y': 'Vehicle'}
            )
            fig_vehicle_costs.update_layout(yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig_vehicle_costs, use_container_width=True)
        
        with col2:
            # Maintenance frequency by vehicle
            vehicle_frequency = maintenance_vehicle.groupby('vehicle_name').size().sort_values(ascending=False).head(10)
            
            fig_vehicle_freq = px.bar(
                x=vehicle_frequency.values,
                y=vehicle_frequency.index,
                orientation='h',
                title="Top 10 Vehicles by Maintenance Frequency",
                labels={'x': 'Number of Maintenance Records', 'y': 'Vehicle'}
            )
            fig_vehicle_freq.update_layout(yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig_vehicle_freq, use_container_width=True)
    
    # Equipment and Rental Analysis
    if not equipment_df.empty:
        st.markdown("---")
        st.subheader("🔧 Equipment & Rental Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Equipment status distribution
            equipment_status = equipment_df['status'].value_counts()
            fig_equipment_status = px.pie(
                values=equipment_status.values,
                names=equipment_status.index,
                title="Equipment Status Distribution"
            )
            fig_equipment_status.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_equipment_status, use_container_width=True)
        
        with col2:
            # Equipment by category
            category_counts = equipment_df['category'].value_counts().head(8)
            fig_categories = px.bar(
                x=category_counts.values,
                y=category_counts.index,
                orientation='h',
                title="Equipment by Category",
                labels={'x': 'Number of Items', 'y': 'Category'}
            )
            fig_categories.update_layout(yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig_categories, use_container_width=True)
        
        # Rental revenue analysis
        if not rentals_df.empty:
            col1, col2 = st.columns(2)
            
            with col1:
                # Monthly rental revenue
                rentals_copy = rentals_df.copy()
                rentals_copy['start_date'] = pd.to_datetime(rentals_copy['start_date'])
                rentals_copy['year_month'] = rentals_copy['start_date'].dt.to_period('M')
                
                monthly_revenue = rentals_copy.groupby('year_month')['rental_rate'].sum().reset_index()
                monthly_revenue['year_month'] = monthly_revenue['year_month'].astype(str)
                
                fig_revenue = px.line(
                    monthly_revenue,
                    x='year_month',
                    y='rental_rate',
                    title="Monthly Rental Revenue",
                    labels={'rental_rate': 'Revenue ($)', 'year_month': 'Month'}
                )
                fig_revenue.update_layout(xaxis_tickangle=-45)
                st.plotly_chart(fig_revenue, use_container_width=True)
            
            with col2:
                # Top earning equipment
                equipment_revenue = rentals_df.merge(
                    equipment_df[['equipment_id', 'name']], 
                    on='equipment_id', 
                    how='left'
                )
                top_equipment = equipment_revenue.groupby('name')['rental_rate'].sum().sort_values(ascending=False).head(10)
                
                fig_top_equipment = px.bar(
                    x=top_equipment.values,
                    y=top_equipment.index,
                    orientation='h',
                    title="Top 10 Equipment by Revenue",
                    labels={'x': 'Total Revenue ($)', 'y': 'Equipment'}
                )
                fig_top_equipment.update_layout(yaxis={'categoryorder': 'total ascending'})
                st.plotly_chart(fig_top_equipment, use_container_width=True)
    
    # Recent Activity and Alerts
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📋 Recent Maintenance Activity")
        
        if not maintenance_df.empty:
            recent_maintenance = maintenance_df.sort_values('date', ascending=False).head(5)
            
            # Merge with vehicle info
            recent_with_vehicles = recent_maintenance.merge(
                vehicles_df[['vehicle_id', 'make', 'model', 'year', 'license_plate']], 
                on='vehicle_id', 
                how='left'
            )
            
            for _, record in recent_with_vehicles.iterrows():
                vehicle_info = f"{record['year']} {record['make']} {record['model']} ({record['license_plate']})"
                st.write(f"**{record['date']}** - {record['type']} on {vehicle_info} - ${record['cost']:.2f}")
        else:
            st.info("No recent maintenance activity")
    
    with col2:
        st.subheader("⚠️ Maintenance Alerts")
        
        if not maintenance_df.empty:
            # Check for overdue maintenance
            due_maintenance = maintenance_df[maintenance_df['next_due_mileage'].notna()].copy()
            
            if not due_maintenance.empty:
                due_maintenance = due_maintenance.merge(vehicles_df, on='vehicle_id', how='left')
                due_maintenance['miles_until_due'] = due_maintenance['next_due_mileage'] - due_maintenance['mileage']
                
                overdue = due_maintenance[due_maintenance['miles_until_due'] <= 0]
                due_soon = due_maintenance[(due_maintenance['miles_until_due'] > 0) & (due_maintenance['miles_until_due'] <= 1000)]
                
                if not overdue.empty:
                    st.error(f"🔴 {len(overdue)} vehicle(s) have overdue maintenance")
                    for _, item in overdue.head(3).iterrows():
                        vehicle_info = f"{item['year']} {item['make']} {item['model']}"
                        st.write(f"• {vehicle_info} - {item['type']}")
                
                if not due_soon.empty:
                    st.warning(f"🟡 {len(due_soon)} vehicle(s) due for maintenance soon")
                    for _, item in due_soon.head(3).iterrows():
                        vehicle_info = f"{item['year']} {item['make']} {item['model']}"
                        st.write(f"• {vehicle_info} - {item['type']} in {item['miles_until_due']:,} miles")
                
                if overdue.empty and due_soon.empty:
                    st.success("✅ No immediate maintenance alerts")
            else:
                st.info("No maintenance schedules tracked")
        else:
            st.info("No maintenance data available")
    
    # Export Reports
    st.markdown("---")
    st.subheader("📄 Reports & Export")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Generate Fleet Summary Report", use_container_width=True):
            # Create a comprehensive report
            report_data = []
            
            # Fleet summary
            report_data.append("FLEET MANAGEMENT SUMMARY REPORT")
            report_data.append("=" * 40)
            report_data.append(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
            report_data.append("")
            
            # Fleet statistics
            report_data.append("FLEET STATISTICS:")
            report_data.append(f"Total Vehicles: {len(vehicles_df)}")
            report_data.append(f"Active Vehicles: {len(vehicles_df[vehicles_df['status'] == 'Active'])}")
            report_data.append(f"Average Mileage: {vehicles_df['mileage'].mean():,.0f} miles")
            
            if not maintenance_df.empty:
                report_data.append(f"Total Maintenance Records: {len(maintenance_df)}")
                report_data.append(f"Total Maintenance Cost: ${maintenance_df['cost'].sum():,.2f}")
                report_data.append(f"Average Maintenance Cost: ${maintenance_df['cost'].mean():.2f}")
            
            report_content = "\n".join(report_data)
            
            st.download_button(
                label="📥 Download Report",
                data=report_content,
                file_name=f"fleet_summary_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain"
            )
    
    with col2:
        if not vehicles_df.empty:
            vehicle_csv = vehicles_df.to_csv(index=False)
            st.download_button(
                label="📥 Export Vehicle Data",
                data=vehicle_csv,
                file_name=f"vehicles_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True
            )
    
    with col3:
        if not maintenance_df.empty:
            maintenance_csv = maintenance_df.to_csv(index=False)
            st.download_button(
                label="📥 Export Maintenance Data",
                data=maintenance_csv,
                file_name=f"maintenance_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True
            )
    


if __name__ == "__main__":
    main()

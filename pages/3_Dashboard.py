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

st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")

# Initialize data manager
@st.cache_resource
def get_data_manager():
    return DataManager()

def main():
    st.title("📊 Fleet Management Dashboard")
    
    dm = get_data_manager()
    vehicles_df = dm.load_vehicles()
    maintenance_df = dm.load_maintenance()
    
    if vehicles_df.empty:
        st.warning("No data available. Please add vehicles and maintenance records first.")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("➕ Add Vehicles"):
                st.switch_page("pages/1_Vehicle_Inventory.py")
        with col2:
            if st.button("🔧 Log Maintenance"):
                st.switch_page("pages/2_Maintenance_Records.py")
        return
    
    # Key Metrics Row
    st.subheader("📈 Key Metrics")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        total_vehicles = len(vehicles_df)
        st.metric("Total Vehicles", total_vehicles)
    
    with col2:
        active_vehicles = len(vehicles_df[vehicles_df['status'] == 'Active'])
        st.metric("Active Vehicles", active_vehicles)
    
    with col3:
        if not maintenance_df.empty:
            total_cost = maintenance_df['cost'].sum()
            st.metric("Total Maintenance Cost", f"${total_cost:,.0f}")
        else:
            st.metric("Total Maintenance Cost", "$0")
    
    with col4:
        if not maintenance_df.empty:
            avg_cost = maintenance_df['cost'].mean()
            st.metric("Avg Maintenance Cost", f"${avg_cost:.0f}")
        else:
            st.metric("Avg Maintenance Cost", "$0")
    
    with col5:
        if not vehicles_df.empty:
            avg_mileage = vehicles_df['mileage'].mean()
            st.metric("Avg Vehicle Mileage", f"{avg_mileage:,.0f}")
        else:
            st.metric("Avg Vehicle Mileage", "0")
    
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

import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.data_manager import DataManager

st.set_page_config(page_title="Maintenance Records", page_icon="🔧", layout="wide")

# Initialize data manager
@st.cache_resource
def get_data_manager():
    return DataManager()

def main():
    st.title("🔧 Maintenance Records")
    
    dm = get_data_manager()
    
    # Check if there are any vehicles
    vehicles_df = dm.load_vehicles()
    if vehicles_df.empty:
        st.warning("No vehicles found. Please add vehicles first before logging maintenance.")
        if st.button("➕ Add Vehicles"):
            st.switch_page("pages/1_Vehicle_Inventory.py")
        return
    
    # Tabs for different actions
    tab1, tab2, tab3, tab4 = st.tabs(["📋 View Records", "➕ Log Maintenance", "📅 Upcoming Due", "📊 Import/Export"])
    
    with tab1:
        st.subheader("Maintenance History")
        
        maintenance_df = dm.load_maintenance()
        
        if not maintenance_df.empty:
            # Search and filter options
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                vehicle_filter = st.selectbox("Filter by Vehicle", ["All"] + vehicles_df['vehicle_id'].tolist())
            
            with col2:
                type_filter = st.selectbox("Filter by Type", ["All"] + sorted(maintenance_df['type'].unique().tolist()))
            
            with col3:
                # Date range filter
                date_range = st.selectbox("Date Range", ["All Time", "Last 30 Days", "Last 90 Days", "Last Year", "Custom"])
            
            with col4:
                if date_range == "Custom":
                    start_date = st.date_input("Start Date", value=date.today() - timedelta(days=365))
                    end_date = st.date_input("End Date", value=date.today())
            
            # Apply filters
            filtered_df = maintenance_df.copy()
            
            if vehicle_filter != "All":
                filtered_df = filtered_df[filtered_df['vehicle_id'] == vehicle_filter]
            
            if type_filter != "All":
                filtered_df = filtered_df[filtered_df['type'] == type_filter]
            
            # Apply date filter
            if date_range != "All Time":
                filtered_df['date'] = pd.to_datetime(filtered_df['date'])
                
                if date_range == "Last 30 Days":
                    cutoff_date = datetime.now() - timedelta(days=30)
                elif date_range == "Last 90 Days":
                    cutoff_date = datetime.now() - timedelta(days=90)
                elif date_range == "Last Year":
                    cutoff_date = datetime.now() - timedelta(days=365)
                elif date_range == "Custom":
                    cutoff_date = pd.Timestamp(start_date)
                    end_cutoff = pd.Timestamp(end_date)
                    filtered_df = filtered_df[
                        (filtered_df['date'] >= cutoff_date) & 
                        (filtered_df['date'] <= end_cutoff)
                    ]
                
                if date_range != "Custom":
                    filtered_df = filtered_df[filtered_df['date'] >= cutoff_date]
            
            # Display summary
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Records", len(filtered_df))
            with col2:
                if not filtered_df.empty:
                    total_cost = filtered_df['cost'].sum()
                    st.metric("Total Cost", f"${total_cost:,.2f}")
                else:
                    st.metric("Total Cost", "$0.00")
            with col3:
                if not filtered_df.empty:
                    avg_cost = filtered_df['cost'].mean()
                    st.metric("Average Cost", f"${avg_cost:.2f}")
                else:
                    st.metric("Average Cost", "$0.00")
            
            # Display records
            if not filtered_df.empty:
                # Sort by date (most recent first)
                filtered_df = filtered_df.sort_values('date', ascending=False)
                
                # Add vehicle info
                filtered_df = filtered_df.merge(
                    vehicles_df[['vehicle_id', 'make', 'model', 'year', 'license_plate']], 
                    on='vehicle_id', 
                    how='left'
                )
                
                # Display in expandable format
                for index, record in filtered_df.iterrows():
                    vehicle_info = f"{record['year']} {record['make']} {record['model']} ({record['license_plate']})"
                    
                    with st.expander(f"{record['date']} - {record['type']} - {vehicle_info} - ${record['cost']:.2f}"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.write(f"**Date:** {record['date']}")
                            st.write(f"**Type:** {record['type']}")
                            st.write(f"**Cost:** ${record['cost']:.2f}")
                            st.write(f"**Mileage:** {record['mileage']:,} miles")
                        
                        with col2:
                            st.write(f"**Vehicle:** {vehicle_info}")
                            st.write(f"**Service Provider:** {record.get('service_provider', 'Not specified')}")
                            if record.get('next_due_mileage'):
                                st.write(f"**Next Due:** {record['next_due_mileage']:,} miles")
                        
                        st.write(f"**Description:** {record['description']}")
                        
                        # Action buttons
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button(f"Edit", key=f"edit_maintenance_{record['maintenance_id']}"):
                                st.session_state[f'edit_maintenance_{record["maintenance_id"]}'] = True
                                st.rerun()
                        
                        with col2:
                            if st.button(f"Delete", key=f"delete_maintenance_{record['maintenance_id']}", type="secondary"):
                                if st.session_state.get(f'confirm_delete_maintenance_{record["maintenance_id"]}', False):
                                    dm.delete_maintenance(record['maintenance_id'])
                                    st.success("Maintenance record deleted successfully!")
                                    st.rerun()
                                else:
                                    st.session_state[f'confirm_delete_maintenance_{record["maintenance_id"]}'] = True
                                    st.warning("Click delete again to confirm")
                        
                        # Edit form
                        if st.session_state.get(f'edit_maintenance_{record["maintenance_id"]}', False):
                            st.markdown("---")
                            st.subheader("Edit Maintenance Record")
                            
                            with st.form(f"edit_maintenance_form_{record['maintenance_id']}"):
                                col1, col2 = st.columns(2)
                                
                                with col1:
                                    new_date = st.date_input("Date", value=pd.to_datetime(record['date']).date())
                                    new_type = st.selectbox("Type", 
                                                          ["Oil Change", "Tire Rotation", "Brake Service", "Transmission Service", 
                                                           "Engine Repair", "General Maintenance", "Inspection", "Other"],
                                                          index=["Oil Change", "Tire Rotation", "Brake Service", "Transmission Service", 
                                                                "Engine Repair", "General Maintenance", "Inspection", "Other"].index(record['type']) if record['type'] in ["Oil Change", "Tire Rotation", "Brake Service", "Transmission Service", "Engine Repair", "General Maintenance", "Inspection", "Other"] else 7)
                                    new_cost = st.number_input("Cost", min_value=0.0, value=float(record['cost']), format="%.2f")
                                    new_mileage = st.number_input("Mileage", min_value=0, value=int(record['mileage']))
                                
                                with col2:
                                    new_service_provider = st.text_input("Service Provider", value=record.get('service_provider', ''))
                                    new_next_due = st.number_input("Next Due Mileage (optional)", min_value=0, value=int(record.get('next_due_mileage', 0)))
                                    new_description = st.text_area("Description", value=record['description'])
                                
                                col1, col2 = st.columns(2)
                                with col1:
                                    if st.form_submit_button("Save Changes"):
                                        updated_maintenance = {
                                            'maintenance_id': record['maintenance_id'],
                                            'vehicle_id': record['vehicle_id'],
                                            'date': new_date.strftime('%Y-%m-%d'),
                                            'type': new_type,
                                            'description': new_description,
                                            'cost': new_cost,
                                            'mileage': new_mileage,
                                            'service_provider': new_service_provider,
                                            'next_due_mileage': new_next_due if new_next_due > 0 else None
                                        }
                                        dm.update_maintenance(updated_maintenance)
                                        st.success("Maintenance record updated successfully!")
                                        del st.session_state[f'edit_maintenance_{record["maintenance_id"]}']
                                        st.rerun()
                                
                                with col2:
                                    if st.form_submit_button("Cancel"):
                                        del st.session_state[f'edit_maintenance_{record["maintenance_id"]}']
                                        st.rerun()
            else:
                st.info("No maintenance records found matching your filters.")
        else:
            st.info("No maintenance records found. Start by logging your first maintenance activity.")
    
    with tab2:
        st.subheader("Log New Maintenance")
        
        with st.form("add_maintenance_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                # Create vehicle selection with readable names
                vehicle_options = {}
                for _, vehicle in vehicles_df.iterrows():
                    display_name = f"{vehicle['year']} {vehicle['make']} {vehicle['model']} ({vehicle['license_plate']})"
                    vehicle_options[display_name] = vehicle['vehicle_id']
                
                selected_vehicle_display = st.selectbox("Vehicle *", list(vehicle_options.keys()))
                selected_vehicle_id = vehicle_options[selected_vehicle_display]
                
                maintenance_date = st.date_input("Date *", value=date.today())
                maintenance_type = st.selectbox("Type *", [
                    "Oil Change", "Tire Rotation", "Brake Service", "Transmission Service", 
                    "Engine Repair", "General Maintenance", "Inspection", "Other"
                ])
                cost = st.number_input("Cost *", min_value=0.0, value=0.0, format="%.2f")
            
            with col2:
                # Get current mileage for selected vehicle
                current_vehicle = vehicles_df[vehicles_df['vehicle_id'] == selected_vehicle_id].iloc[0]
                current_mileage = int(current_vehicle['mileage'])
                
                mileage = st.number_input("Current Mileage *", min_value=current_mileage, value=current_mileage)
                service_provider = st.text_input("Service Provider", placeholder="e.g., Joe's Auto Shop")
                next_due_mileage = st.number_input("Next Due Mileage (optional)", min_value=0, value=0)
            
            description = st.text_area("Description *", placeholder="Describe the maintenance performed...")
            
            if st.form_submit_button("Log Maintenance", type="primary"):
                if not description.strip():
                    st.error("Please provide a description of the maintenance performed.")
                elif cost <= 0:
                    st.error("Please enter a valid cost.")
                else:
                    # Add maintenance record
                    new_maintenance = {
                        'vehicle_id': selected_vehicle_id,
                        'date': maintenance_date.strftime('%Y-%m-%d'),
                        'type': maintenance_type,
                        'description': description.strip(),
                        'cost': cost,
                        'mileage': mileage,
                        'service_provider': service_provider.strip() if service_provider.strip() else None,
                        'next_due_mileage': next_due_mileage if next_due_mileage > 0 else None
                    }
                    dm.add_maintenance(new_maintenance)
                    
                    # Update vehicle mileage if higher
                    if mileage > current_mileage:
                        dm.update_vehicle_mileage(selected_vehicle_id, mileage)
                    
                    st.success(f"Maintenance logged successfully for {selected_vehicle_display}!")
                    st.rerun()
    
    with tab3:
        st.subheader("Upcoming Maintenance Due")
        
        maintenance_df = dm.load_maintenance()
        
        if not maintenance_df.empty:
            # Get vehicles with next due mileage
            due_maintenance = maintenance_df[maintenance_df['next_due_mileage'].notna()].copy()
            
            if not due_maintenance.empty:
                # Merge with vehicle data
                due_maintenance = due_maintenance.merge(vehicles_df, on='vehicle_id', how='left')
                
                # Calculate how close each vehicle is to due maintenance
                due_maintenance['miles_until_due'] = due_maintenance['next_due_mileage'] - due_maintenance['mileage']
                
                # Sort by miles until due (closest first)
                due_maintenance = due_maintenance.sort_values('miles_until_due')
                
                # Categorize by urgency
                overdue = due_maintenance[due_maintenance['miles_until_due'] <= 0]
                due_soon = due_maintenance[(due_maintenance['miles_until_due'] > 0) & (due_maintenance['miles_until_due'] <= 1000)]
                upcoming = due_maintenance[due_maintenance['miles_until_due'] > 1000]
                
                # Display overdue items
                if not overdue.empty:
                    st.error("⚠️ Overdue Maintenance")
                    for _, item in overdue.iterrows():
                        vehicle_info = f"{item['year']} {item['make']} {item['model']} ({item['license_plate']})"
                        overdue_miles = abs(item['miles_until_due'])
                        st.write(f"🔴 **{vehicle_info}** - {item['type']} - Overdue by {overdue_miles:,} miles")
                
                # Display due soon items
                if not due_soon.empty:
                    st.warning("⏰ Due Soon (Within 1,000 miles)")
                    for _, item in due_soon.iterrows():
                        vehicle_info = f"{item['year']} {item['make']} {item['model']} ({item['license_plate']})"
                        st.write(f"🟡 **{vehicle_info}** - {item['type']} - Due in {item['miles_until_due']:,} miles")
                
                # Display upcoming items
                if not upcoming.empty:
                    st.info("📅 Upcoming Maintenance")
                    for _, item in upcoming.iterrows():
                        vehicle_info = f"{item['year']} {item['make']} {item['model']} ({item['license_plate']})"
                        st.write(f"🟢 **{vehicle_info}** - {item['type']} - Due in {item['miles_until_due']:,} miles")
                
                if overdue.empty and due_soon.empty and upcoming.empty:
                    st.success("✅ No upcoming maintenance scheduled!")
            else:
                st.info("No maintenance schedules found. Log maintenance with 'Next Due Mileage' to track upcoming services.")
        else:
            st.info("No maintenance records found.")
    
    with tab4:
        st.subheader("Import/Export Maintenance Data")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Export Data")
            maintenance_df = dm.load_maintenance()
            
            if not maintenance_df.empty:
                # Merge with vehicle data for better export
                export_df = maintenance_df.merge(
                    vehicles_df[['vehicle_id', 'make', 'model', 'year', 'license_plate']], 
                    on='vehicle_id', 
                    how='left'
                )
                
                csv_data = export_df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Maintenance CSV",
                    data=csv_data,
                    file_name=f"maintenance_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            else:
                st.info("No maintenance records to export")
        
        with col2:
            st.markdown("#### Import Data")
            uploaded_file = st.file_uploader("Choose a CSV file", type="csv", key="maintenance_upload")
            
            if uploaded_file is not None:
                try:
                    import_df = pd.read_csv(uploaded_file)
                    
                    # Validate required columns
                    required_columns = ['vehicle_id', 'date', 'type', 'description', 'cost', 'mileage']
                    
                    if all(col in import_df.columns for col in required_columns):
                        st.write("Preview of imported data:")
                        st.dataframe(import_df.head())
                        
                        if st.button("Import Maintenance Records"):
                            success_count = dm.import_maintenance(import_df)
                            st.success(f"Successfully imported {success_count} maintenance records!")
                            st.rerun()
                    else:
                        st.error(f"CSV must contain these columns: {', '.join(required_columns)}")
                        
                except Exception as e:
                    st.error(f"Error reading CSV file: {str(e)}")

if __name__ == "__main__":
    main()

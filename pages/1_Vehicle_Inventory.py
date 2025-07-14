import streamlit as st
import pandas as pd
from datetime import datetime, date
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.data_manager import DataManager
from utils.validators import validate_vin, validate_year

st.set_page_config(page_title="Vehicle Inventory", page_icon="🚗", layout="wide")

# Initialize data manager
@st.cache_resource
def get_data_manager():
    return DataManager()

def main():
    st.title("🚗 Vehicle Inventory Management")
    
    dm = get_data_manager()
    
    # Tabs for different actions
    tab1, tab2, tab3 = st.tabs(["📋 View Inventory", "➕ Add Vehicle", "📊 Import/Export"])
    
    with tab1:
        st.subheader("Current Fleet")
        
        # Load vehicles
        vehicles_df = dm.load_vehicles()
        
        if not vehicles_df.empty:
            # Search and filter options
            col1, col2, col3 = st.columns(3)
            
            with col1:
                search_term = st.text_input("🔍 Search vehicles", placeholder="Make, model, VIN...")
            
            with col2:
                status_filter = st.selectbox("Filter by Status", ["All", "Active", "Inactive", "Maintenance"])
            
            with col3:
                year_filter = st.selectbox("Filter by Year", ["All"] + sorted(vehicles_df['year'].unique().tolist(), reverse=True))
            
            # Apply filters
            filtered_df = vehicles_df.copy()
            
            if search_term:
                mask = (
                    filtered_df['make'].str.contains(search_term, case=False, na=False) |
                    filtered_df['model'].str.contains(search_term, case=False, na=False) |
                    filtered_df['vin'].str.contains(search_term, case=False, na=False) |
                    filtered_df['license_plate'].str.contains(search_term, case=False, na=False)
                )
                filtered_df = filtered_df[mask]
            
            if status_filter != "All":
                filtered_df = filtered_df[filtered_df['status'] == status_filter]
            
            if year_filter != "All":
                filtered_df = filtered_df[filtered_df['year'] == year_filter]
            
            # Display results
            st.write(f"Showing {len(filtered_df)} of {len(vehicles_df)} vehicles")
            
            # Display vehicles in a more readable format
            for index, vehicle in filtered_df.iterrows():
                with st.expander(f"{vehicle['year']} {vehicle['make']} {vehicle['model']} - {vehicle['license_plate']}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**VIN:** {vehicle['vin']}")
                        st.write(f"**Year:** {vehicle['year']}")
                        st.write(f"**Make:** {vehicle['make']}")
                        st.write(f"**Model:** {vehicle['model']}")
                    
                    with col2:
                        st.write(f"**License Plate:** {vehicle['license_plate']}")
                        st.write(f"**Status:** {vehicle['status']}")
                        st.write(f"**Mileage:** {vehicle['mileage']:,} miles")
                        st.write(f"**Purchase Date:** {vehicle['purchase_date']}")
                    
                    # Action buttons
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        if st.button(f"Edit", key=f"edit_{vehicle['vehicle_id']}"):
                            st.session_state[f'edit_vehicle_{vehicle["vehicle_id"]}'] = True
                            st.rerun()
                    
                    with col2:
                        if st.button(f"Update Mileage", key=f"mileage_{vehicle['vehicle_id']}"):
                            st.session_state[f'update_mileage_{vehicle["vehicle_id"]}'] = True
                            st.rerun()
                    
                    with col3:
                        if st.button(f"Delete", key=f"delete_{vehicle['vehicle_id']}", type="secondary"):
                            if st.session_state.get(f'confirm_delete_{vehicle["vehicle_id"]}', False):
                                dm.delete_vehicle(vehicle['vehicle_id'])
                                st.success("Vehicle deleted successfully!")
                                st.rerun()
                            else:
                                st.session_state[f'confirm_delete_{vehicle["vehicle_id"]}'] = True
                                st.warning("Click delete again to confirm")
                    
                    # Edit form
                    if st.session_state.get(f'edit_vehicle_{vehicle["vehicle_id"]}', False):
                        st.markdown("---")
                        st.subheader("Edit Vehicle")
                        
                        with st.form(f"edit_form_{vehicle['vehicle_id']}"):
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                new_make = st.text_input("Make", value=vehicle['make'])
                                new_model = st.text_input("Model", value=vehicle['model'])
                                new_year = st.number_input("Year", min_value=1900, max_value=2030, value=int(vehicle['year']))
                                new_vin = st.text_input("VIN", value=vehicle['vin'])
                            
                            with col2:
                                new_license = st.text_input("License Plate", value=vehicle['license_plate'])
                                new_status = st.selectbox("Status", ["Active", "Inactive", "Maintenance"], 
                                                        index=["Active", "Inactive", "Maintenance"].index(vehicle['status']))
                                new_mileage = st.number_input("Mileage", min_value=0, value=int(vehicle['mileage']))
                                new_purchase_date = st.date_input("Purchase Date", value=pd.to_datetime(vehicle['purchase_date']).date())
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                if st.form_submit_button("Save Changes"):
                                    # Validate inputs
                                    if not validate_vin(new_vin):
                                        st.error("Invalid VIN format")
                                    elif not validate_year(new_year):
                                        st.error("Invalid year")
                                    else:
                                        # Update vehicle
                                        updated_vehicle = {
                                            'vehicle_id': vehicle['vehicle_id'],
                                            'make': new_make,
                                            'model': new_model,
                                            'year': new_year,
                                            'vin': new_vin,
                                            'license_plate': new_license,
                                            'status': new_status,
                                            'mileage': new_mileage,
                                            'purchase_date': new_purchase_date.strftime('%Y-%m-%d')
                                        }
                                        dm.update_vehicle(updated_vehicle)
                                        st.success("Vehicle updated successfully!")
                                        del st.session_state[f'edit_vehicle_{vehicle["vehicle_id"]}']
                                        st.rerun()
                            
                            with col2:
                                if st.form_submit_button("Cancel"):
                                    del st.session_state[f'edit_vehicle_{vehicle["vehicle_id"]}']
                                    st.rerun()
                    
                    # Update mileage form
                    if st.session_state.get(f'update_mileage_{vehicle["vehicle_id"]}', False):
                        st.markdown("---")
                        st.subheader("Update Mileage")
                        
                        with st.form(f"mileage_form_{vehicle['vehicle_id']}"):
                            new_mileage = st.number_input("New Mileage", min_value=int(vehicle['mileage']), value=int(vehicle['mileage']))
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                if st.form_submit_button("Update Mileage"):
                                    dm.update_vehicle_mileage(vehicle['vehicle_id'], new_mileage)
                                    st.success("Mileage updated successfully!")
                                    del st.session_state[f'update_mileage_{vehicle["vehicle_id"]}']
                                    st.rerun()
                            
                            with col2:
                                if st.form_submit_button("Cancel"):
                                    del st.session_state[f'update_mileage_{vehicle["vehicle_id"]}']
                                    st.rerun()
        else:
            st.info("No vehicles in inventory. Add your first vehicle using the 'Add Vehicle' tab.")
    
    with tab2:
        st.subheader("Add New Vehicle")
        
        with st.form("add_vehicle_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                make = st.text_input("Make *", placeholder="e.g., Ford, Toyota, Chevrolet")
                model = st.text_input("Model *", placeholder="e.g., F-150, Camry, Silverado")
                year = st.number_input("Year *", min_value=1900, max_value=2030, value=datetime.now().year)
                vin = st.text_input("VIN *", placeholder="17-character VIN")
            
            with col2:
                license_plate = st.text_input("License Plate *", placeholder="e.g., ABC-1234")
                status = st.selectbox("Status *", ["Active", "Inactive", "Maintenance"])
                mileage = st.number_input("Current Mileage *", min_value=0, value=0)
                purchase_date = st.date_input("Purchase Date *", value=date.today())
            
            if st.form_submit_button("Add Vehicle", type="primary"):
                # Validate inputs
                if not all([make, model, year, vin, license_plate]):
                    st.error("Please fill in all required fields marked with *")
                elif not validate_vin(vin):
                    st.error("Invalid VIN format. VIN must be 17 characters long.")
                elif not validate_year(year):
                    st.error("Invalid year. Year must be between 1900 and 2030.")
                else:
                    # Check if VIN already exists
                    vehicles_df = dm.load_vehicles()
                    if not vehicles_df.empty and vin in vehicles_df['vin'].values:
                        st.error("A vehicle with this VIN already exists.")
                    else:
                        # Add vehicle
                        new_vehicle = {
                            'make': make,
                            'model': model,
                            'year': year,
                            'vin': vin,
                            'license_plate': license_plate,
                            'status': status,
                            'mileage': mileage,
                            'purchase_date': purchase_date.strftime('%Y-%m-%d')
                        }
                        dm.add_vehicle(new_vehicle)
                        st.success(f"Vehicle {year} {make} {model} added successfully!")
                        st.rerun()
    
    with tab3:
        st.subheader("Import/Export Data")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Export Data")
            vehicles_df = dm.load_vehicles()
            
            if not vehicles_df.empty:
                csv_data = vehicles_df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Vehicles CSV",
                    data=csv_data,
                    file_name=f"vehicles_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            else:
                st.info("No vehicles to export")
        
        with col2:
            st.markdown("#### Import Data")
            uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
            
            if uploaded_file is not None:
                try:
                    import_df = pd.read_csv(uploaded_file)
                    
                    # Validate required columns
                    required_columns = ['make', 'model', 'year', 'vin', 'license_plate', 'status', 'mileage', 'purchase_date']
                    
                    if all(col in import_df.columns for col in required_columns):
                        st.write("Preview of imported data:")
                        st.dataframe(import_df.head())
                        
                        if st.button("Import Vehicles"):
                            success_count = dm.import_vehicles(import_df)
                            st.success(f"Successfully imported {success_count} vehicles!")
                            st.rerun()
                    else:
                        st.error(f"CSV must contain these columns: {', '.join(required_columns)}")
                        
                except Exception as e:
                    st.error(f"Error reading CSV file: {str(e)}")

if __name__ == "__main__":
    main()

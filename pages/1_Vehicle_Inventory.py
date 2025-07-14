import streamlit as st
import pandas as pd
from datetime import datetime, date
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.data_manager import DataManager
from utils.validators import validate_weight, validate_year

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
                search_term = st.text_input("🔍 Search vehicles", placeholder="Make, model, Whites ID...")
            
            with col2:
                status_filter = st.selectbox("Filter by Status", ["All", "On Hire", "Off Hire", "Maintenance"])
            
            with col3:
                # Handle vehicle type filter with NaN values
                if 'vehicle_type' in vehicles_df.columns and not vehicles_df.empty:
                    unique_types = vehicles_df['vehicle_type'].dropna().unique().tolist()
                    type_options = ["All"] + sorted([str(t) for t in unique_types])
                    # Add "Unknown" if there are any NaN values
                    if vehicles_df['vehicle_type'].isna().any():
                        type_options.append("Unknown")
                else:
                    type_options = ["All"]
                type_filter = st.selectbox("Filter by Type", type_options)
            
            # Apply filters
            filtered_df = vehicles_df.copy()
            
            if search_term:
                mask = (
                    filtered_df['make'].str.contains(search_term, case=False, na=False) |
                    filtered_df['model'].str.contains(search_term, case=False, na=False) |
                    filtered_df.get('whites_id', pd.Series()).astype(str).str.contains(search_term, case=False, na=False) |
                    filtered_df['license_plate'].str.contains(search_term, case=False, na=False)
                )
                filtered_df = filtered_df[mask]
            
            if status_filter != "All":
                filtered_df = filtered_df[filtered_df['status'] == status_filter]
            
            if type_filter != "All":
                filtered_df = filtered_df[filtered_df['vehicle_type'].fillna('Unknown') == type_filter]
            
            # Display results
            st.write(f"Showing {len(filtered_df)} of {len(vehicles_df)} vehicles")
            
            # Display vehicles in a more readable format
            for index, vehicle in filtered_df.iterrows():
                whites_id = vehicle.get('whites_id', 'N/A')
                vehicle_type = vehicle.get('vehicle_type', 'Unknown')
                with st.expander(f"{vehicle['year']} {vehicle['make']} {vehicle['model']} - {vehicle_type} (ID: {whites_id})"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**Whites ID:** {whites_id}")
                        st.write(f"**Year:** {vehicle['year']}")
                        st.write(f"**Make:** {vehicle['make']}")
                        st.write(f"**Model:** {vehicle['model']}")
                        st.write(f"**Vehicle Type:** {vehicle_type}")
                        st.write(f"**Weight:** {vehicle.get('weight', 'N/A')} tonnes")
                    
                    with col2:
                        st.write(f"**License Plate:** {vehicle['license_plate']}")
                        st.write(f"**Status:** {vehicle['status']}")
                        st.write(f"**Mileage:** {vehicle['mileage']:,} miles")
                        if vehicle.get('defects'):
                            st.write(f"**Defects:** {vehicle['defects']}")
                        if vehicle.get('notes'):
                            st.write(f"**Notes:** {vehicle['notes']}")
                    
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
                                new_whites_id = st.text_input("Whites ID", value=vehicle.get('whites_id', ''))
                                new_make = st.text_input("Make", value=vehicle['make'])
                                new_model = st.text_input("Model", value=vehicle['model'])
                                new_year = st.number_input("Year", min_value=1900, max_value=2030, value=int(vehicle['year']))
                                new_weight = st.number_input("Weight (tonnes)", min_value=0.1, value=float(vehicle.get('weight', 1.0)), format="%.1f")
                                
                                # Vehicle type with custom option
                                existing_types = ["Digger", "Dumper", "Roller", "Excavator", "Truck", "Van", "Other"]
                                current_type = vehicle.get('vehicle_type', 'Other')
                                if current_type not in existing_types:
                                    existing_types.append(current_type)
                                
                                type_option = st.selectbox("Vehicle Type", existing_types + ["Add Custom..."], 
                                                         index=existing_types.index(current_type) if current_type in existing_types else len(existing_types)-1)
                                
                                if type_option == "Add Custom...":
                                    new_vehicle_type = st.text_input("Custom Vehicle Type")
                                else:
                                    new_vehicle_type = type_option
                            
                            with col2:
                                new_license = st.text_input("License Plate", value=vehicle['license_plate'])
                                new_status = st.selectbox("Status", ["On Hire", "Off Hire", "Maintenance"], 
                                                        index=["On Hire", "Off Hire", "Maintenance"].index(vehicle['status']) if vehicle['status'] in ["On Hire", "Off Hire", "Maintenance"] else 1)
                                new_mileage = st.number_input("Mileage", min_value=0, value=int(vehicle['mileage']))
                                new_defects = st.text_area("Defects", value=vehicle.get('defects', ''))
                                new_notes = st.text_area("Notes", value=vehicle.get('notes', ''))
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                if st.form_submit_button("Save Changes"):
                                    # Validate inputs
                                    if not validate_weight(new_weight):
                                        st.error("Invalid weight - must be a positive number")
                                    elif not validate_year(new_year):
                                        st.error("Invalid year")
                                    elif not new_vehicle_type:
                                        st.error("Please select or enter a vehicle type")
                                    else:
                                        # Update vehicle
                                        updated_vehicle = {
                                            'vehicle_id': vehicle['vehicle_id'],
                                            'whites_id': new_whites_id,
                                            'make': new_make,
                                            'model': new_model,
                                            'year': new_year,
                                            'weight': new_weight,
                                            'license_plate': new_license,
                                            'vehicle_type': new_vehicle_type,
                                            'status': new_status,
                                            'mileage': new_mileage,
                                            'defects': new_defects,
                                            'notes': new_notes
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
                whites_id = st.text_input("Whites ID", placeholder="e.g., W001, W123")
                make = st.text_input("Make *", placeholder="e.g., Caterpillar, JCB, Volvo")
                model = st.text_input("Model *", placeholder="e.g., 320D, 3CX, EC220")
                year = st.number_input("Year *", min_value=1900, max_value=2030, value=datetime.now().year)
                weight = st.number_input("Weight (tonnes) *", min_value=0.1, value=1.0, format="%.1f")
                
                # Vehicle type with custom option
                vehicle_types = ["Digger", "Dumper", "Roller", "Excavator", "Truck", "Van", "Telehandler", "Compactor", "Other"]
                type_option = st.selectbox("Vehicle Type *", vehicle_types + ["Add Custom..."])
                
                if type_option == "Add Custom...":
                    vehicle_type = st.text_input("Custom Vehicle Type *")
                else:
                    vehicle_type = type_option
            
            with col2:
                license_plate = st.text_input("License Plate *", placeholder="e.g., ABC-1234")
                status = st.selectbox("Status *", ["Off Hire", "On Hire", "Maintenance"])
                mileage = st.number_input("Current Mileage *", min_value=0, value=0)
                defects = st.text_area("Defects", placeholder="List any known defects or issues...")
                notes = st.text_area("Notes", placeholder="Additional information about the vehicle...")
            
            if st.form_submit_button("Add Vehicle", type="primary"):
                # Validate inputs
                if not all([make, model, year, weight, license_plate, vehicle_type]):
                    st.error("Please fill in all required fields marked with *")
                elif not validate_weight(weight):
                    st.error("Invalid weight. Weight must be a positive number.")
                elif not validate_year(year):
                    st.error("Invalid year. Year must be between 1900 and 2030.")
                else:
                    # Check if Whites ID already exists (if provided)
                    vehicles_df = dm.load_vehicles()
                    if whites_id and not vehicles_df.empty and 'whites_id' in vehicles_df.columns:
                        if whites_id in vehicles_df['whites_id'].values:
                            st.error("A vehicle with this Whites ID already exists.")
                            continue_process = False
                        else:
                            continue_process = True
                    else:
                        continue_process = True
                    
                    if continue_process:
                        # Add vehicle
                        new_vehicle = {
                            'whites_id': whites_id,
                            'make': make,
                            'model': model,
                            'year': year,
                            'weight': weight,
                            'license_plate': license_plate,
                            'vehicle_type': vehicle_type,
                            'status': status,
                            'mileage': mileage,
                            'defects': defects,
                            'notes': notes
                        }
                        dm.add_vehicle(new_vehicle)
                        st.success(f"Vehicle {year} {make} {model} ({vehicle_type}) added successfully!")
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
                    required_columns = ['make', 'model', 'year', 'weight', 'license_plate', 'vehicle_type', 'status', 'mileage']
                    
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

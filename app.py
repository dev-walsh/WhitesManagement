import streamlit as st
import pandas as pd
from datetime import datetime, date
import os
from utils.data_manager import DataManager
from login import check_password, show_logout_button, get_current_user, logout
import plotly.express as px

# Set page configuration at the top level
st.set_page_config(
    page_title="Whites Management System",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize data manager
@st.cache_resource
def get_data_manager():
    return DataManager()

def create_single_page_layout(vehicles_df, maintenance_df, equipment_df, rentals_df):
    """Create single-page layout with all functionality"""
    
    # Header with navigation and user info
    st.markdown("""
    <div style="background: rgba(255, 255, 255, 0.03); border-radius: 12px; padding: 1.5rem; margin-bottom: 2rem; border: 1px solid rgba(255, 255, 255, 0.1);">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
            <div>
                <h1 style="margin: 0; color: #2196f3; font-size: 2rem;">🚗 Whites Management System</h1>
                <p style="margin: 0.5rem 0 0 0; color: #b0bec5;">Complete fleet and equipment management solution</p>
            </div>
            <div style="display: flex; align-items: center; gap: 1rem;">
                <span style="color: #e0e6ed;">👤 Welcome, admin</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "🚗 Vehicles", 
        "🏗️ Machines",
        "🔧 Maintenance", 
        "📊 Dashboard", 
        "⚙️ Tool Hire", 
        "📈 Statistics"
    ])
    
    with tab1:
        show_vehicle_inventory_content(vehicles_df)
    
    with tab2:
        show_machine_inventory_content()
    
    with tab3:
        show_maintenance_content(maintenance_df, vehicles_df)
    
    with tab4:
        show_dashboard_content(vehicles_df, maintenance_df, equipment_df, rentals_df)
    
    with tab5:
        show_tool_hire_content(equipment_df, rentals_df)
    
    with tab6:
        show_statistics_content(vehicles_df, maintenance_df, equipment_df, rentals_df)
    
    # Footer with quick actions and export options
    st.markdown("---")
    
    # Custom CSS for blue export buttons
    st.markdown("""
    <style>
    /* All download buttons should have blue gradient */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #2196f3 0%, #1976d2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.5rem 1rem !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 2px 4px rgba(33, 150, 243, 0.3) !important;
        width: 100% !important;
    }
    .stDownloadButton > button:hover {
        background: linear-gradient(135deg, #1976d2 0%, #1565c0 100%) !important;
        box-shadow: 0 4px 8px rgba(33, 150, 243, 0.4) !important;
        transform: translateY(-2px) !important;
    }
    .stDownloadButton > button:active {
        transform: translateY(0px) !important;
        box-shadow: 0 2px 4px rgba(33, 150, 243, 0.3) !important;
    }
    
    /* Style disabled buttons in export section */
    .stButton > button[disabled] {
        background: linear-gradient(135deg, #666666 0%, #555555 100%) !important;
        color: #cccccc !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.5rem 1rem !important;
        font-weight: 500 !important;
        width: 100% !important;
        cursor: not-allowed !important;
        opacity: 0.7 !important;
    }
    
    .stButton > button[disabled]:hover {
        background: linear-gradient(135deg, #666666 0%, #555555 100%) !important;
        transform: none !important;
    }
    
    /* Force blue gradient on all export buttons regardless of position */
    div[data-testid="stVerticalBlock"] .stDownloadButton > button,
    div[data-testid="column"] .stDownloadButton > button,
    .stDownloadButton button,
    button[kind="primary"] {
        background: linear-gradient(135deg, #2196f3 0%, #1976d2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.5rem 1rem !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 2px 4px rgba(33, 150, 243, 0.3) !important;
        width: 100% !important;
    }
    
    /* Hover effects for all export buttons */
    div[data-testid="stVerticalBlock"] .stDownloadButton > button:hover,
    div[data-testid="column"] .stDownloadButton > button:hover,
    .stDownloadButton button:hover,
    button[kind="primary"]:hover {
        background: linear-gradient(135deg, #1976d2 0%, #1565c0 100%) !important;
        box-shadow: 0 4px 8px rgba(33, 150, 243, 0.4) !important;
        transform: translateY(-2px) !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 📥 Quick Export")
        
        # Get fresh data for machines
        dm = get_data_manager()
        machines_df = dm.load_machines()
        
        # Vehicles Export
        if not vehicles_df.empty:
            excel_vehicles = create_excel_export({"Vehicles": vehicles_df}, "vehicles.xlsx")
            st.download_button(
                label="🚗 Vehicles Excel",
                data=excel_vehicles,
                file_name=f"vehicles_{datetime.now().strftime('%Y%m%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
        else:
            st.button("🚗 Vehicles Excel", disabled=True, use_container_width=True, help="No vehicles to export")
        
        # Machines Export
        if not machines_df.empty:
            excel_machines = create_excel_export({"Machines": machines_df}, "machines.xlsx")
            st.download_button(
                label="🏗️ Machines Excel",
                data=excel_machines,
                file_name=f"machines_{datetime.now().strftime('%Y%m%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
        else:
            st.button("🏗️ Machines Excel", disabled=True, use_container_width=True, help="No machines to export")
        
        # Maintenance Export
        if not maintenance_df.empty:
            excel_maintenance = create_excel_export({"Maintenance": maintenance_df}, "maintenance.xlsx")
            st.download_button(
                label="🔧 Maintenance Excel",
                data=excel_maintenance,
                file_name=f"maintenance_{datetime.now().strftime('%Y%m%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
        else:
            st.button("🔧 Maintenance Excel", disabled=True, use_container_width=True, help="No maintenance records to export")
        
        # Equipment Export
        if not equipment_df.empty:
            excel_equipment = create_excel_export({"Equipment": equipment_df}, "equipment.xlsx")
            st.download_button(
                label="⚙️ Equipment Excel",
                data=excel_equipment,
                file_name=f"equipment_{datetime.now().strftime('%Y%m%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
        else:
            st.button("⚙️ Equipment Excel", disabled=True, use_container_width=True, help="No equipment to export")
        
        # Complete Export (All Data)
        has_any_data = not (vehicles_df.empty and machines_df.empty and maintenance_df.empty and equipment_df.empty)
        if has_any_data:
            all_data = {}
            if not vehicles_df.empty:
                all_data["Vehicles"] = vehicles_df
            if not machines_df.empty:
                all_data["Machines"] = machines_df
            if not maintenance_df.empty:
                all_data["Maintenance"] = maintenance_df
            if not equipment_df.empty:
                all_data["Equipment"] = equipment_df
            
            excel_all = create_excel_export(all_data, "all_data.xlsx")
            st.download_button(
                label="📊 Complete Export",
                data=excel_all,
                file_name=f"whites_management_{datetime.now().strftime('%Y%m%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
        else:
            st.button("📊 Complete Export", disabled=True, use_container_width=True, help="No data to export")
    
    with col2:
        st.markdown("### 📊 Quick Export")
        
        # Show data summary
        total_vehicles = len(vehicles_df)
        total_machines = len(machines_df)
        total_maintenance = len(maintenance_df)
        total_equipment = len(equipment_df)
        
        st.markdown(f"""
        **Data Summary:**
        - 🚗 Vehicles: {total_vehicles}
        - 🏗️ Machines: {total_machines}
        - 🔧 Maintenance Records: {total_maintenance}
        - ⚙️ Equipment: {total_equipment}
        """)
    
    with col3:
        st.markdown("### 🚪 Account")
        if st.button("🚪 Logout", use_container_width=True):
            logout()


def show_vehicle_inventory_content(vehicles_df):
    """Vehicle inventory content"""
    st.markdown("### 🚗 Vehicle Inventory Management")
    
    # Reload data to ensure we have the latest vehicles
    dm = get_data_manager()
    vehicles_df = dm.load_vehicles()
    
    # Add new vehicle form
    with st.expander("➕ Add New Vehicle"):
        with st.form("add_vehicle_form"):
            col1, col2, col3 = st.columns(3)
            with col1:
                make = st.text_input("Make*", placeholder="Toyota")
                model = st.text_input("Model*", placeholder="Hilux")
                year = st.number_input("Year*", min_value=1900, max_value=2030, value=2020)
                license_plate = st.text_input("License Plate*", placeholder="ABC123")
                fuel_type = st.selectbox("Fuel Type*", ["Petrol", "Diesel", "Electric", "Hybrid"])
            
            with col2:
                whites_id = st.text_input("Whites ID", placeholder="W001")
                vin_chassis = st.text_input("VIN/Chassis", placeholder="VIN123456789")
                vehicle_type = st.selectbox("Vehicle Type", ["Car", "Van", "Truck", "Lorry", "Bus", "Motorcycle", "Other"])
                mileage = st.number_input("Mileage*", min_value=0, value=0)
                weight = st.number_input("Weight (tonnes)*", min_value=0.0, value=1.5, format="%.1f")
            
            with col3:
                status = st.selectbox("Status*", ["Active", "Maintenance", "Retired"])
                defects = st.text_area("Defects", placeholder="List any known defects...")
                notes = st.text_area("Notes", placeholder="Additional notes...")
            
            if st.form_submit_button("Add Vehicle", use_container_width=True):
                if make and model and license_plate:
                    vehicle_data = {
                        'make': make,
                        'model': model,
                        'year': year,
                        'license_plate': license_plate,
                        'fuel_type': fuel_type,
                        'mileage': mileage,
                        'weight': weight,
                        'status': status,
                        'whites_id': whites_id if whites_id else None,
                        'vin_chassis': vin_chassis if vin_chassis else None,
                        'vehicle_type': vehicle_type if vehicle_type else None,
                        'defects': defects if defects else None,
                        'notes': notes if notes else None
                    }
                    dm = get_data_manager()
                    dm.add_vehicle(vehicle_data)
                    st.success(f"✅ Vehicle {make} {model} added successfully!")
                    st.rerun()
                else:
                    st.error("Please fill in all required fields marked with *")
    
    # Display vehicles
    if not vehicles_df.empty:
        st.markdown("### Current Vehicles")
        
        # Create a cleaner display with only essential columns
        display_vehicles = vehicles_df.copy()
        
        # Select and rename columns for better readability
        display_columns = {
            'make': 'Make',
            'model': 'Model', 
            'year': 'Year',
            'license_plate': 'License Plate',
            'fuel_type': 'Fuel Type',
            'status': 'Status',
            'mileage': 'Mileage',
            'weight': 'Weight (t)'
        }
        
        # Filter to only include columns that exist and are useful
        available_cols = [col for col in display_columns.keys() if col in display_vehicles.columns]
        display_vehicles = display_vehicles[available_cols]
        
        # Rename columns for display
        display_vehicles = display_vehicles.rename(columns={col: display_columns[col] for col in available_cols})
        
        # Format numeric columns
        if 'Mileage' in display_vehicles.columns:
            display_vehicles['Mileage'] = display_vehicles['Mileage'].apply(lambda x: f"{x:,}" if pd.notna(x) else "")
        if 'Weight (t)' in display_vehicles.columns:
            display_vehicles['Weight (t)'] = display_vehicles['Weight (t)'].apply(lambda x: f"{x:.1f}" if pd.notna(x) else "")
        
        # Add status styling
        def highlight_status(val):
            if val == 'Active':
                return 'background-color: #4CAF50; color: white; font-weight: bold'
            elif val == 'Maintenance':
                return 'background-color: #FF9800; color: white; font-weight: bold'
            elif val == 'Retired':
                return 'background-color: #f44336; color: white; font-weight: bold'
            return ''
        
        if 'Status' in display_vehicles.columns:
            styled_df = display_vehicles.style.map(highlight_status, subset=['Status'])
            st.dataframe(styled_df, use_container_width=True, hide_index=True)
        else:
            st.dataframe(display_vehicles, use_container_width=True, hide_index=True)
        
        # Edit vehicle functionality
        st.markdown("### Edit Vehicle")
        if not vehicles_df.empty:
            vehicle_options = [f"{row['make']} {row['model']} ({row['license_plate']})" 
                             for _, row in vehicles_df.iterrows()]
            selected_vehicle = st.selectbox("Select Vehicle to Edit", vehicle_options)
            selected_idx = vehicle_options.index(selected_vehicle)
            selected_vehicle_data = vehicles_df.iloc[selected_idx]
            
            with st.expander("✏️ Edit Selected Vehicle"):
                with st.form("edit_vehicle_form"):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        make = st.text_input("Make*", value=selected_vehicle_data.get('make', ''))
                        model = st.text_input("Model*", value=selected_vehicle_data.get('model', ''))
                        year = st.number_input("Year*", min_value=1900, max_value=2030, value=int(selected_vehicle_data.get('year', 2020)))
                        license_plate = st.text_input("License Plate*", value=selected_vehicle_data.get('license_plate', ''))
                        fuel_type = st.selectbox("Fuel Type*", ["Petrol", "Diesel", "Electric", "Hybrid"], 
                                                index=["Petrol", "Diesel", "Electric", "Hybrid"].index(selected_vehicle_data.get('fuel_type', 'Diesel')))
                    
                    with col2:
                        whites_id = st.text_input("Whites ID", value=selected_vehicle_data.get('whites_id', '') if pd.notna(selected_vehicle_data.get('whites_id')) else '')
                        vin_chassis = st.text_input("VIN/Chassis", value=selected_vehicle_data.get('vin_chassis', '') if pd.notna(selected_vehicle_data.get('vin_chassis')) else '')
                        vehicle_type = st.selectbox("Vehicle Type", ["Car", "Van", "Truck", "Lorry", "Bus", "Motorcycle", "Other"], 
                                                   index=["Car", "Van", "Truck", "Lorry", "Bus", "Motorcycle", "Other"].index(selected_vehicle_data.get('vehicle_type', 'Car')) if pd.notna(selected_vehicle_data.get('vehicle_type')) else 0)
                        mileage = st.number_input("Mileage*", min_value=0, value=int(selected_vehicle_data.get('mileage', 0)))
                        weight = st.number_input("Weight (tonnes)*", min_value=0.0, value=float(selected_vehicle_data.get('weight', 1.5)), format="%.1f")
                    
                    with col3:
                        status = st.selectbox("Status*", ["Active", "Maintenance", "Retired"], 
                                             index=["Active", "Maintenance", "Retired"].index(selected_vehicle_data.get('status', 'Active')))
                        defects = st.text_area("Defects", value=selected_vehicle_data.get('defects', '') if pd.notna(selected_vehicle_data.get('defects')) else '')
                        notes = st.text_area("Notes", value=selected_vehicle_data.get('notes', '') if pd.notna(selected_vehicle_data.get('notes')) else '')
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.form_submit_button("Update Vehicle", use_container_width=True):
                            updated_vehicle = selected_vehicle_data.copy()
                            updated_vehicle['make'] = make
                            updated_vehicle['model'] = model
                            updated_vehicle['year'] = year
                            updated_vehicle['license_plate'] = license_plate
                            updated_vehicle['fuel_type'] = fuel_type
                            updated_vehicle['mileage'] = mileage
                            updated_vehicle['weight'] = weight
                            updated_vehicle['status'] = status
                            updated_vehicle['whites_id'] = whites_id if whites_id else None
                            updated_vehicle['vin_chassis'] = vin_chassis if vin_chassis else None
                            updated_vehicle['vehicle_type'] = vehicle_type if vehicle_type else None
                            updated_vehicle['defects'] = defects if defects else None
                            updated_vehicle['notes'] = notes if notes else None
                            
                            dm = get_data_manager()
                            dm.update_vehicle(updated_vehicle)
                            st.success(f"✅ Vehicle {make} {model} updated successfully!")
                            st.rerun()
                    
                    with col2:
                        if st.form_submit_button("Delete Vehicle", use_container_width=True):
                            dm = get_data_manager()
                            dm.delete_vehicle(selected_vehicle_data['vehicle_id'])
                            st.success(f"✅ Vehicle {selected_vehicle_data['make']} {selected_vehicle_data['model']} deleted successfully!")
                            st.rerun()
    else:
        st.info("No vehicles found. Add your first vehicle above.")


def show_maintenance_content(maintenance_df, vehicles_df):
    """Maintenance records content"""
    st.markdown("### 🔧 Maintenance Records")
    
    # Reload data to ensure we have the latest maintenance records
    dm = get_data_manager()
    maintenance_df = dm.load_maintenance()
    vehicles_df = dm.load_vehicles()
    
    # Add new maintenance record
    with st.expander("➕ Add New Maintenance Record"):
        with st.form("add_maintenance_form"):
            col1, col2 = st.columns(2)
            with col1:
                if not vehicles_df.empty:
                    vehicle_options = [f"{row['make']} {row['model']} ({row['license_plate']})" 
                                     for _, row in vehicles_df.iterrows()]
                    selected_vehicle = st.selectbox("Select Vehicle*", vehicle_options)
                    vehicle_id = vehicles_df.iloc[vehicle_options.index(selected_vehicle)]['vehicle_id']
                else:
                    st.warning("No vehicles available. Add vehicles first.")
                    vehicle_id = None
                
                service_type = st.selectbox("Service Type*", [
                    "Oil Change", "Brake Service", "Tire Rotation", "MOT Test", 
                    "Engine Repair", "Transmission Service", "Other"
                ])
                service_date = st.date_input("Service Date*")
            
            with col2:
                cost = st.number_input("Cost (£)*", min_value=0.0, value=50.0, format="%.2f")
                description = st.text_area("Description", placeholder="Service details...")
                next_service_date = st.date_input("Next Service Date")
            
            if st.form_submit_button("Add Maintenance Record", use_container_width=True):
                if vehicle_id and service_type and service_date:
                    maintenance_data = {
                        'vehicle_id': vehicle_id,
                        'service_type': service_type,
                        'service_date': service_date.strftime('%Y-%m-%d'),
                        'cost': cost,
                        'description': description,
                        'next_service_date': next_service_date.strftime('%Y-%m-%d') if next_service_date else ""
                    }
                    dm = get_data_manager()
                    dm.add_maintenance(maintenance_data)
                    st.success(f"✅ Maintenance record added successfully!")
                    st.rerun()
                else:
                    st.error("Please fill in all required fields marked with *")
    
    # Display maintenance records
    if not maintenance_df.empty:
        st.markdown("### Maintenance History")
        
        # Create a cleaner display with only essential columns
        display_maintenance = maintenance_df.copy()
        
        # Map vehicle IDs to readable names
        if not vehicles_df.empty:
            vehicle_map = {row['vehicle_id']: f"{row['make']} {row['model']} ({row['license_plate']})" 
                          for _, row in vehicles_df.iterrows()}
            display_maintenance['vehicle_name'] = display_maintenance['vehicle_id'].map(vehicle_map)
        
        # Select and rename columns for better readability
        display_columns = {
            'vehicle_name': 'Vehicle',
            'service_type': 'Service Type',
            'service_date': 'Service Date',
            'cost': 'Cost',
            'description': 'Description',
            'next_service_date': 'Next Service'
        }
        
        # Use vehicle_id as fallback if vehicle_name mapping failed
        if 'vehicle_name' not in display_maintenance.columns:
            display_columns['vehicle_id'] = 'Vehicle ID'
            del display_columns['vehicle_name']
        
        # Filter to only include columns that exist and are useful
        available_cols = [col for col in display_columns.keys() if col in display_maintenance.columns]
        display_maintenance = display_maintenance[available_cols]
        
        # Rename columns for display
        display_maintenance = display_maintenance.rename(columns={col: display_columns[col] for col in available_cols})
        
        # Format cost column
        if 'Cost' in display_maintenance.columns:
            display_maintenance['Cost'] = display_maintenance['Cost'].apply(lambda x: f"£{x:,.2f}" if pd.notna(x) else "")
        
        # Format date columns
        for date_col in ['Service Date', 'Next Service']:
            if date_col in display_maintenance.columns:
                display_maintenance[date_col] = display_maintenance[date_col].apply(
                    lambda x: x if pd.notna(x) and x != '' else ""
                )
        
        # Truncate description for better display
        if 'Description' in display_maintenance.columns:
            display_maintenance['Description'] = display_maintenance['Description'].apply(
                lambda x: (x[:50] + "...") if isinstance(x, str) and len(x) > 50 else (x if pd.notna(x) else "")
            )
        
        st.dataframe(display_maintenance, use_container_width=True, hide_index=True)
    else:
        st.info("No maintenance records found. Add your first record above.")


def show_dashboard_content(vehicles_df, maintenance_df, equipment_df, rentals_df):
    """Dashboard content with metrics and charts"""
    st.markdown("### 📊 Dashboard Overview")
    
    # Load machines data
    dm = get_data_manager()
    machines_df = dm.load_machines()
    
    # Metrics - reordered to vehicles, machines, tool hire
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        active_vehicles = len(vehicles_df[vehicles_df['status'] == 'Active']) if not vehicles_df.empty else 0
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #2196f3 0%, #1976d2 100%);
            color: white;
            border-radius: 12px;
            padding: 1.5rem;
            text-align: center;
            box-shadow: 0 4px 15px rgba(33, 150, 243, 0.3);
            border: 1px solid rgba(255, 255, 255, 0.1);
            transition: all 0.3s ease;
        ">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">🚗</div>
            <div style="font-size: 1.8rem; font-weight: 700; margin-bottom: 0.3rem;">{len(vehicles_df)}</div>
            <div style="font-size: 1rem; font-weight: 500; opacity: 0.9;">Total Vehicles</div>
            <div style="font-size: 0.9rem; margin-top: 0.5rem; opacity: 0.8;">↑ {active_vehicles} Active</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        active_machines = len(machines_df[machines_df['status'] == 'Active']) if not machines_df.empty else 0
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #2196f3 0%, #1976d2 100%);
            color: white;
            border-radius: 12px;
            padding: 1.5rem;
            text-align: center;
            box-shadow: 0 4px 15px rgba(33, 150, 243, 0.3);
            border: 1px solid rgba(255, 255, 255, 0.1);
            transition: all 0.3s ease;
        ">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">🏗️</div>
            <div style="font-size: 1.8rem; font-weight: 700; margin-bottom: 0.3rem;">{len(machines_df)}</div>
            <div style="font-size: 1rem; font-weight: 500; opacity: 0.9;">Total Machines</div>
            <div style="font-size: 0.9rem; margin-top: 0.5rem; opacity: 0.8;">↑ {active_machines} Active</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        available_equipment = len(equipment_df[equipment_df['status'] == 'Available']) if not equipment_df.empty else 0
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #2196f3 0%, #1976d2 100%);
            color: white;
            border-radius: 12px;
            padding: 1.5rem;
            text-align: center;
            box-shadow: 0 4px 15px rgba(33, 150, 243, 0.3);
            border: 1px solid rgba(255, 255, 255, 0.1);
            transition: all 0.3s ease;
        ">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">⚙️</div>
            <div style="font-size: 1.8rem; font-weight: 700; margin-bottom: 0.3rem;">{len(equipment_df)}</div>
            <div style="font-size: 1rem; font-weight: 500; opacity: 0.9;">Tool Hire</div>
            <div style="font-size: 0.9rem; margin-top: 0.5rem; opacity: 0.8;">↑ {available_equipment} Available</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        total_maintenance_cost = maintenance_df['cost'].sum() if not maintenance_df.empty else 0
        maintenance_records = len(maintenance_df)
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #2196f3 0%, #1976d2 100%);
            color: white;
            border-radius: 12px;
            padding: 1.5rem;
            text-align: center;
            box-shadow: 0 4px 15px rgba(33, 150, 243, 0.3);
            border: 1px solid rgba(255, 255, 255, 0.1);
            transition: all 0.3s ease;
        ">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">💰</div>
            <div style="font-size: 1.8rem; font-weight: 700; margin-bottom: 0.3rem;">£{total_maintenance_cost:,.0f}</div>
            <div style="font-size: 1rem; font-weight: 500; opacity: 0.9;">Maintenance</div>
            <div style="font-size: 0.9rem; margin-top: 0.5rem; opacity: 0.8;">↑ {maintenance_records} Records</div>
        </div>
        """, unsafe_allow_html=True)
    



def show_tool_hire_content(equipment_df, rentals_df):
    """Tool hire content"""
    st.markdown("### ⚙️ Tool Hire Management")
    
    # Reload data to ensure we have the latest equipment
    dm = get_data_manager()
    equipment_df = dm.load_equipment()
    rentals_df = dm.load_rentals()
    
    # Add new equipment
    with st.expander("➕ Add New Equipment"):
        with st.form("add_equipment_form"):
            col1, col2, col3 = st.columns(3)
            with col1:
                name = st.text_input("Equipment Name*", placeholder="Excavator")
                category = st.selectbox("Category*", [
                    "Excavation", "Lifting", "Cutting", "Drilling", 
                    "Measuring", "Safety", "Other"
                ])
                brand = st.text_input("Brand", placeholder="Caterpillar")
                model = st.text_input("Model", placeholder="320D")
                serial_number = st.text_input("Serial Number", placeholder="SN123456")
            
            with col2:
                daily_rate = st.number_input("Daily Rate (£)*", min_value=0.0, value=50.0, format="%.2f")
                weekly_rate = st.number_input("Weekly Rate (£)", min_value=0.0, value=0.0, format="%.2f")
                purchase_price = st.number_input("Purchase Price (£)", min_value=0.0, value=0.0, format="%.2f")
                purchase_date = st.date_input("Purchase Date", value=None)
                last_service_date = st.date_input("Last Service Date", value=None)
            
            with col3:
                status = st.selectbox("Status*", ["Available", "Rented", "Maintenance", "Retired"])
                description = st.text_area("Description", placeholder="Equipment details...")
                notes = st.text_area("Notes", placeholder="Additional notes...")
            
            if st.form_submit_button("Add Equipment", use_container_width=True):
                if name and category:
                    equipment_data = {
                        'name': name,
                        'category': category,
                        'daily_rate': daily_rate,
                        'status': status,
                        'brand': brand if brand else None,
                        'model': model if model else None,
                        'serial_number': serial_number if serial_number else None,
                        'weekly_rate': weekly_rate if weekly_rate > 0 else None,
                        'purchase_price': purchase_price if purchase_price > 0 else None,
                        'purchase_date': purchase_date.strftime('%Y-%m-%d') if purchase_date else None,
                        'last_service_date': last_service_date.strftime('%Y-%m-%d') if last_service_date else None,
                        'description': description if description else None,
                        'notes': notes if notes else None
                    }
                    dm = get_data_manager()
                    dm.add_equipment(equipment_data)
                    st.success(f"✅ Equipment {name} added successfully!")
                    st.rerun()
                else:
                    st.error("Please fill in all required fields marked with *")
    
    # Display equipment
    if not equipment_df.empty:
        st.markdown("### Equipment Inventory")
        
        # Create a cleaner display with only essential columns
        display_equipment = equipment_df.copy()
        
        # Select and rename columns for better readability
        display_columns = {
            'name': 'Equipment Name',
            'category': 'Category',
            'daily_rate': 'Daily Rate',
            'status': 'Status',
            'brand': 'Brand',
            'model': 'Model',
            'description': 'Description'
        }
        
        # Filter to only include columns that exist and are useful
        available_cols = [col for col in display_columns.keys() if col in display_equipment.columns]
        display_equipment = display_equipment[available_cols]
        
        # Rename columns for display
        display_equipment = display_equipment.rename(columns={col: display_columns[col] for col in available_cols})
        
        # Format daily rate column
        if 'Daily Rate' in display_equipment.columns:
            display_equipment['Daily Rate'] = display_equipment['Daily Rate'].apply(lambda x: f"£{x:,.2f}" if pd.notna(x) else "")
        
        # Truncate description for better display
        if 'Description' in display_equipment.columns:
            display_equipment['Description'] = display_equipment['Description'].apply(
                lambda x: (x[:40] + "...") if isinstance(x, str) and len(x) > 40 else (x if pd.notna(x) else "")
            )
        
        # Clean up None values
        display_equipment = display_equipment.fillna("")
        
        # Add status styling
        def highlight_status(val):
            if val == 'Available':
                return 'background-color: #4CAF50; color: white; font-weight: bold'
            elif val == 'Rented':
                return 'background-color: #FF9800; color: white; font-weight: bold'
            elif val == 'Maintenance':
                return 'background-color: #f44336; color: white; font-weight: bold'
            elif val == 'Retired':
                return 'background-color: #666666; color: white; font-weight: bold'
            return ''
        
        if 'Status' in display_equipment.columns:
            styled_df = display_equipment.style.map(highlight_status, subset=['Status'])
            st.dataframe(styled_df, use_container_width=True, hide_index=True)
        else:
            st.dataframe(display_equipment, use_container_width=True, hide_index=True)
        
        # Edit equipment functionality
        st.markdown("### Edit Equipment")
        equipment_options = [f"{row['name']} ({row['category']})" 
                           for _, row in equipment_df.iterrows()]
        selected_equipment = st.selectbox("Select Equipment to Edit", equipment_options)
        selected_idx = equipment_options.index(selected_equipment)
        selected_equipment_data = equipment_df.iloc[selected_idx]
        
        with st.expander("✏️ Edit Selected Equipment"):
            with st.form("edit_equipment_form"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    name = st.text_input("Equipment Name*", value=selected_equipment_data.get('name', ''))
                    category = st.selectbox("Category*", [
                        "Excavation", "Lifting", "Cutting", "Drilling", 
                        "Measuring", "Safety", "Other"
                    ], index=["Excavation", "Lifting", "Cutting", "Drilling", "Measuring", "Safety", "Other"].index(selected_equipment_data.get('category', 'Other')))
                    brand = st.text_input("Brand", value=selected_equipment_data.get('brand', '') if pd.notna(selected_equipment_data.get('brand')) else '')
                    model = st.text_input("Model", value=selected_equipment_data.get('model', '') if pd.notna(selected_equipment_data.get('model')) else '')
                    serial_number = st.text_input("Serial Number", value=selected_equipment_data.get('serial_number', '') if pd.notna(selected_equipment_data.get('serial_number')) else '')
                
                with col2:
                    daily_rate = st.number_input("Daily Rate (£)*", min_value=0.0, value=float(selected_equipment_data.get('daily_rate', 0)), format="%.2f")
                    weekly_rate = st.number_input("Weekly Rate (£)", min_value=0.0, value=float(selected_equipment_data.get('weekly_rate', 0)) if pd.notna(selected_equipment_data.get('weekly_rate')) else 0.0, format="%.2f")
                    purchase_price = st.number_input("Purchase Price (£)", min_value=0.0, value=float(selected_equipment_data.get('purchase_price', 0)) if pd.notna(selected_equipment_data.get('purchase_price')) else 0.0, format="%.2f")
                    
                    # Handle date inputs
                    purchase_date = selected_equipment_data.get('purchase_date')
                    if pd.notna(purchase_date) and purchase_date:
                        try:
                            purchase_date_val = pd.to_datetime(purchase_date).date()
                        except:
                            purchase_date_val = None
                    else:
                        purchase_date_val = None
                    purchase_date_input = st.date_input("Purchase Date", value=purchase_date_val)
                    
                    last_service_date = selected_equipment_data.get('last_service_date')
                    if pd.notna(last_service_date) and last_service_date:
                        try:
                            last_service_date_val = pd.to_datetime(last_service_date).date()
                        except:
                            last_service_date_val = None
                    else:
                        last_service_date_val = None
                    last_service_date_input = st.date_input("Last Service Date", value=last_service_date_val)
                
                with col3:
                    status = st.selectbox("Status*", ["Available", "Rented", "Maintenance", "Retired"], 
                                         index=["Available", "Rented", "Maintenance", "Retired"].index(selected_equipment_data.get('status', 'Available')))
                    description = st.text_area("Description", value=selected_equipment_data.get('description', '') if pd.notna(selected_equipment_data.get('description')) else '')
                    notes = st.text_area("Notes", value=selected_equipment_data.get('notes', '') if pd.notna(selected_equipment_data.get('notes')) else '')
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.form_submit_button("Update Equipment", use_container_width=True):
                        updated_equipment = selected_equipment_data.copy()
                        updated_equipment['name'] = name
                        updated_equipment['category'] = category
                        updated_equipment['daily_rate'] = daily_rate
                        updated_equipment['status'] = status
                        updated_equipment['brand'] = brand if brand else None
                        updated_equipment['model'] = model if model else None
                        updated_equipment['serial_number'] = serial_number if serial_number else None
                        updated_equipment['weekly_rate'] = weekly_rate if weekly_rate > 0 else None
                        updated_equipment['purchase_price'] = purchase_price if purchase_price > 0 else None
                        updated_equipment['purchase_date'] = purchase_date_input.strftime('%Y-%m-%d') if purchase_date_input else None
                        updated_equipment['last_service_date'] = last_service_date_input.strftime('%Y-%m-%d') if last_service_date_input else None
                        updated_equipment['description'] = description if description else None
                        updated_equipment['notes'] = notes if notes else None
                        
                        dm = get_data_manager()
                        dm.update_equipment(updated_equipment)
                        st.success(f"✅ Equipment {name} updated successfully!")
                        st.rerun()
                
                with col2:
                    if st.form_submit_button("Delete Equipment", use_container_width=True):
                        dm = get_data_manager()
                        dm.delete_equipment(selected_equipment_data['equipment_id'])
                        st.success(f"✅ Equipment {selected_equipment_data['name']} deleted successfully!")
                        st.rerun()
    else:
        st.info("No equipment found. Add your first equipment above.")


def show_statistics_content(vehicles_df, maintenance_df, equipment_df, rentals_df):
    """Statistics content"""
    st.markdown("### 📈 Statistics & Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Vehicle Statistics")
        if not vehicles_df.empty:
            st.write(f"**Total Vehicles:** {len(vehicles_df)}")
            st.write(f"**Active Vehicles:** {len(vehicles_df[vehicles_df['status'] == 'Active'])}")
            st.write(f"**Average Year:** {vehicles_df['year'].mean():.0f}")
            st.write(f"**Total Mileage:** {vehicles_df['mileage'].sum():,} miles")
        else:
            st.info("No vehicle data available")
    
    with col2:
        st.markdown("#### Maintenance Statistics")
        if not maintenance_df.empty:
            st.write(f"**Total Records:** {len(maintenance_df)}")
            st.write(f"**Total Cost:** £{maintenance_df['cost'].sum():,.2f}")
            st.write(f"**Average Cost:** £{maintenance_df['cost'].mean():.2f}")
            st.write(f"**Most Common Service:** {maintenance_df['service_type'].mode().iloc[0]}")
        else:
            st.info("No maintenance data available")


def show_machine_inventory_content():
    """Machine inventory content"""
    st.markdown("### 🏗️ Machine Inventory (Plant Vehicles)")
    
    # Reload data to ensure we have the latest machines
    dm = get_data_manager()
    machines_df = dm.load_machines()
    
    # Add new machine
    with st.expander("➕ Add New Machine"):
        with st.form("add_machine_form"):
            col1, col2, col3 = st.columns(3)
            with col1:
                make = st.text_input("Make*", placeholder="Caterpillar")
                model = st.text_input("Model*", placeholder="320D")
                year = st.number_input("Year*", min_value=1900, max_value=2030, value=2020)
                serial_number = st.text_input("Serial Number*", placeholder="CAT123456")
                whites_id = st.text_input("Whites ID", placeholder="W001")
            
            with col2:
                machine_type = st.selectbox("Machine Type*", [
                    "Excavator", "Bulldozer", "Loader", "Crane", 
                    "Compactor", "Grader", "Other"
                ])
                hours = st.number_input("Operating Hours*", min_value=0, value=0)
                weight = st.number_input("Weight (tonnes)*", min_value=0.0, value=10.0, format="%.1f")
                vin_chassis = st.text_input("VIN/Chassis", placeholder="VIN123456789")
                status = st.selectbox("Status*", ["Active", "Maintenance", "Retired"])
            
            with col3:
                daily_rate = st.number_input("Daily Rate (£)", min_value=0.0, value=0.0, format="%.2f")
                weekly_rate = st.number_input("Weekly Rate (£)", min_value=0.0, value=0.0, format="%.2f")
                defects = st.text_area("Defects", placeholder="List any known defects...")
                notes = st.text_area("Notes", placeholder="Additional notes...")
            
            if st.form_submit_button("Add Machine", use_container_width=True):
                if make and model and serial_number:
                    machine_data = {
                        'make': make,
                        'model': model,
                        'year': year,
                        'serial_number': serial_number,
                        'machine_type': machine_type,
                        'hours': hours,
                        'weight': weight,
                        'status': status,
                        'whites_id': whites_id if whites_id else None,
                        'vin_chassis': vin_chassis if vin_chassis else None,
                        'daily_rate': daily_rate if daily_rate > 0 else None,
                        'weekly_rate': weekly_rate if weekly_rate > 0 else None,
                        'defects': defects if defects else None,
                        'notes': notes if notes else None
                    }
                    dm.add_machine(machine_data)
                    st.success(f"✅ Machine {make} {model} added successfully!")
                    st.rerun()
                else:
                    st.error("Please fill in all required fields marked with *")
    
    # Display machines
    if not machines_df.empty:
        st.markdown("### Current Machines")
        
        # Create a cleaner display with only essential columns
        display_machines = machines_df.copy()
        
        # Select and rename columns for better readability
        display_columns = {
            'make': 'Make',
            'model': 'Model', 
            'year': 'Year',
            'machine_type': 'Type',
            'status': 'Status',
            'hours': 'Hours',
            'weight': 'Weight (t)',
            'serial_number': 'Serial Number'
        }
        
        # Filter to only include columns that exist and are useful
        available_cols = [col for col in display_columns.keys() if col in display_machines.columns]
        display_machines = display_machines[available_cols]
        
        # Rename columns for display
        display_machines = display_machines.rename(columns={col: display_columns[col] for col in available_cols})
        
        # Format numeric columns
        if 'Hours' in display_machines.columns:
            display_machines['Hours'] = display_machines['Hours'].apply(lambda x: f"{x:,}" if pd.notna(x) else "")
        if 'Weight (t)' in display_machines.columns:
            display_machines['Weight (t)'] = display_machines['Weight (t)'].apply(lambda x: f"{x:.1f}" if pd.notna(x) else "")
        
        # Add status styling
        def highlight_status(val):
            if val == 'Active':
                return 'background-color: #4CAF50; color: white; font-weight: bold'
            elif val == 'Maintenance':
                return 'background-color: #FF9800; color: white; font-weight: bold'
            elif val == 'Retired':
                return 'background-color: #f44336; color: white; font-weight: bold'
            return ''
        
        if 'Status' in display_machines.columns:
            styled_df = display_machines.style.map(highlight_status, subset=['Status'])
            st.dataframe(styled_df, use_container_width=True, hide_index=True)
        else:
            st.dataframe(display_machines, use_container_width=True, hide_index=True)
        
        # Edit machine functionality
        st.markdown("### Edit Machine")
        machine_options = [f"{row['make']} {row['model']} ({row['serial_number']})" 
                          for _, row in machines_df.iterrows()]
        selected_machine = st.selectbox("Select Machine to Edit", machine_options)
        selected_idx = machine_options.index(selected_machine)
        selected_machine_data = machines_df.iloc[selected_idx]
        
        with st.expander("✏️ Edit Selected Machine"):
            with st.form("edit_machine_form"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    make = st.text_input("Make*", value=selected_machine_data.get('make', ''))
                    model = st.text_input("Model*", value=selected_machine_data.get('model', ''))
                    year = st.number_input("Year*", min_value=1900, max_value=2030, value=int(selected_machine_data.get('year', 2020)))
                    serial_number = st.text_input("Serial Number*", value=selected_machine_data.get('serial_number', ''))
                    whites_id = st.text_input("Whites ID", value=selected_machine_data.get('whites_id', '') if pd.notna(selected_machine_data.get('whites_id')) else '')
                
                with col2:
                    machine_type = st.selectbox("Machine Type*", [
                        "Excavator", "Bulldozer", "Loader", "Crane", 
                        "Compactor", "Grader", "Other"
                    ], index=["Excavator", "Bulldozer", "Loader", "Crane", "Compactor", "Grader", "Other"].index(selected_machine_data.get('machine_type', 'Other')))
                    hours = st.number_input("Operating Hours*", min_value=0, value=int(selected_machine_data.get('hours', 0)))
                    weight = st.number_input("Weight (tonnes)*", min_value=0.0, value=float(selected_machine_data.get('weight', 10.0)), format="%.1f")
                    vin_chassis = st.text_input("VIN/Chassis", value=selected_machine_data.get('vin_chassis', '') if pd.notna(selected_machine_data.get('vin_chassis')) else '')
                    status = st.selectbox("Status*", ["Active", "Maintenance", "Retired"], 
                                         index=["Active", "Maintenance", "Retired"].index(selected_machine_data.get('status', 'Active')))
                
                with col3:
                    daily_rate = st.number_input("Daily Rate (£)", min_value=0.0, value=float(selected_machine_data.get('daily_rate', 0)) if pd.notna(selected_machine_data.get('daily_rate')) else 0.0, format="%.2f")
                    weekly_rate = st.number_input("Weekly Rate (£)", min_value=0.0, value=float(selected_machine_data.get('weekly_rate', 0)) if pd.notna(selected_machine_data.get('weekly_rate')) else 0.0, format="%.2f")
                    defects = st.text_area("Defects", value=selected_machine_data.get('defects', '') if pd.notna(selected_machine_data.get('defects')) else '')
                    notes = st.text_area("Notes", value=selected_machine_data.get('notes', '') if pd.notna(selected_machine_data.get('notes')) else '')
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.form_submit_button("Update Machine", use_container_width=True):
                        updated_machine = selected_machine_data.copy()
                        updated_machine['make'] = make
                        updated_machine['model'] = model
                        updated_machine['year'] = year
                        updated_machine['serial_number'] = serial_number
                        updated_machine['machine_type'] = machine_type
                        updated_machine['hours'] = hours
                        updated_machine['weight'] = weight
                        updated_machine['status'] = status
                        updated_machine['whites_id'] = whites_id if whites_id else None
                        updated_machine['vin_chassis'] = vin_chassis if vin_chassis else None
                        updated_machine['daily_rate'] = daily_rate if daily_rate > 0 else None
                        updated_machine['weekly_rate'] = weekly_rate if weekly_rate > 0 else None
                        updated_machine['defects'] = defects if defects else None
                        updated_machine['notes'] = notes if notes else None
                        
                        dm = get_data_manager()
                        dm.update_machine(updated_machine)
                        st.success(f"✅ Machine {make} {model} updated successfully!")
                        st.rerun()
                
                with col2:
                    if st.form_submit_button("Delete Machine", use_container_width=True):
                        dm = get_data_manager()
                        dm.delete_machine(selected_machine_data['machine_id'])
                        st.success(f"✅ Machine {selected_machine_data['make']} {selected_machine_data['model']} deleted successfully!")
                        st.rerun()
    else:
        st.info("No machines found. Add your first machine above.")


def create_excel_export(dataframes, filename):
    """Create Excel export function"""
    import io
    import pandas as pd
    
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        for sheet_name, df in dataframes.items():
            if not df.empty:
                df.to_excel(writer, sheet_name=sheet_name, index=False)
    
    return output.getvalue()


def main():
    """Main application entry point"""
    # Check authentication first
    if not check_password():
        st.stop()
    
    # Modern Dark Theme CSS with Mobile Responsiveness
    st.markdown("""
    <style>
    /* Global Styles */
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        color: #e0e6ed;
        min-height: 100vh;
    }
    
    /* Completely hide sidebar */
    .stSidebar {
        display: none !important;
    }
    
    .stSidebar > div {
        display: none !important;
    }
    
    section[data-testid="stSidebar"] {
        display: none !important;
    }
    
    /* Make main content full width */
    .main .block-container {
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        max-width: 100% !important;
    }
    
    /* Tab Styling */
    .stTabs {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 12px;
        padding: 1rem;
        margin: 1rem 0;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 8px;
        padding: 0.5rem 1rem;
        color: #e0e6ed;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #2196f3 0%, #1976d2 100%);
        color: white;
    }
    
    /* Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, #2196f3 0%, #1976d2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 16px rgba(33, 150, 243, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(33, 150, 243, 0.4);
    }
    
    /* Improved Input Styling for Better Readability */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.95) !important;
        border: 2px solid rgba(33, 150, 243, 0.3) !important;
        border-radius: 8px !important;
        color: #1a1a2e !important;
        font-weight: 500 !important;
        font-size: 14px !important;
        padding: 0.75rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #2196f3 !important;
        box-shadow: 0 0 0 3px rgba(33, 150, 243, 0.2) !important;
        background: rgba(255, 255, 255, 1) !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #666 !important;
        opacity: 0.8 !important;
    }
    
    /* Number Input Styling */
    .stNumberInput > div > div > input {
        background: rgba(255, 255, 255, 0.95) !important;
        border: 2px solid rgba(33, 150, 243, 0.3) !important;
        border-radius: 8px !important;
        color: #1a1a2e !important;
        font-weight: 500 !important;
        font-size: 14px !important;
        padding: 0.75rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stNumberInput > div > div > input:focus {
        border-color: #2196f3 !important;
        box-shadow: 0 0 0 3px rgba(33, 150, 243, 0.2) !important;
        background: rgba(255, 255, 255, 1) !important;
    }
    
    /* Selectbox Styling */
    .stSelectbox > div > div > div {
        background: rgba(255, 255, 255, 0.95) !important;
        border: 2px solid rgba(33, 150, 243, 0.3) !important;
        border-radius: 8px !important;
        color: #1a1a2e !important;
        font-weight: 500 !important;
        font-size: 14px !important;
        padding: 0.5rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stSelectbox > div > div > div:hover {
        border-color: #2196f3 !important;
        background: rgba(255, 255, 255, 1) !important;
    }
    
    /* Date Input Styling */
    .stDateInput > div > div > input {
        background: rgba(255, 255, 255, 0.95) !important;
        border: 2px solid rgba(33, 150, 243, 0.3) !important;
        border-radius: 8px !important;
        color: #1a1a2e !important;
        font-weight: 500 !important;
        font-size: 14px !important;
        padding: 0.75rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stDateInput > div > div > input:focus {
        border-color: #2196f3 !important;
        box-shadow: 0 0 0 3px rgba(33, 150, 243, 0.2) !important;
        background: rgba(255, 255, 255, 1) !important;
    }
    
    /* Text Area Styling */
    .stTextArea > div > div > textarea {
        background: rgba(255, 255, 255, 0.95) !important;
        border: 2px solid rgba(33, 150, 243, 0.3) !important;
        border-radius: 8px !important;
        color: #1a1a2e !important;
        font-weight: 500 !important;
        font-size: 14px !important;
        padding: 0.75rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: #2196f3 !important;
        box-shadow: 0 0 0 3px rgba(33, 150, 243, 0.2) !important;
        background: rgba(255, 255, 255, 1) !important;
    }
    
    .stTextArea > div > div > textarea::placeholder {
        color: #666 !important;
        opacity: 0.8 !important;
    }
    
    /* Form Labels */
    .stTextInput > label, .stNumberInput > label, .stSelectbox > label, .stDateInput > label, .stTextArea > label {
        color: #e0e6ed !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* Metrics Styling */
    .stMetric {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 12px;
        padding: 1.5rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    
    .stMetric:hover {
        transform: translateY(-2px);
        border-color: rgba(33, 150, 243, 0.3);
        box-shadow: 0 4px 20px rgba(33, 150, 243, 0.1);
    }
    
    /* Expander Styling */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 8px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Form styling */
    .stForm {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    
    @media (max-width: 768px) {
        .stApp {
            padding: 0.5rem;
        }
        
        .stTabs [data-baseweb="tab"] {
            padding: 0.375rem 0.75rem;
            font-size: 0.875rem;
        }
        
        .main .block-container {
            padding-left: 0.5rem !important;
            padding-right: 0.5rem !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Load data
    dm = get_data_manager()
    vehicles_df = dm.load_vehicles()
    maintenance_df = dm.load_maintenance()
    equipment_df = dm.load_equipment()
    rentals_df = dm.load_rentals()
    
    # Create single-page navigation and content
    create_single_page_layout(vehicles_df, maintenance_df, equipment_df, rentals_df)


if __name__ == "__main__":
    main()
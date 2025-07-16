import streamlit as st
import pandas as pd
from datetime import datetime, date
import os
from utils.data_manager import DataManager
from login import check_password, show_logout_button, get_current_user, logout
import plotly.express as px

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
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 📥 Quick Export")
        if not vehicles_df.empty:
            excel_vehicles = create_excel_export({"Vehicles": vehicles_df}, "vehicles.xlsx")
            st.download_button(
                label="🚗 Vehicles Excel",
                data=excel_vehicles,
                file_name=f"vehicles_{datetime.now().strftime('%Y%m%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
        
        if not equipment_df.empty:
            excel_equipment = create_excel_export({"Equipment": equipment_df}, "equipment.xlsx")
            st.download_button(
                label="⚙️ Equipment Excel",
                data=excel_equipment,
                file_name=f"equipment_{datetime.now().strftime('%Y%m%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
    
    with col2:
        st.markdown("### 💡 System Info")
        st.info("Offline system using local CSV files. No internet required!")
    
    with col3:
        st.markdown("### 🚪 Account")
        if st.button("🚪 Logout", use_container_width=True):
            logout()


def show_vehicle_inventory_content(vehicles_df):
    """Vehicle inventory content"""
    st.markdown("### 🚗 Vehicle Inventory Management")
    
    # Add new vehicle form
    with st.expander("➕ Add New Vehicle"):
        with st.form("add_vehicle_form"):
            col1, col2 = st.columns(2)
            with col1:
                make = st.text_input("Make*", placeholder="Toyota")
                model = st.text_input("Model*", placeholder="Hilux")
                year = st.number_input("Year*", min_value=1900, max_value=2030, value=2020)
                license_plate = st.text_input("License Plate*", placeholder="ABC123")
            
            with col2:
                fuel_type = st.selectbox("Fuel Type*", ["Petrol", "Diesel", "Electric", "Hybrid"])
                mileage = st.number_input("Mileage*", min_value=0, value=0)
                weight = st.number_input("Weight (tonnes)*", min_value=0.0, value=1.5, format="%.1f")
                status = st.selectbox("Status*", ["Active", "Maintenance", "Retired"])
            
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
                        'status': status
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
        st.dataframe(vehicles_df, use_container_width=True, hide_index=True)
    else:
        st.info("No vehicles found. Add your first vehicle above.")


def show_maintenance_content(maintenance_df, vehicles_df):
    """Maintenance records content"""
    st.markdown("### 🔧 Maintenance Records")
    
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
        display_maintenance = maintenance_df.copy()
        display_maintenance['cost'] = display_maintenance['cost'].apply(lambda x: f"£{x:,.2f}")
        st.dataframe(display_maintenance, use_container_width=True, hide_index=True)
    else:
        st.info("No maintenance records found. Add your first record above.")


def show_dashboard_content(vehicles_df, maintenance_df, equipment_df, rentals_df):
    """Dashboard content with metrics and charts"""
    st.markdown("### 📊 Dashboard Overview")
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="🚗 Total Vehicles",
            value=len(vehicles_df),
            delta=f"{len(vehicles_df[vehicles_df['status'] == 'Active'])} Active" if not vehicles_df.empty else "0 Active"
        )
    
    with col2:
        total_maintenance_cost = maintenance_df['cost'].sum() if not maintenance_df.empty else 0
        st.metric(
            label="💰 Maintenance Cost",
            value=f"£{total_maintenance_cost:,.2f}",
            delta=f"{len(maintenance_df)} Records"
        )
    
    with col3:
        st.metric(
            label="⚙️ Equipment Items",
            value=len(equipment_df),
            delta=f"{len(equipment_df[equipment_df['status'] == 'Available'])} Available" if not equipment_df.empty else "0 Available"
        )
    
    with col4:
        total_rental_revenue = rentals_df['rental_rate'].sum() if not rentals_df.empty else 0
        st.metric(
            label="💵 Rental Revenue",
            value=f"£{total_rental_revenue:,.2f}",
            delta=f"{len(rentals_df)} Rentals"
        )
    
    # Charts
    if not vehicles_df.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Vehicle Status Distribution")
            status_counts = vehicles_df['status'].value_counts()
            fig = px.pie(values=status_counts.values, names=status_counts.index, 
                        title="Vehicle Status Distribution")
            fig.update_layout(template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### Fuel Type Distribution")
            fuel_counts = vehicles_df['fuel_type'].value_counts()
            fig = px.bar(x=fuel_counts.index, y=fuel_counts.values, 
                        title="Fuel Type Distribution")
            fig.update_layout(template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)


def show_tool_hire_content(equipment_df, rentals_df):
    """Tool hire content"""
    st.markdown("### ⚙️ Tool Hire Management")
    
    # Add new equipment
    with st.expander("➕ Add New Equipment"):
        with st.form("add_equipment_form"):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Equipment Name*", placeholder="Excavator")
                category = st.selectbox("Category*", [
                    "Excavation", "Lifting", "Cutting", "Drilling", 
                    "Measuring", "Safety", "Other"
                ])
                daily_rate = st.number_input("Daily Rate (£)*", min_value=0.0, value=50.0, format="%.2f")
            
            with col2:
                description = st.text_area("Description", placeholder="Equipment details...")
                status = st.selectbox("Status*", ["Available", "Rented", "Maintenance", "Retired"])
            
            if st.form_submit_button("Add Equipment", use_container_width=True):
                if name and category:
                    equipment_data = {
                        'name': name,
                        'category': category,
                        'daily_rate': daily_rate,
                        'description': description,
                        'status': status
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
        display_equipment = equipment_df.copy()
        display_equipment['daily_rate'] = display_equipment['daily_rate'].apply(lambda x: f"£{x:,.2f}")
        st.dataframe(display_equipment, use_container_width=True, hide_index=True)
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
    
    dm = get_data_manager()
    machines_df = dm.load_machines()
    
    # Add new machine
    with st.expander("➕ Add New Machine"):
        with st.form("add_machine_form"):
            col1, col2 = st.columns(2)
            with col1:
                make = st.text_input("Make*", placeholder="Caterpillar")
                model = st.text_input("Model*", placeholder="320D")
                year = st.number_input("Year*", min_value=1900, max_value=2030, value=2020)
                serial_number = st.text_input("Serial Number*", placeholder="CAT123456")
            
            with col2:
                machine_type = st.selectbox("Machine Type*", [
                    "Excavator", "Bulldozer", "Loader", "Crane", 
                    "Compactor", "Grader", "Other"
                ])
                hours = st.number_input("Operating Hours*", min_value=0, value=0)
                weight = st.number_input("Weight (tonnes)*", min_value=0.0, value=10.0, format="%.1f")
                status = st.selectbox("Status*", ["Active", "Maintenance", "Retired"])
            
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
                        'status': status
                    }
                    dm.add_machine(machine_data)
                    st.success(f"✅ Machine {make} {model} added successfully!")
                    st.rerun()
                else:
                    st.error("Please fill in all required fields marked with *")
    
    # Display machines
    if not machines_df.empty:
        st.markdown("### Current Machines")
        st.dataframe(machines_df, use_container_width=True, hide_index=True)
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
    # Set page configuration
    st.set_page_config(
        page_title="Whites Management System",
        page_icon="🚗",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
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
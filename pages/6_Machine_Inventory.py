import streamlit as st
import pandas as pd
from datetime import datetime, date
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.data_manager import DataManager
from utils.validators import validate_weight, validate_year

st.set_page_config(
    page_title="Machine Inventory", 
    page_icon="🏗️", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize data manager
@st.cache_resource
def get_data_manager():
    return DataManager()

def create_sidebar():
    """Create permanent sidebar navigation"""
    with st.sidebar:
        st.title("🚗 Whites Management")
        
        # Navigation Section
        st.markdown("### 📍 Navigation")
        
        # Main Navigation
        if st.button("🚗 Vehicle Inventory", use_container_width=True):
            st.switch_page("pages/1_Vehicle_Inventory.py")
        if st.button("🏗️ Machine Inventory", use_container_width=True, disabled=True):
            pass  # Current page
        if st.button("⚙️ Tool Hire", use_container_width=True):
            st.switch_page("pages/4_Tool_Hire.py")
        if st.button("📊 Dashboard", use_container_width=True):
            st.switch_page("pages/3_Dashboard.py")
        if st.button("📈 Statistics", use_container_width=True):
            st.switch_page("pages/5_Statistics.py")
        
        # Maintenance & Records
        st.markdown("**Maintenance & Records**")
        if st.button("🔧 Maintenance Records", use_container_width=True):
            st.switch_page("pages/2_Maintenance_Records.py")
        
        # Home
        st.markdown("**Home**")
        if st.button("🏠 Home", use_container_width=True):
            st.switch_page("app.py")
        
        st.markdown("---")
        st.markdown("### 💡 System Info")
        st.info("Offline system using local CSV files. No internet required!")

def main():
    # Custom CSS for better styling
    st.markdown("""
    <style>
    .page-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f77b4;
        margin-bottom: 1rem;
        text-align: center;
    }
    .machine-card {
        background: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .section-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #343a40;
        margin: 1.5rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #1f77b4;
    }
    .filter-section {
        background: #e9ecef;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
    .status-active {
        background-color: #d4edda;
        color: #155724;
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
        font-weight: bold;
    }
    .status-inactive {
        background-color: #f8d7da;
        color: #721c24;
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
        font-weight: bold;
    }
    .status-maintenance {
        background-color: #fff3cd;
        color: #856404;
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
        font-weight: bold;
    }
    .form-section {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

    create_sidebar()

    # Page header
    st.markdown('<div class="page-header">🏗️ Plant Machine Inventory</div>', unsafe_allow_html=True)
    st.markdown("---")

    data_manager = get_data_manager()
    machines_df = data_manager.load_machines()

    # Create tabs for different sections
    tab1, tab2, tab3, tab4 = st.tabs(["📋 View Machines", "➕ Add Machine", "📊 Quick Stats", "📥 Import/Export"])

    with tab1:
        st.markdown('<div class="section-header">Machine Inventory</div>', unsafe_allow_html=True)
        
        # Filter section
        with st.container():
            st.markdown('<div class="filter-section">', unsafe_allow_html=True)
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                status_filter = st.selectbox("Filter by Status", ["All", "Active", "Inactive", "Under Maintenance"])
            
            with col2:
                make_options = ["All"] + list(machines_df['make'].unique()) if not machines_df.empty else ["All"]
                make_filter = st.selectbox("Filter by Make", make_options)
            
            with col3:
                type_options = ["All"] + list(machines_df['machine_type'].unique()) if not machines_df.empty else ["All"]
                type_filter = st.selectbox("Filter by Type", type_options)
            
            with col4:
                search_term = st.text_input("Search (Whites ID, Make, Model)")
            
            st.markdown('</div>', unsafe_allow_html=True)

        # Apply filters
        filtered_df = machines_df.copy()
        
        if status_filter != "All":
            filtered_df = filtered_df[filtered_df['status'] == status_filter]
        
        if make_filter != "All":
            filtered_df = filtered_df[filtered_df['make'] == make_filter]
        
        if type_filter != "All":
            filtered_df = filtered_df[filtered_df['machine_type'] == type_filter]
        
        if search_term:
            mask = (
                filtered_df['whites_id'].astype(str).str.contains(search_term, case=False, na=False) |
                filtered_df['make'].astype(str).str.contains(search_term, case=False, na=False) |
                filtered_df['model'].astype(str).str.contains(search_term, case=False, na=False)
            )
            filtered_df = filtered_df[mask]

        # Display machines
        if filtered_df.empty:
            st.info("No machines found matching your criteria.")
        else:
            st.write(f"Showing {len(filtered_df)} of {len(machines_df)} machines")
            
            for _, machine in filtered_df.iterrows():
                with st.container():
                    st.markdown(f'<div class="machine-card">', unsafe_allow_html=True)
                    
                    col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
                    
                    with col1:
                        st.write(f"**Whites ID:** {machine['whites_id']}")
                        st.write(f"**Make/Model:** {machine['make']} {machine['model']}")
                        st.write(f"**Type:** {machine['machine_type']}")
                    
                    with col2:
                        st.write(f"**Year:** {machine['year']}")
                        st.write(f"**Weight:** {machine['weight']} tonnes")
                        st.write(f"**Hours:** {machine['hours']:,.0f}")
                        if machine.get('daily_rate') and machine['daily_rate'] > 0:
                            st.write(f"**Daily Rate:** £{machine['daily_rate']:.2f}")
                        if machine.get('weekly_rate') and machine['weekly_rate'] > 0:
                            st.write(f"**Weekly Rate:** £{machine['weekly_rate']:.2f}")
                    
                    with col3:
                        st.write(f"**VIN/Chassis:** {machine['vin_chassis']}")
                        status_class = f"status-{machine['status'].lower().replace(' ', '-').replace('under-maintenance', 'maintenance')}"
                        st.markdown(f'<span class="{status_class}">Status: {machine["status"]}</span>', unsafe_allow_html=True)
                        if machine['defects']:
                            st.write(f"**Defects:** {machine['defects']}")
                    
                    with col4:
                        if st.button("Edit", key=f"edit_{machine['machine_id']}"):
                            st.session_state.edit_machine = machine.to_dict()
                        if st.button("Delete", key=f"delete_{machine['machine_id']}", type="secondary"):
                            if st.session_state.get(f"confirm_delete_{machine['machine_id']}", False):
                                data_manager.delete_machine(machine['machine_id'])
                                st.success("Machine deleted successfully!")
                                st.rerun()
                            else:
                                st.session_state[f"confirm_delete_{machine['machine_id']}"] = True
                                st.warning("Click delete again to confirm")
                    
                    st.markdown('</div>', unsafe_allow_html=True)

        # Edit machine form
        if 'edit_machine' in st.session_state:
            st.markdown('<div class="section-header">Edit Machine</div>', unsafe_allow_html=True)
            machine = st.session_state.edit_machine
            
            with st.form("edit_machine_form"):
                st.markdown('<div class="form-section">', unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    whites_id = st.text_input("Whites ID *", value=machine['whites_id'])
                    make = st.text_input("Make *", value=machine['make'])
                    model = st.text_input("Model *", value=machine['model'])
                    year = st.number_input("Year *", min_value=1900, max_value=datetime.now().year + 1, value=int(machine['year']))
                    weight = st.number_input("Weight (tonnes) *", min_value=0.1, step=0.1, value=float(machine['weight']))
                    vin_chassis = st.text_input("VIN/Chassis Number", value=machine['vin_chassis'])
                    daily_rate = st.number_input("Daily Rate (£)", min_value=0.0, step=0.01, value=float(machine.get('daily_rate', 0.0)), format="%.2f")
                    weekly_rate = st.number_input("Weekly Rate (£)", min_value=0.0, step=0.01, value=float(machine.get('weekly_rate', 0.0)), format="%.2f")
                
                with col2:
                    # Machine type with custom option
                    existing_types = ["Excavator", "Bulldozer", "Crane", "Forklift", "Loader", "Compactor", "Generator", "Telehandler", "Dumper", "Roller", "Other"]
                    current_type = machine['machine_type']
                    if current_type not in existing_types:
                        existing_types.append(current_type)
                    
                    type_option = st.selectbox("Machine Type *", existing_types + ["Add Custom..."], 
                                             index=existing_types.index(current_type) if current_type in existing_types else len(existing_types)-1)
                    
                    if type_option == "Add Custom...":
                        machine_type = st.text_input("Custom Machine Type *")
                    else:
                        machine_type = type_option
                    status = st.selectbox("Status *", 
                        ["Active", "Inactive", "Under Maintenance"],
                        index=["Active", "Inactive", "Under Maintenance"].index(machine['status'])
                    )
                    hours = st.number_input("Operating Hours", min_value=0, value=int(machine['hours']))
                    defects = st.text_area("Defects/Issues", value=machine['defects'] if machine['defects'] else "")
                    notes = st.text_area("Notes", value=machine['notes'] if machine['notes'] else "")
                
                st.markdown('</div>', unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.form_submit_button("Update Machine", type="primary"):
                        if not machine_type:
                            st.error("Please select or enter a machine type")
                        else:
                            updated_machine = {
                            'machine_id': machine['machine_id'],
                            'whites_id': whites_id,
                            'vin_chassis': vin_chassis,
                            'make': make,
                            'model': model,
                            'year': year,
                            'weight': weight,
                            'machine_type': machine_type,
                            'daily_rate': daily_rate,
                            'weekly_rate': weekly_rate,
                            'status': status,
                            'hours': hours,
                            'defects': defects,
                            'notes': notes
                        }
                        
                            data_manager.update_machine(updated_machine)
                            st.success("Machine updated successfully!")
                            del st.session_state.edit_machine
                            st.rerun()
                
                with col2:
                    if st.form_submit_button("Cancel"):
                        del st.session_state.edit_machine
                        st.rerun()

    with tab2:
        st.markdown('<div class="section-header">Add New Machine</div>', unsafe_allow_html=True)
        
        with st.form("add_machine_form"):
            st.markdown('<div class="form-section">', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                whites_id = st.text_input("Whites ID *")
                make = st.text_input("Make *")
                model = st.text_input("Model *")
                year = st.number_input("Year *", min_value=1900, max_value=datetime.now().year + 1, value=datetime.now().year)
                weight = st.number_input("Weight (tonnes) *", min_value=0.1, step=0.1, value=1.0)
                vin_chassis = st.text_input("VIN/Chassis Number")
                daily_rate = st.number_input("Daily Rate (£)", min_value=0.0, step=0.01, value=0.0, format="%.2f")
                weekly_rate = st.number_input("Weekly Rate (£)", min_value=0.0, step=0.01, value=0.0, format="%.2f")
            
            with col2:
                machine_types = ["Excavator", "Bulldozer", "Crane", "Forklift", "Loader", "Compactor", "Generator", "Telehandler", "Dumper", "Roller", "Other"]
                type_option = st.selectbox("Machine Type *", machine_types + ["Add Custom..."])
                
                if type_option == "Add Custom...":
                    machine_type = st.text_input("Custom Machine Type *")
                else:
                    machine_type = type_option
                
                status = st.selectbox("Status *", ["Active", "Inactive", "Under Maintenance"], index=0)
                hours = st.number_input("Operating Hours", min_value=0, value=0)
                defects = st.text_area("Defects/Issues")
                notes = st.text_area("Notes")
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            if st.form_submit_button("Add Machine", type="primary"):
                if not all([whites_id, make, model, machine_type]):
                    st.error("Please fill in all required fields marked with *")
                else:
                    # Validate inputs
                    weight_valid, weight_msg = validate_weight(weight)
                    year_valid, year_msg = validate_year(year)
                    
                    if not weight_valid:
                        st.error(weight_msg)
                    elif not year_valid:
                        st.error(year_msg)
                    else:
                        machine_data = {
                            'whites_id': whites_id,
                            'vin_chassis': vin_chassis,
                            'make': make,
                            'model': model,
                            'year': year,
                            'weight': weight,
                            'machine_type': machine_type,
                            'daily_rate': daily_rate,
                            'weekly_rate': weekly_rate,
                            'status': status,
                            'hours': hours,
                            'defects': defects,
                            'notes': notes
                        }
                        
                        machine_id = data_manager.add_machine(machine_data)
                        st.success(f"Machine added successfully! Machine ID: {machine_id}")
                        st.rerun()

    with tab3:
        st.markdown('<div class="section-header">Quick Statistics</div>', unsafe_allow_html=True)
        
        if machines_df.empty:
            st.info("No machine data available yet.")
        else:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                total_machines = len(machines_df)
                st.metric("Total Machines", total_machines)
            
            with col2:
                active_machines = len(machines_df[machines_df['status'] == 'Active'])
                st.metric("Active Machines", active_machines)
            
            with col3:
                avg_hours = machines_df['hours'].mean() if not machines_df.empty else 0
                st.metric("Average Hours", f"{avg_hours:,.0f}")
            
            with col4:
                machines_with_rates = machines_df[(machines_df.get('daily_rate', 0) > 0) | (machines_df.get('weekly_rate', 0) > 0)]
                rentable_machines = len(machines_with_rates)
                st.metric("Rentable Machines", rentable_machines)
            
            # Status distribution
            st.markdown('<div class="section-header">Status Distribution</div>', unsafe_allow_html=True)
            status_counts = machines_df['status'].value_counts()
            st.bar_chart(status_counts)
            
            # Machine type distribution
            st.markdown('<div class="section-header">Machine Type Distribution</div>', unsafe_allow_html=True)
            type_counts = machines_df['machine_type'].value_counts()
            st.bar_chart(type_counts)
            
            # Rental rates summary
            if not machines_df.empty and 'daily_rate' in machines_df.columns:
                st.markdown('<div class="section-header">Rental Rates Summary</div>', unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    avg_daily = machines_df[machines_df['daily_rate'] > 0]['daily_rate'].mean() if len(machines_df[machines_df['daily_rate'] > 0]) > 0 else 0
                    st.metric("Average Daily Rate", f"£{avg_daily:.2f}")
                
                with col2:
                    avg_weekly = machines_df[machines_df['weekly_rate'] > 0]['weekly_rate'].mean() if len(machines_df[machines_df['weekly_rate'] > 0]) > 0 else 0
                    st.metric("Average Weekly Rate", f"£{avg_weekly:.2f}")
                
                with col3:
                    total_potential_daily = machines_df[machines_df['daily_rate'] > 0]['daily_rate'].sum()
                    st.metric("Total Daily Potential", f"£{total_potential_daily:.2f}")
                
                # Top rental rates
                machines_with_rates = machines_df[machines_df['daily_rate'] > 0].copy()
                if not machines_with_rates.empty:
                    st.markdown("**Top Daily Rates:**")
                    top_machines = machines_with_rates.nlargest(5, 'daily_rate')[['whites_id', 'make', 'model', 'machine_type', 'daily_rate']]
                    for _, machine in top_machines.iterrows():
                        st.write(f"• {machine['whites_id']} - {machine['make']} {machine['model']} ({machine['machine_type']}): £{machine['daily_rate']:.2f}/day")

    with tab4:
        st.markdown('<div class="section-header">Import/Export Data</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Export Data")
            
            if not machines_df.empty:
                # CSV Export
                csv_data = machines_df.to_csv(index=False)
                st.download_button(
                    label="Download as CSV",
                    data=csv_data,
                    file_name=f"whites_machines_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
                
                # Excel Export
                from io import BytesIO
                excel_buffer = BytesIO()
                with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                    machines_df.to_excel(writer, sheet_name='Machines', index=False)
                excel_data = excel_buffer.getvalue()
                
                st.download_button(
                    label="Download as Excel",
                    data=excel_data,
                    file_name=f"whites_machines_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            else:
                st.info("No machine data to export.")
        
        with col2:
            st.subheader("Import Data")
            
            uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
            
            if uploaded_file is not None:
                try:
                    import_df = pd.read_csv(uploaded_file)
                    st.write("Preview of uploaded data:")
                    st.dataframe(import_df.head())
                    
                    if st.button("Import Machines"):
                        # Add import functionality for machines
                        success_count = 0
                        for _, row in import_df.iterrows():
                            try:
                                machine_data = row.to_dict()
                                data_manager.add_machine(machine_data)
                                success_count += 1
                            except Exception as e:
                                st.error(f"Error importing machine: {e}")
                        
                        st.success(f"Successfully imported {success_count} machines!")
                        st.rerun()
                        
                except Exception as e:
                    st.error(f"Error reading file: {e}")

if __name__ == "__main__":
    main()
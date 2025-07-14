import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.data_manager import DataManager

st.set_page_config(
    page_title="Tool Hire", 
    page_icon="🔧", 
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
        
        # Fleet Management
        st.markdown("**Fleet Management**")
        if st.button("🚗 Vehicle Inventory", use_container_width=True):
            st.switch_page("pages/1_Vehicle_Inventory.py")
        if st.button("🔧 Maintenance Records", use_container_width=True):
            st.switch_page("pages/2_Maintenance_Records.py")
        
        # Equipment & Rentals
        st.markdown("**Equipment & Rentals**")
        if st.button("⚙️ Equipment Hire", use_container_width=True, disabled=True):
            pass  # Current page
        
        # Analytics & Reports
        st.markdown("**Analytics & Reports**")
        if st.button("📊 Dashboard", use_container_width=True):
            st.switch_page("pages/3_Dashboard.py")
        if st.button("📈 Statistics", use_container_width=True):
            st.switch_page("pages/5_Statistics.py")
        
        # Home
        st.markdown("**Home**")
        if st.button("🏠 Home", use_container_width=True):
            st.switch_page("app.py")
        
        st.markdown("---")
        st.markdown("### 💡 System Info")
        st.info("Offline system using local CSV files. No internet required!")

def main():
    # Custom CSS for tool hire page
    st.markdown("""
    <style>
    .tool-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f77b4;
        margin-bottom: 1rem;
        text-align: center;
    }
    .equipment-card {
        background: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        border-left: 4px solid #28a745;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .rental-card {
        background: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        border-left: 4px solid #17a2b8;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .status-available {
        background: #28a745;
        color: white;
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .status-rented {
        background: #dc3545;
        color: white;
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .status-maintenance {
        background: #ffc107;
        color: #212529;
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .section-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #333;
        margin: 2rem 0 1rem 0;
        border-bottom: 2px solid #1f77b4;
        padding-bottom: 0.5rem;
    }
    .filter-section {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="tool-header">🔧 Tool & Equipment Hire</div>', unsafe_allow_html=True)
    
    dm = get_data_manager()
    
    # Tabs for different actions
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📋 View Equipment", "➕ Add Equipment", "📅 Active Rentals", "📊 Rental History", "💰 Import/Export"])
    
    with tab1:
        st.markdown('<div class="section-header">Equipment Inventory</div>', unsafe_allow_html=True)
        
        equipment_df = dm.load_equipment()
        
        if not equipment_df.empty:
            # Search and filter options
            col1, col2, col3 = st.columns(3)
            
            with col1:
                search_term = st.text_input("🔍 Search equipment", placeholder="Name, category, brand...")
            
            with col2:
                category_filter = st.selectbox("Filter by Category", ["All"] + sorted(equipment_df['category'].unique().tolist()))
            
            with col3:
                status_filter = st.selectbox("Filter by Status", ["All", "Available", "Rented", "Maintenance", "Out of Service"])
            
            # Apply filters
            filtered_df = equipment_df.copy()
            
            if search_term:
                mask = (
                    filtered_df['name'].str.contains(search_term, case=False, na=False) |
                    filtered_df['category'].str.contains(search_term, case=False, na=False) |
                    filtered_df['brand'].str.contains(search_term, case=False, na=False) |
                    filtered_df['model'].str.contains(search_term, case=False, na=False)
                )
                filtered_df = filtered_df[mask]
            
            if category_filter != "All":
                filtered_df = filtered_df[filtered_df['category'] == category_filter]
            
            if status_filter != "All":
                filtered_df = filtered_df[filtered_df['status'] == status_filter]
            
            # Display summary
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Equipment", len(filtered_df))
            with col2:
                available_count = len(filtered_df[filtered_df['status'] == 'Available'])
                st.metric("Available", available_count)
            with col3:
                rented_count = len(filtered_df[filtered_df['status'] == 'Rented'])
                st.metric("Currently Rented", rented_count)
            with col4:
                if not filtered_df.empty:
                    total_value = filtered_df['purchase_price'].sum()
                    st.metric("Total Value", f"£{total_value:,.2f}")
                else:
                    st.metric("Total Value", "£0.00")
            
            # Display equipment
            for index, equipment in filtered_df.iterrows():
                status_color = {
                    'Available': '🟢',
                    'Rented': '🔴',
                    'Maintenance': '🟡',
                    'Out of Service': '⚫'
                }.get(equipment['status'], '⚪')
                
                with st.expander(f"{status_color} {equipment['name']} - {equipment['brand']} {equipment['model']}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**Category:** {equipment['category']}")
                        st.write(f"**Brand:** {equipment['brand']}")
                        st.write(f"**Model:** {equipment['model']}")
                        st.write(f"**Serial Number:** {equipment['serial_number']}")
                        st.write(f"**Status:** {equipment['status']}")
                    
                    with col2:
                        st.write(f"**Daily Rate:** £{equipment['daily_rate']:.2f}")
                        st.write(f"**Weekly Rate:** £{equipment['weekly_rate']:.2f}")
                        st.write(f"**Purchase Price:** £{equipment['purchase_price']:.2f}")
                        st.write(f"**Purchase Date:** {equipment['purchase_date']}")
                        st.write(f"**Last Service:** {equipment.get('last_service_date', 'N/A')}")
                    
                    if equipment.get('notes'):
                        st.write(f"**Notes:** {equipment['notes']}")
                    
                    # Action buttons
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        if equipment['status'] == 'Available' and st.button(f"Rent Out", key=f"rent_{equipment['equipment_id']}"):
                            st.session_state[f'rent_equipment_{equipment["equipment_id"]}'] = True
                            st.rerun()
                    
                    with col2:
                        if st.button(f"Edit", key=f"edit_{equipment['equipment_id']}"):
                            st.session_state[f'edit_equipment_{equipment["equipment_id"]}'] = True
                            st.rerun()
                    
                    with col3:
                        if st.button(f"Service Log", key=f"service_{equipment['equipment_id']}"):
                            st.session_state[f'service_equipment_{equipment["equipment_id"]}'] = True
                            st.rerun()
                    
                    with col4:
                        if st.button(f"Delete", key=f"delete_{equipment['equipment_id']}", type="secondary"):
                            if st.session_state.get(f'confirm_delete_{equipment["equipment_id"]}', False):
                                dm.delete_equipment(equipment['equipment_id'])
                                st.success("Equipment deleted successfully!")
                                st.rerun()
                            else:
                                st.session_state[f'confirm_delete_{equipment["equipment_id"]}'] = True
                                st.warning("Click delete again to confirm")
                    
                    # Rent equipment form
                    if st.session_state.get(f'rent_equipment_{equipment["equipment_id"]}', False):
                        st.markdown("---")
                        st.subheader("Rent Equipment")
                        
                        with st.form(f"rent_form_{equipment['equipment_id']}"):
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                customer_name = st.text_input("Customer Name *")
                                customer_phone = st.text_input("Customer Phone")
                                customer_email = st.text_input("Customer Email")
                                start_date = st.date_input("Rental Start Date *", value=date.today())
                            
                            with col2:
                                expected_return = st.date_input("Expected Return Date *", value=date.today() + timedelta(days=1))
                                rental_type = st.selectbox("Rental Type", ["Daily", "Weekly", "Custom"])
                                if rental_type == "Custom":
                                    custom_rate = st.number_input("Custom Rate (£)", min_value=0.0, format="%.2f")
                                deposit = st.number_input("Security Deposit (£)", min_value=0.0, format="%.2f")
                            
                            notes = st.text_area("Rental Notes")
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                if st.form_submit_button("Create Rental"):
                                    if not customer_name or not start_date or not expected_return:
                                        st.error("Please fill in all required fields")
                                    else:
                                        # Calculate rental cost
                                        days = (expected_return - start_date).days + 1
                                        if rental_type == "Daily":
                                            rate = equipment['daily_rate']
                                        elif rental_type == "Weekly":
                                            weeks = max(1, days // 7)
                                            rate = equipment['weekly_rate'] * weeks
                                        else:
                                            rate = custom_rate
                                        
                                        rental_data = {
                                            'equipment_id': equipment['equipment_id'],
                                            'customer_name': customer_name,
                                            'customer_phone': customer_phone,
                                            'customer_email': customer_email,
                                            'start_date': start_date.strftime('%Y-%m-%d'),
                                            'expected_return_date': expected_return.strftime('%Y-%m-%d'),
                                            'rental_rate': rate,
                                            'deposit': deposit,
                                            'status': 'Active',
                                            'notes': notes
                                        }
                                        
                                        dm.add_rental(rental_data)
                                        dm.update_equipment_status(equipment['equipment_id'], 'Rented')
                                        st.success("Rental created successfully!")
                                        del st.session_state[f'rent_equipment_{equipment["equipment_id"]}']
                                        st.rerun()
                            
                            with col2:
                                if st.form_submit_button("Cancel"):
                                    del st.session_state[f'rent_equipment_{equipment["equipment_id"]}']
                                    st.rerun()
        else:
            st.info("No equipment in inventory. Add your first piece of equipment using the 'Add Equipment' tab.")
    
    with tab2:
        st.subheader("Add New Equipment")
        
        with st.form("add_equipment_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("Equipment Name *", placeholder="e.g., Excavator, Generator, Drill")
                # Category with custom option
                categories = ["Construction", "Power Tools", "Generators", "Compressors", 
                            "Lifting Equipment", "Vehicles", "Welding", "Safety", "Other"]
                category_option = st.selectbox("Category *", categories + ["Add Custom..."])
                
                if category_option == "Add Custom...":
                    category = st.text_input("Custom Category *")
                else:
                    category = category_option
                brand = st.text_input("Brand *", placeholder="e.g., Caterpillar, DeWalt")
                model = st.text_input("Model *", placeholder="Model number/name")
                serial_number = st.text_input("Serial Number", placeholder="Unique identifier")
            
            with col2:
                daily_rate = st.number_input("Daily Rate (£) *", min_value=0.0, format="%.2f")
                weekly_rate = st.number_input("Weekly Rate (£) *", min_value=0.0, format="%.2f")
                purchase_price = st.number_input("Purchase Price (£) *", min_value=0.0, format="%.2f")
                purchase_date = st.date_input("Purchase Date *", value=date.today())
                status = st.selectbox("Status *", ["Available", "Maintenance", "Out of Service"])
            
            notes = st.text_area("Notes", placeholder="Additional information about the equipment...")
            
            if st.form_submit_button("Add Equipment", type="primary"):
                if not all([name, category, brand, model, daily_rate]):
                    st.error("Please fill in all required fields marked with *")
                else:
                    new_equipment = {
                        'name': name,
                        'category': category,
                        'brand': brand,
                        'model': model,
                        'serial_number': serial_number,
                        'daily_rate': daily_rate,
                        'weekly_rate': weekly_rate,
                        'purchase_price': purchase_price,
                        'purchase_date': purchase_date.strftime('%Y-%m-%d'),
                        'status': status,
                        'notes': notes
                    }
                    dm.add_equipment(new_equipment)
                    st.success(f"Equipment {name} added successfully!")
                    st.rerun()
    
    with tab3:
        st.subheader("Active Rentals")
        
        rentals_df = dm.load_rentals()
        equipment_df = dm.load_equipment()
        
        if not rentals_df.empty:
            active_rentals = rentals_df[rentals_df['status'] == 'Active'].copy()
            
            if not active_rentals.empty:
                # Merge with equipment data
                active_rentals = active_rentals.merge(
                    equipment_df[['equipment_id', 'name', 'category', 'brand', 'model']], 
                    on='equipment_id', 
                    how='left'
                )
                
                # Calculate days overdue
                active_rentals['expected_return_date'] = pd.to_datetime(active_rentals['expected_return_date'])
                active_rentals['days_overdue'] = (pd.Timestamp.now() - active_rentals['expected_return_date']).dt.days
                
                # Sort by overdue first, then by return date
                active_rentals = active_rentals.sort_values(['days_overdue'], ascending=False)
                
                for index, rental in active_rentals.iterrows():
                    equipment_name = f"{rental['name']} - {rental['brand']} {rental['model']}"
                    
                    # Color code based on status
                    if rental['days_overdue'] > 0:
                        status_indicator = f"🔴 OVERDUE ({rental['days_overdue']} days)"
                    elif rental['days_overdue'] == 0:
                        status_indicator = "🟡 DUE TODAY"
                    else:
                        status_indicator = f"🟢 {abs(rental['days_overdue'])} days remaining"
                    
                    with st.expander(f"{status_indicator} - {equipment_name} - {rental['customer_name']}"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.write(f"**Equipment:** {equipment_name}")
                            st.write(f"**Customer:** {rental['customer_name']}")
                            st.write(f"**Phone:** {rental.get('customer_phone', 'N/A')}")
                            st.write(f"**Email:** {rental.get('customer_email', 'N/A')}")
                        
                        with col2:
                            st.write(f"**Start Date:** {rental['start_date']}")
                            st.write(f"**Expected Return:** {rental['expected_return_date'].strftime('%Y-%m-%d')}")
                            st.write(f"**Rental Rate:** £{rental['rental_rate']:.2f}")
                            st.write(f"**Deposit:** £{rental.get('deposit', 0):.2f}")
                        
                        if rental.get('notes'):
                            st.write(f"**Notes:** {rental['notes']}")
                        
                        # Action buttons
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            if st.button(f"Return Equipment", key=f"return_{rental['rental_id']}"):
                                st.session_state[f'return_rental_{rental["rental_id"]}'] = True
                                st.rerun()
                        
                        with col2:
                            if st.button(f"Extend Rental", key=f"extend_{rental['rental_id']}"):
                                st.session_state[f'extend_rental_{rental["rental_id"]}'] = True
                                st.rerun()
                        
                        with col3:
                            if st.button(f"Contact Customer", key=f"contact_{rental['rental_id']}"):
                                if rental.get('customer_phone'):
                                    st.info(f"Call: {rental['customer_phone']}")
                                if rental.get('customer_email'):
                                    st.info(f"Email: {rental['customer_email']}")
                        
                        # Return equipment form
                        if st.session_state.get(f'return_rental_{rental["rental_id"]}', False):
                            st.markdown("---")
                            st.subheader("Return Equipment")
                            
                            with st.form(f"return_form_{rental['rental_id']}"):
                                return_date = st.date_input("Return Date", value=date.today())
                                return_condition = st.selectbox("Equipment Condition", 
                                                              ["Excellent", "Good", "Fair", "Damaged"])
                                damage_notes = st.text_area("Damage/Notes")
                                additional_charges = st.number_input("Additional Charges (£)", min_value=0.0, format="%.2f")
                                
                                col1, col2 = st.columns(2)
                                with col1:
                                    if st.form_submit_button("Process Return"):
                                        # Calculate final cost
                                        actual_days = (return_date - pd.to_datetime(rental['start_date']).date()).days + 1
                                        expected_days = (pd.to_datetime(rental['expected_return_date']).date() - pd.to_datetime(rental['start_date']).date()).days + 1
                                        
                                        # Update rental record
                                        dm.return_rental(rental['rental_id'], {
                                            'actual_return_date': return_date.strftime('%Y-%m-%d'),
                                            'return_condition': return_condition,
                                            'damage_notes': damage_notes,
                                            'additional_charges': additional_charges,
                                            'status': 'Returned'
                                        })
                                        
                                        # Update equipment status
                                        new_status = 'Available' if return_condition in ['Excellent', 'Good'] else 'Maintenance'
                                        dm.update_equipment_status(rental['equipment_id'], new_status)
                                        
                                        st.success("Equipment returned successfully!")
                                        del st.session_state[f'return_rental_{rental["rental_id"]}']
                                        st.rerun()
                                
                                with col2:
                                    if st.form_submit_button("Cancel"):
                                        del st.session_state[f'return_rental_{rental["rental_id"]}']
                                        st.rerun()
            else:
                st.info("No active rentals at the moment.")
        else:
            st.info("No rental records found.")
    
    with tab4:
        st.subheader("Rental History")
        
        rentals_df = dm.load_rentals()
        equipment_df = dm.load_equipment()
        
        if not rentals_df.empty:
            # Filter options
            col1, col2, col3 = st.columns(3)
            
            with col1:
                customer_filter = st.selectbox("Filter by Customer", ["All"] + sorted(rentals_df['customer_name'].unique().tolist()))
            
            with col2:
                status_filter = st.selectbox("Filter by Status", ["All", "Active", "Returned", "Overdue"])
            
            with col3:
                date_range = st.selectbox("Date Range", ["All Time", "Last 30 Days", "Last 90 Days", "This Year"])
            
            # Apply filters
            filtered_df = rentals_df.copy()
            
            if customer_filter != "All":
                filtered_df = filtered_df[filtered_df['customer_name'] == customer_filter]
            
            if status_filter != "All":
                filtered_df = filtered_df[filtered_df['status'] == status_filter]
            
            # Merge with equipment data
            filtered_df = filtered_df.merge(
                equipment_df[['equipment_id', 'name', 'category', 'brand', 'model']], 
                on='equipment_id', 
                how='left'
            )
            
            # Display summary
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Rentals", len(filtered_df))
            with col2:
                if not filtered_df.empty:
                    total_revenue = filtered_df['rental_rate'].sum()
                    st.metric("Total Revenue", f"£{total_revenue:.2f}")
                else:
                    st.metric("Total Revenue", "£0.00")
            with col3:
                if not filtered_df.empty:
                    avg_rental = filtered_df['rental_rate'].mean()
                    st.metric("Average Rental", f"£{avg_rental:.2f}")
                else:
                    st.metric("Average Rental", "£0.00")
            
            # Display rentals table
            if not filtered_df.empty:
                st.dataframe(
                    filtered_df[['start_date', 'customer_name', 'name', 'brand', 'model', 'rental_rate', 'status']],
                    use_container_width=True
                )
            else:
                st.info("No rental records found matching your filters.")
        else:
            st.info("No rental history available.")
    
    with tab5:
        st.subheader("Import/Export Data")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Export Data")
            equipment_df = dm.load_equipment()
            rentals_df = dm.load_rentals()
            
            if not equipment_df.empty:
                equipment_csv = equipment_df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Equipment CSV",
                    data=equipment_csv,
                    file_name=f"equipment_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            
            if not rentals_df.empty:
                rentals_csv = rentals_df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Rentals CSV",
                    data=rentals_csv,
                    file_name=f"rentals_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
        
        with col2:
            st.markdown("#### Import Data")
            uploaded_file = st.file_uploader("Choose a CSV file", type="csv", key="equipment_import")
            
            if uploaded_file is not None:
                try:
                    import_df = pd.read_csv(uploaded_file)
                    
                    # Check if it's equipment or rental data
                    equipment_columns = ['name', 'category', 'brand', 'model', 'daily_rate']
                    rental_columns = ['equipment_id', 'customer_name', 'start_date']
                    
                    if all(col in import_df.columns for col in equipment_columns):
                        st.write("Preview of equipment data:")
                        st.dataframe(import_df.head())
                        
                        if st.button("Import Equipment"):
                            success_count = dm.import_equipment(import_df)
                            st.success(f"Successfully imported {success_count} equipment items!")
                            st.rerun()
                    
                    elif all(col in import_df.columns for col in rental_columns):
                        st.write("Preview of rental data:")
                        st.dataframe(import_df.head())
                        
                        if st.button("Import Rentals"):
                            success_count = dm.import_rentals(import_df)
                            st.success(f"Successfully imported {success_count} rental records!")
                            st.rerun()
                    
                    else:
                        st.error("CSV format not recognized. Please check column headers.")
                        
                except Exception as e:
                    st.error(f"Error reading CSV file: {str(e)}")
    
    # Create permanent sidebar
    create_sidebar()

if __name__ == "__main__":
    main()
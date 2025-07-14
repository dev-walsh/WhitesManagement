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
    page_title="Statistics", 
    page_icon="📊", 
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
        if st.button("🏗️ Machine Inventory", use_container_width=True):
            st.switch_page("pages/6_Machine_Inventory.py")
        if st.button("⚙️ Tool Hire", use_container_width=True):
            st.switch_page("pages/4_Tool_Hire.py")
        if st.button("📊 Dashboard", use_container_width=True):
            st.switch_page("pages/3_Dashboard.py")
        if st.button("📈 Statistics", use_container_width=True, disabled=True):
            pass  # Current page
        
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
    # Custom CSS for statistics page
    st.markdown("""
    <style>
    .stats-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f77b4;
        margin-bottom: 1rem;
        text-align: center;
    }
    .stats-subheader {
        font-size: 1.1rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stat-card {
        background: linear-gradient(135deg, #1f77b4 0%, #1f77b4 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 8px;
        text-align: center;
        margin: 0.5rem 0;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    .stat-value {
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .stat-label {
        font-size: 0.9rem;
        opacity: 0.9;
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
    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1rem;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="stats-header">📊 Fleet Statistics</div>', unsafe_allow_html=True)
    st.markdown('<div class="stats-subheader">Comprehensive analytics and insights for your fleet operations</div>', unsafe_allow_html=True)
    
    dm = get_data_manager()
    
    # Load all data
    vehicles_df = dm.load_vehicles()
    maintenance_df = dm.load_maintenance()
    equipment_df = dm.load_equipment()
    rentals_df = dm.load_rentals()
    
    # Check if there's any data
    if vehicles_df.empty and equipment_df.empty and maintenance_df.empty and rentals_df.empty:
        st.warning("No data available for statistics. Please add some data first.")
        return
    
    # Create tabs for different statistics
    tab1, tab2, tab3, tab4 = st.tabs(["🚗 Fleet Statistics", "🔧 Maintenance Analytics", "🏢 Equipment & Rentals", "📈 Financial Overview"])
    
    with tab1:
        st.markdown('<div class="section-header">Fleet Overview</div>', unsafe_allow_html=True)
        
        if not vehicles_df.empty:
            # Key Fleet Metrics
            col1, col2, col3, col4, col5 = st.columns(5)
            
            with col1:
                total_vehicles = len(vehicles_df)
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-value">{total_vehicles}</div>
                    <div class="stat-label">Total Vehicles</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                on_hire = len(vehicles_df[vehicles_df['status'] == 'On Hire'])
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-value">{on_hire}</div>
                    <div class="stat-label">On Hire</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                off_hire = len(vehicles_df[vehicles_df['status'] == 'Off Hire'])
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-value">{off_hire}</div>
                    <div class="stat-label">Off Hire</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                maintenance_status = len(vehicles_df[vehicles_df['status'] == 'Maintenance'])
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-value">{maintenance_status}</div>
                    <div class="stat-label">In Maintenance</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col5:
                utilization = (on_hire / total_vehicles * 100) if total_vehicles > 0 else 0
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-value">{utilization:.1f}%</div>
                    <div class="stat-label">Utilization Rate</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("")
            
            # Fleet composition charts
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.subheader("Fleet Status Distribution")
                status_counts = vehicles_df['status'].value_counts()
                fig_status = px.pie(
                    values=status_counts.values,
                    names=status_counts.index,
                    title="Vehicle Status Distribution",
                    color_discrete_map={
                        'On Hire': '#28a745',
                        'Off Hire': '#17a2b8',
                        'Maintenance': '#ffc107'
                    }
                )
                st.plotly_chart(fig_status, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.subheader("Fleet by Type")
                if 'vehicle_type' in vehicles_df.columns:
                    type_counts = vehicles_df['vehicle_type'].fillna('Unknown').value_counts()
                    fig_type = px.bar(
                        x=type_counts.index,
                        y=type_counts.values,
                        title="Vehicle Types",
                        labels={'x': 'Vehicle Type', 'y': 'Count'},
                        color=type_counts.values,
                        color_continuous_scale='Blues'
                    )
                    st.plotly_chart(fig_type, use_container_width=True)
                else:
                    st.info("Vehicle type data not available")
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Age and mileage analysis
            st.markdown('<div class="section-header">Fleet Age & Mileage Analysis</div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.subheader("Vehicle Age Distribution")
                current_year = datetime.now().year
                vehicles_df['age'] = current_year - vehicles_df['year'].astype(int)
                fig_age = px.histogram(
                    vehicles_df,
                    x='age',
                    nbins=10,
                    title="Vehicle Age Distribution (Years)",
                    labels={'age': 'Age (Years)', 'count': 'Number of Vehicles'},
                    color_discrete_sequence=['#1f77b4']
                )
                st.plotly_chart(fig_age, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.subheader("Mileage Distribution")
                fig_mileage = px.histogram(
                    vehicles_df,
                    x='mileage',
                    nbins=15,
                    title="Vehicle Mileage Distribution",
                    labels={'mileage': 'Mileage', 'count': 'Number of Vehicles'},
                    color_discrete_sequence=['#28a745']
                )
                st.plotly_chart(fig_mileage, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
        
        else:
            st.info("No vehicle data available for statistics")
    
    with tab2:
        st.markdown('<div class="section-header">Maintenance Analytics</div>', unsafe_allow_html=True)
        
        if not maintenance_df.empty:
            # Maintenance key metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                total_maintenance = len(maintenance_df)
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-value">{total_maintenance}</div>
                    <div class="stat-label">Total Records</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                total_cost = maintenance_df['cost'].sum()
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-value">£{total_cost:,.0f}</div>
                    <div class="stat-label">Total Cost</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                avg_cost = maintenance_df['cost'].mean()
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-value">£{avg_cost:,.0f}</div>
                    <div class="stat-label">Average Cost</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                # Recent maintenance (last 30 days)
                maintenance_df['date'] = pd.to_datetime(maintenance_df['date'])
                recent_maintenance = maintenance_df[maintenance_df['date'] >= datetime.now() - timedelta(days=30)]
                recent_count = len(recent_maintenance)
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-value">{recent_count}</div>
                    <div class="stat-label">Last 30 Days</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("")
            
            # Maintenance charts
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.subheader("Maintenance by Type")
                type_counts = maintenance_df['type'].value_counts()
                fig_type = px.bar(
                    x=type_counts.index,
                    y=type_counts.values,
                    title="Maintenance Types",
                    labels={'x': 'Maintenance Type', 'y': 'Count'},
                    color=type_counts.values,
                    color_continuous_scale='Reds'
                )
                st.plotly_chart(fig_type, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.subheader("Monthly Maintenance Costs")
                maintenance_df['month'] = maintenance_df['date'].dt.to_period('M')
                monthly_costs = maintenance_df.groupby('month')['cost'].sum().reset_index()
                monthly_costs['month'] = monthly_costs['month'].astype(str)
                fig_monthly = px.line(
                    monthly_costs,
                    x='month',
                    y='cost',
                    title="Monthly Maintenance Costs",
                    labels={'month': 'Month', 'cost': 'Cost (£)'},
                    markers=True
                )
                st.plotly_chart(fig_monthly, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
        
        else:
            st.info("No maintenance data available for statistics")
    
    with tab3:
        st.markdown('<div class="section-header">Equipment & Rental Analytics</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            if not equipment_df.empty:
                # Equipment metrics
                col1a, col1b, col1c = st.columns(3)
                
                with col1a:
                    total_equipment = len(equipment_df)
                    st.markdown(f"""
                    <div class="stat-card">
                        <div class="stat-value">{total_equipment}</div>
                        <div class="stat-label">Total Equipment</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col1b:
                    available_equipment = len(equipment_df[equipment_df['status'] == 'Available'])
                    st.markdown(f"""
                    <div class="stat-card">
                        <div class="stat-value">{available_equipment}</div>
                        <div class="stat-label">Available</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col1c:
                    rented_equipment = len(equipment_df[equipment_df['status'] == 'Rented'])
                    st.markdown(f"""
                    <div class="stat-card">
                        <div class="stat-value">{rented_equipment}</div>
                        <div class="stat-label">Rented</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Equipment by category
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.subheader("Equipment by Category")
                category_counts = equipment_df['category'].value_counts()
                fig_category = px.pie(
                    values=category_counts.values,
                    names=category_counts.index,
                    title="Equipment Categories"
                )
                st.plotly_chart(fig_category, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            else:
                st.info("No equipment data available")
        
        with col2:
            if not rentals_df.empty:
                # Rental metrics
                col2a, col2b, col2c = st.columns(3)
                
                with col2a:
                    total_rentals = len(rentals_df)
                    st.markdown(f"""
                    <div class="stat-card">
                        <div class="stat-value">{total_rentals}</div>
                        <div class="stat-label">Total Rentals</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2b:
                    active_rentals = len(rentals_df[rentals_df['status'] == 'Active'])
                    st.markdown(f"""
                    <div class="stat-card">
                        <div class="stat-value">{active_rentals}</div>
                        <div class="stat-label">Active Rentals</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2c:
                    total_revenue = rentals_df['rental_rate'].sum()
                    st.markdown(f"""
                    <div class="stat-card">
                        <div class="stat-value">£{total_revenue:,.0f}</div>
                        <div class="stat-label">Total Revenue</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Rental timeline
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.subheader("Rental Timeline")
                rentals_df['start_date'] = pd.to_datetime(rentals_df['start_date'])
                rentals_df['month'] = rentals_df['start_date'].dt.to_period('M')
                monthly_rentals = rentals_df.groupby('month').size().reset_index(name='count')
                monthly_rentals['month'] = monthly_rentals['month'].astype(str)
                fig_timeline = px.bar(
                    monthly_rentals,
                    x='month',
                    y='count',
                    title="Monthly Rental Volume",
                    labels={'month': 'Month', 'count': 'Number of Rentals'}
                )
                st.plotly_chart(fig_timeline, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            else:
                st.info("No rental data available")
    
    with tab4:
        st.markdown('<div class="section-header">Financial Overview</div>', unsafe_allow_html=True)
        
        # Financial summary
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            maintenance_cost = maintenance_df['cost'].sum() if not maintenance_df.empty else 0
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-value">£{maintenance_cost:,.0f}</div>
                <div class="stat-label">Maintenance Costs</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            rental_revenue = rentals_df['rental_rate'].sum() if not rentals_df.empty else 0
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-value">£{rental_revenue:,.0f}</div>
                <div class="stat-label">Rental Revenue</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            equipment_value = equipment_df['purchase_price'].sum() if not equipment_df.empty else 0
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-value">£{equipment_value:,.0f}</div>
                <div class="stat-label">Equipment Value</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            net_position = rental_revenue - maintenance_cost
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-value">£{net_position:,.0f}</div>
                <div class="stat-label">Net Position</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Financial trends
        if not maintenance_df.empty or not rentals_df.empty:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.subheader("Financial Trends")
            
            # Create monthly financial summary
            financial_data = []
            
            if not maintenance_df.empty:
                maintenance_monthly = maintenance_df.groupby(maintenance_df['date'].dt.to_period('M'))['cost'].sum()
                for month, cost in maintenance_monthly.items():
                    financial_data.append({'Month': str(month), 'Type': 'Maintenance Cost', 'Amount': -cost})
            
            if not rentals_df.empty:
                rentals_monthly = rentals_df.groupby(rentals_df['start_date'].dt.to_period('M'))['rental_rate'].sum()
                for month, revenue in rentals_monthly.items():
                    financial_data.append({'Month': str(month), 'Type': 'Rental Revenue', 'Amount': revenue})
            
            if financial_data:
                financial_df = pd.DataFrame(financial_data)
                fig_financial = px.bar(
                    financial_df,
                    x='Month',
                    y='Amount',
                    color='Type',
                    title="Monthly Financial Overview",
                    labels={'Amount': 'Amount (£)', 'Month': 'Month'},
                    color_discrete_map={
                        'Maintenance Cost': '#dc3545',
                        'Rental Revenue': '#28a745'
                    }
                )
                st.plotly_chart(fig_financial, use_container_width=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        else:
            st.info("No financial data available for trends")
    
    # Create permanent sidebar
    create_sidebar()

if __name__ == "__main__":
    main()
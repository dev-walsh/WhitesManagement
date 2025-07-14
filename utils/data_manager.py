import pandas as pd
import os
import uuid
from datetime import datetime

class DataManager:
    def __init__(self):
        self.vehicles_file = "data/vehicles.csv"
        self.maintenance_file = "data/maintenance.csv"
        self.equipment_file = "data/equipment.csv"
        self.rentals_file = "data/rentals.csv"
        self.ensure_data_directory()
        self.ensure_csv_files()
    
    def ensure_data_directory(self):
        """Create data directory if it doesn't exist"""
        if not os.path.exists("data"):
            os.makedirs("data")
    
    def ensure_csv_files(self):
        """Create CSV files with headers if they don't exist"""
        # Vehicle CSV headers
        if not os.path.exists(self.vehicles_file):
            vehicle_columns = [
                'vehicle_id', 'whites_id', 'make', 'model', 'year', 'weight', 'license_plate', 
                'vehicle_type', 'status', 'mileage', 'defects', 'notes'
            ]
            empty_df = pd.DataFrame(columns=vehicle_columns)
            empty_df.to_csv(self.vehicles_file, index=False)
        
        # Maintenance CSV headers
        if not os.path.exists(self.maintenance_file):
            maintenance_columns = [
                'maintenance_id', 'vehicle_id', 'date', 'type', 'description', 
                'cost', 'mileage', 'service_provider', 'next_due_mileage'
            ]
            empty_df = pd.DataFrame(columns=maintenance_columns)
            empty_df.to_csv(self.maintenance_file, index=False)
        
        # Equipment CSV headers
        if not os.path.exists(self.equipment_file):
            equipment_columns = [
                'equipment_id', 'name', 'category', 'brand', 'model', 'serial_number',
                'daily_rate', 'weekly_rate', 'purchase_price', 'purchase_date', 
                'status', 'last_service_date', 'notes'
            ]
            empty_df = pd.DataFrame(columns=equipment_columns)
            empty_df.to_csv(self.equipment_file, index=False)
        
        # Rentals CSV headers
        if not os.path.exists(self.rentals_file):
            rental_columns = [
                'rental_id', 'equipment_id', 'customer_name', 'customer_phone', 'customer_email',
                'start_date', 'expected_return_date', 'actual_return_date', 'rental_rate', 
                'deposit', 'additional_charges', 'status', 'return_condition', 'damage_notes', 'notes'
            ]
            empty_df = pd.DataFrame(columns=rental_columns)
            empty_df.to_csv(self.rentals_file, index=False)
    
    def load_vehicles(self):
        """Load vehicles from CSV"""
        try:
            df = pd.read_csv(self.vehicles_file)
            return df
        except (FileNotFoundError, pd.errors.EmptyDataError):
            return pd.DataFrame(columns=[
                'vehicle_id', 'whites_id', 'make', 'model', 'year', 'weight', 'license_plate', 
                'vehicle_type', 'status', 'mileage', 'defects', 'notes'
            ])
    
    def load_maintenance(self):
        """Load maintenance records from CSV"""
        try:
            df = pd.read_csv(self.maintenance_file)
            return df
        except (FileNotFoundError, pd.errors.EmptyDataError):
            return pd.DataFrame(columns=[
                'maintenance_id', 'vehicle_id', 'date', 'type', 'description', 
                'cost', 'mileage', 'service_provider', 'next_due_mileage'
            ])
    
    def add_vehicle(self, vehicle_data):
        """Add a new vehicle"""
        df = self.load_vehicles()
        
        # Generate unique vehicle ID
        vehicle_data['vehicle_id'] = str(uuid.uuid4())[:8]
        
        # Convert to DataFrame and append
        new_vehicle = pd.DataFrame([vehicle_data])
        df = pd.concat([df, new_vehicle], ignore_index=True)
        
        # Save to CSV
        df.to_csv(self.vehicles_file, index=False)
        return vehicle_data['vehicle_id']
    
    def update_vehicle(self, updated_vehicle):
        """Update an existing vehicle"""
        df = self.load_vehicles()
        
        # Find and update the vehicle
        vehicle_id = updated_vehicle['vehicle_id']
        df.loc[df['vehicle_id'] == vehicle_id, df.columns] = [updated_vehicle[col] for col in df.columns]
        
        # Save to CSV
        df.to_csv(self.vehicles_file, index=False)
    
    def update_vehicle_mileage(self, vehicle_id, new_mileage):
        """Update vehicle mileage"""
        df = self.load_vehicles()
        df.loc[df['vehicle_id'] == vehicle_id, 'mileage'] = new_mileage
        df.to_csv(self.vehicles_file, index=False)
    
    def delete_vehicle(self, vehicle_id):
        """Delete a vehicle"""
        df = self.load_vehicles()
        df = df[df['vehicle_id'] != vehicle_id]
        df.to_csv(self.vehicles_file, index=False)
        
        # Also delete associated maintenance records
        maintenance_df = self.load_maintenance()
        maintenance_df = maintenance_df[maintenance_df['vehicle_id'] != vehicle_id]
        maintenance_df.to_csv(self.maintenance_file, index=False)
    
    def add_maintenance(self, maintenance_data):
        """Add a new maintenance record"""
        df = self.load_maintenance()
        
        # Generate unique maintenance ID
        maintenance_data['maintenance_id'] = str(uuid.uuid4())[:8]
        
        # Convert to DataFrame and append
        new_maintenance = pd.DataFrame([maintenance_data])
        df = pd.concat([df, new_maintenance], ignore_index=True)
        
        # Save to CSV
        df.to_csv(self.maintenance_file, index=False)
        return maintenance_data['maintenance_id']
    
    def update_maintenance(self, updated_maintenance):
        """Update an existing maintenance record"""
        df = self.load_maintenance()
        
        # Find and update the maintenance record
        maintenance_id = updated_maintenance['maintenance_id']
        df.loc[df['maintenance_id'] == maintenance_id, df.columns] = [updated_maintenance[col] for col in df.columns]
        
        # Save to CSV
        df.to_csv(self.maintenance_file, index=False)
    
    def delete_maintenance(self, maintenance_id):
        """Delete a maintenance record"""
        df = self.load_maintenance()
        df = df[df['maintenance_id'] != maintenance_id]
        df.to_csv(self.maintenance_file, index=False)
    
    def import_vehicles(self, import_df):
        """Import vehicles from DataFrame"""
        existing_df = self.load_vehicles()
        
        success_count = 0
        for _, row in import_df.iterrows():
            try:
                # Check if VIN already exists
                if not existing_df.empty and row['vin'] in existing_df['vin'].values:
                    continue
                
                # Generate unique vehicle ID
                vehicle_data = row.to_dict()
                vehicle_data['vehicle_id'] = str(uuid.uuid4())[:8]
                
                # Add to existing DataFrame
                new_vehicle = pd.DataFrame([vehicle_data])
                existing_df = pd.concat([existing_df, new_vehicle], ignore_index=True)
                success_count += 1
                
            except Exception as e:
                print(f"Error importing vehicle: {e}")
                continue
        
        # Save updated DataFrame
        existing_df.to_csv(self.vehicles_file, index=False)
        return success_count
    
    def import_maintenance(self, import_df):
        """Import maintenance records from DataFrame"""
        existing_df = self.load_maintenance()
        
        success_count = 0
        for _, row in import_df.iterrows():
            try:
                # Generate unique maintenance ID
                maintenance_data = row.to_dict()
                maintenance_data['maintenance_id'] = str(uuid.uuid4())[:8]
                
                # Add to existing DataFrame
                new_maintenance = pd.DataFrame([maintenance_data])
                existing_df = pd.concat([existing_df, new_maintenance], ignore_index=True)
                success_count += 1
                
            except Exception as e:
                print(f"Error importing maintenance record: {e}")
                continue
        
        # Save updated DataFrame
        existing_df.to_csv(self.maintenance_file, index=False)
        return success_count
    
    def get_vehicle_maintenance_history(self, vehicle_id):
        """Get maintenance history for a specific vehicle"""
        maintenance_df = self.load_maintenance()
        return maintenance_df[maintenance_df['vehicle_id'] == vehicle_id].sort_values('date', ascending=False)
    
    def get_maintenance_cost_summary(self, start_date=None, end_date=None):
        """Get maintenance cost summary for a date range"""
        maintenance_df = self.load_maintenance()
        
        if start_date and end_date:
            maintenance_df['date'] = pd.to_datetime(maintenance_df['date'])
            maintenance_df = maintenance_df[
                (maintenance_df['date'] >= pd.to_datetime(start_date)) &
                (maintenance_df['date'] <= pd.to_datetime(end_date))
            ]
        
        return {
            'total_cost': maintenance_df['cost'].sum(),
            'average_cost': maintenance_df['cost'].mean(),
            'record_count': len(maintenance_df),
            'cost_by_type': maintenance_df.groupby('type')['cost'].sum().to_dict()
        }
    
    # Equipment management methods
    def load_equipment(self):
        """Load equipment from CSV"""
        try:
            df = pd.read_csv(self.equipment_file)
            return df
        except (FileNotFoundError, pd.errors.EmptyDataError):
            return pd.DataFrame(columns=[
                'equipment_id', 'name', 'category', 'brand', 'model', 'serial_number',
                'daily_rate', 'weekly_rate', 'purchase_price', 'purchase_date', 
                'status', 'last_service_date', 'notes'
            ])
    
    def add_equipment(self, equipment_data):
        """Add a new piece of equipment"""
        df = self.load_equipment()
        
        # Generate unique equipment ID
        equipment_data['equipment_id'] = str(uuid.uuid4())[:8]
        
        # Convert to DataFrame and append
        new_equipment = pd.DataFrame([equipment_data])
        df = pd.concat([df, new_equipment], ignore_index=True)
        
        # Save to CSV
        df.to_csv(self.equipment_file, index=False)
        return equipment_data['equipment_id']
    
    def update_equipment(self, updated_equipment):
        """Update an existing piece of equipment"""
        df = self.load_equipment()
        
        # Find and update the equipment
        equipment_id = updated_equipment['equipment_id']
        df.loc[df['equipment_id'] == equipment_id, df.columns] = [updated_equipment[col] for col in df.columns]
        
        # Save to CSV
        df.to_csv(self.equipment_file, index=False)
    
    def update_equipment_status(self, equipment_id, new_status):
        """Update equipment status"""
        df = self.load_equipment()
        df.loc[df['equipment_id'] == equipment_id, 'status'] = new_status
        df.to_csv(self.equipment_file, index=False)
    
    def delete_equipment(self, equipment_id):
        """Delete equipment"""
        df = self.load_equipment()
        df = df[df['equipment_id'] != equipment_id]
        df.to_csv(self.equipment_file, index=False)
        
        # Also delete associated rental records
        rentals_df = self.load_rentals()
        rentals_df = rentals_df[rentals_df['equipment_id'] != equipment_id]
        rentals_df.to_csv(self.rentals_file, index=False)
    
    def import_equipment(self, import_df):
        """Import equipment from DataFrame"""
        existing_df = self.load_equipment()
        
        success_count = 0
        for _, row in import_df.iterrows():
            try:
                # Generate unique equipment ID
                equipment_data = row.to_dict()
                equipment_data['equipment_id'] = str(uuid.uuid4())[:8]
                
                # Add to existing DataFrame
                new_equipment = pd.DataFrame([equipment_data])
                existing_df = pd.concat([existing_df, new_equipment], ignore_index=True)
                success_count += 1
                
            except Exception as e:
                print(f"Error importing equipment: {e}")
                continue
        
        # Save updated DataFrame
        existing_df.to_csv(self.equipment_file, index=False)
        return success_count
    
    # Rental management methods
    def load_rentals(self):
        """Load rentals from CSV"""
        try:
            df = pd.read_csv(self.rentals_file)
            return df
        except (FileNotFoundError, pd.errors.EmptyDataError):
            return pd.DataFrame(columns=[
                'rental_id', 'equipment_id', 'customer_name', 'customer_phone', 'customer_email',
                'start_date', 'expected_return_date', 'actual_return_date', 'rental_rate', 
                'deposit', 'additional_charges', 'status', 'return_condition', 'damage_notes', 'notes'
            ])
    
    def add_rental(self, rental_data):
        """Add a new rental record"""
        df = self.load_rentals()
        
        # Generate unique rental ID
        rental_data['rental_id'] = str(uuid.uuid4())[:8]
        
        # Convert to DataFrame and append
        new_rental = pd.DataFrame([rental_data])
        df = pd.concat([df, new_rental], ignore_index=True)
        
        # Save to CSV
        df.to_csv(self.rentals_file, index=False)
        return rental_data['rental_id']
    
    def update_rental(self, updated_rental):
        """Update an existing rental record"""
        df = self.load_rentals()
        
        # Find and update the rental record
        rental_id = updated_rental['rental_id']
        df.loc[df['rental_id'] == rental_id, df.columns] = [updated_rental[col] for col in df.columns]
        
        # Save to CSV
        df.to_csv(self.rentals_file, index=False)
    
    def return_rental(self, rental_id, return_data):
        """Process equipment return"""
        df = self.load_rentals()
        
        # Update rental with return information
        for key, value in return_data.items():
            df.loc[df['rental_id'] == rental_id, key] = value
        
        # Save to CSV
        df.to_csv(self.rentals_file, index=False)
    
    def import_rentals(self, import_df):
        """Import rentals from DataFrame"""
        existing_df = self.load_rentals()
        
        success_count = 0
        for _, row in import_df.iterrows():
            try:
                # Generate unique rental ID
                rental_data = row.to_dict()
                rental_data['rental_id'] = str(uuid.uuid4())[:8]
                
                # Add to existing DataFrame
                new_rental = pd.DataFrame([rental_data])
                existing_df = pd.concat([existing_df, new_rental], ignore_index=True)
                success_count += 1
                
            except Exception as e:
                print(f"Error importing rental: {e}")
                continue
        
        # Save updated DataFrame
        existing_df.to_csv(self.rentals_file, index=False)
        return success_count
    
    def get_equipment_rental_history(self, equipment_id):
        """Get rental history for a specific piece of equipment"""
        rentals_df = self.load_rentals()
        return rentals_df[rentals_df['equipment_id'] == equipment_id].sort_values('start_date', ascending=False)
    
    def get_rental_revenue_summary(self, start_date=None, end_date=None):
        """Get rental revenue summary for a date range"""
        rentals_df = self.load_rentals()
        
        if start_date and end_date:
            rentals_df['start_date'] = pd.to_datetime(rentals_df['start_date'])
            rentals_df = rentals_df[
                (rentals_df['start_date'] >= pd.to_datetime(start_date)) &
                (rentals_df['start_date'] <= pd.to_datetime(end_date))
            ]
        
        return {
            'total_revenue': rentals_df['rental_rate'].sum(),
            'average_rental': rentals_df['rental_rate'].mean(),
            'rental_count': len(rentals_df),
            'revenue_by_equipment': rentals_df.groupby('equipment_id')['rental_rate'].sum().to_dict()
        }

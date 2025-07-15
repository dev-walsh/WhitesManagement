#!/usr/bin/env python3
"""
Test script to add realistic data to the Whites Management system
"""

import pandas as pd
import uuid
import os
from datetime import datetime, timedelta
import random

# Create data directory if it doesn't exist
os.makedirs('data', exist_ok=True)

# Test Vehicles (Road Vehicles)
test_vehicles = [
    {
        'vehicle_id': str(uuid.uuid4())[:8],
        'whites_id': 'WH001',
        'vin_chassis': 'JM1GJ1W57H1234567',
        'make': 'Ford',
        'model': 'Transit',
        'year': 2019,
        'weight': 3.5,
        'license_plate': 'BT19 ABC',
        'vehicle_type': 'Van',
        'status': 'On Hire',
        'mileage': 45000,
        'defects': 'Minor paint scratches on rear door',
        'notes': 'Regular service due in 2000 miles'
    },
    {
        'vehicle_id': str(uuid.uuid4())[:8],
        'whites_id': 'WH002',
        'vin_chassis': 'WVWZZZ9NZHE123456',
        'make': 'Volkswagen',
        'model': 'Crafter',
        'year': 2020,
        'weight': 4.2,
        'license_plate': 'BT20 DEF',
        'vehicle_type': 'Van',
        'status': 'Off Hire',
        'mileage': 32000,
        'defects': '',
        'notes': 'Recently serviced, excellent condition'
    },
    {
        'vehicle_id': str(uuid.uuid4())[:8],
        'whites_id': 'WH003',
        'vin_chassis': 'SALGS2VF5HA123456',
        'make': 'Land Rover',
        'model': 'Defender',
        'year': 2018,
        'weight': 2.8,
        'license_plate': 'BT18 GHI',
        'vehicle_type': 'Truck',
        'status': 'Maintenance',
        'mileage': 78000,
        'defects': 'Brake pads need replacement',
        'notes': 'In workshop for brake service'
    }
]

# Test Machines (Plant Vehicles)
test_machines = [
    {
        'machine_id': str(uuid.uuid4())[:8],
        'whites_id': 'WM001',
        'vin_chassis': 'CAT320DL2345678',
        'make': 'Caterpillar',
        'model': '320D',
        'year': 2017,
        'weight': 20.5,
        'machine_type': 'Excavator',
        'daily_rate': 450.00,
        'weekly_rate': 2700.00,
        'status': 'Active',
        'hours': 3450,
        'defects': '',
        'notes': 'Excellent condition, recently serviced'
    },
    {
        'machine_id': str(uuid.uuid4())[:8],
        'whites_id': 'WM002',
        'vin_chassis': 'JCB531-70345678',
        'make': 'JCB',
        'model': '531-70',
        'year': 2019,
        'weight': 4.2,
        'machine_type': 'Telehandler',
        'daily_rate': 280.00,
        'weekly_rate': 1680.00,
        'status': 'Active',
        'hours': 2150,
        'defects': 'Minor hydraulic leak',
        'notes': 'Popular machine, high demand'
    },
    {
        'machine_id': str(uuid.uuid4())[:8],
        'whites_id': 'WM003',
        'vin_chassis': 'VOL210G2345678',
        'make': 'Volvo',
        'model': 'L110G',
        'year': 2020,
        'weight': 15.8,
        'machine_type': 'Loader',
        'daily_rate': 380.00,
        'weekly_rate': 2280.00,
        'status': 'Under Maintenance',
        'hours': 1890,
        'defects': 'Engine service required',
        'notes': 'Scheduled for major service'
    }
]

# Test Equipment
test_equipment = [
    {
        'equipment_id': str(uuid.uuid4())[:8],
        'name': 'Portable Generator 10kVA',
        'category': 'Power Generation',
        'brand': 'Honda',
        'model': 'EU10i',
        'serial_number': 'HND-10KVA-001',
        'daily_rate': 45.00,
        'weekly_rate': 270.00,
        'purchase_price': 2500.00,
        'purchase_date': '2023-01-15',
        'status': 'Available',
        'last_service_date': '2024-06-01',
        'notes': 'Quiet operation, fuel efficient'
    },
    {
        'equipment_id': str(uuid.uuid4())[:8],
        'name': 'Concrete Mixer 250L',
        'category': 'Construction',
        'brand': 'Belle',
        'model': 'Minimix 150',
        'serial_number': 'BEL-250L-002',
        'daily_rate': 35.00,
        'weekly_rate': 210.00,
        'purchase_price': 1200.00,
        'purchase_date': '2022-08-20',
        'status': 'Available',
        'last_service_date': '2024-05-15',
        'notes': 'Petrol engine, easy start'
    }
]

# Test Maintenance Records
test_maintenance = [
    {
        'maintenance_id': str(uuid.uuid4())[:8],
        'vehicle_id': test_vehicles[0]['vehicle_id'],
        'date': '2024-06-15',
        'type': 'Service',
        'description': 'Annual service and MOT',
        'cost': 450.00,
        'mileage': 43000,
        'service_provider': 'Ford Main Dealer',
        'next_due_mileage': 48000
    },
    {
        'maintenance_id': str(uuid.uuid4())[:8],
        'vehicle_id': test_vehicles[1]['vehicle_id'],
        'date': '2024-07-01',
        'description': 'Oil change and filter replacement',
        'type': 'Routine',
        'cost': 120.00,
        'mileage': 31500,
        'service_provider': 'Local Garage',
        'next_due_mileage': 36500
    }
]

# Test Rentals
test_rentals = [
    {
        'rental_id': str(uuid.uuid4())[:8],
        'equipment_id': test_equipment[0]['equipment_id'],
        'customer_name': 'ABC Construction Ltd',
        'customer_phone': '01234 567890',
        'customer_email': 'orders@abcconstruction.co.uk',
        'start_date': '2024-07-10',
        'expected_return_date': '2024-07-17',
        'actual_return_date': '',
        'rental_rate': 270.00,
        'deposit': 500.00,
        'additional_charges': 0.00,
        'status': 'Active',
        'return_condition': '',
        'damage_notes': '',
        'notes': 'Weekly hire for site power'
    }
]

# Create CSV files
def create_csv_files():
    # Vehicles
    vehicles_df = pd.DataFrame(test_vehicles)
    vehicles_df.to_csv('data/vehicles.csv', index=False)
    
    # Machines
    machines_df = pd.DataFrame(test_machines)
    machines_df.to_csv('data/machines.csv', index=False)
    
    # Equipment
    equipment_df = pd.DataFrame(test_equipment)
    equipment_df.to_csv('data/equipment.csv', index=False)
    
    # Maintenance
    maintenance_df = pd.DataFrame(test_maintenance)
    maintenance_df.to_csv('data/maintenance.csv', index=False)
    
    # Rentals
    rentals_df = pd.DataFrame(test_rentals)
    rentals_df.to_csv('data/rentals.csv', index=False)
    
    print("Test data created successfully!")
    print(f"Added {len(test_vehicles)} vehicles")
    print(f"Added {len(test_machines)} machines")
    print(f"Added {len(test_equipment)} equipment items")
    print(f"Added {len(test_maintenance)} maintenance records")
    print(f"Added {len(test_rentals)} rental records")

if __name__ == "__main__":
    create_csv_files()
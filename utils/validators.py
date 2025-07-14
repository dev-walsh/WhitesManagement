import re
from datetime import datetime

def validate_vin(vin):
    """
    Validate Vehicle Identification Number (VIN)
    VIN should be 17 characters long and contain only alphanumeric characters
    excluding I, O, and Q
    """
    if not vin:
        return False
    
    # Remove any spaces and convert to uppercase
    vin = vin.replace(" ", "").upper()
    
    # Check length
    if len(vin) != 17:
        return False
    
    # Check for valid characters (no I, O, Q)
    valid_chars = re.match(r'^[ABCDEFGHJKLMNPRSTUVWXYZ0-9]{17}$', vin)
    
    return bool(valid_chars)

def validate_year(year):
    """
    Validate vehicle year
    Should be between 1900 and current year + 1
    """
    current_year = datetime.now().year
    
    try:
        year = int(year)
        return 1900 <= year <= (current_year + 1)
    except (ValueError, TypeError):
        return False

def validate_license_plate(license_plate):
    """
    Basic license plate validation
    Should be alphanumeric and between 2-8 characters
    """
    if not license_plate:
        return False
    
    # Remove spaces and convert to uppercase
    license_plate = license_plate.replace(" ", "").upper()
    
    # Check length and characters
    if 2 <= len(license_plate) <= 8:
        return re.match(r'^[A-Z0-9-]+$', license_plate) is not None
    
    return False

def validate_mileage(mileage):
    """
    Validate vehicle mileage
    Should be a non-negative number
    """
    try:
        mileage = float(mileage)
        return mileage >= 0
    except (ValueError, TypeError):
        return False

def validate_cost(cost):
    """
    Validate maintenance cost
    Should be a non-negative number
    """
    try:
        cost = float(cost)
        return cost >= 0
    except (ValueError, TypeError):
        return False

def validate_date(date_string):
    """
    Validate date string in YYYY-MM-DD format
    """
    try:
        datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def validate_required_fields(data, required_fields):
    """
    Validate that all required fields are present and not empty
    """
    for field in required_fields:
        if field not in data or not data[field] or str(data[field]).strip() == '':
            return False, f"Field '{field}' is required"
    
    return True, "All required fields are present"

def validate_vehicle_data(vehicle_data):
    """
    Comprehensive validation for vehicle data
    """
    errors = []
    
    # Required fields check
    required_fields = ['make', 'model', 'year', 'vin', 'license_plate', 'status', 'mileage']
    is_valid, message = validate_required_fields(vehicle_data, required_fields)
    if not is_valid:
        errors.append(message)
    
    # Specific field validations
    if 'vin' in vehicle_data and not validate_vin(vehicle_data['vin']):
        errors.append("Invalid VIN format")
    
    if 'year' in vehicle_data and not validate_year(vehicle_data['year']):
        errors.append("Invalid year")
    
    if 'license_plate' in vehicle_data and not validate_license_plate(vehicle_data['license_plate']):
        errors.append("Invalid license plate format")
    
    if 'mileage' in vehicle_data and not validate_mileage(vehicle_data['mileage']):
        errors.append("Invalid mileage")
    
    if 'status' in vehicle_data and vehicle_data['status'] not in ['Active', 'Inactive', 'Maintenance']:
        errors.append("Status must be Active, Inactive, or Maintenance")
    
    return len(errors) == 0, errors

def validate_maintenance_data(maintenance_data):
    """
    Comprehensive validation for maintenance data
    """
    errors = []
    
    # Required fields check
    required_fields = ['vehicle_id', 'date', 'type', 'description', 'cost', 'mileage']
    is_valid, message = validate_required_fields(maintenance_data, required_fields)
    if not is_valid:
        errors.append(message)
    
    # Specific field validations
    if 'date' in maintenance_data and not validate_date(maintenance_data['date']):
        errors.append("Invalid date format (use YYYY-MM-DD)")
    
    if 'cost' in maintenance_data and not validate_cost(maintenance_data['cost']):
        errors.append("Invalid cost")
    
    if 'mileage' in maintenance_data and not validate_mileage(maintenance_data['mileage']):
        errors.append("Invalid mileage")
    
    # Validate maintenance type
    valid_types = [
        "Oil Change", "Tire Rotation", "Brake Service", "Transmission Service",
        "Engine Repair", "General Maintenance", "Inspection", "Other"
    ]
    if 'type' in maintenance_data and maintenance_data['type'] not in valid_types:
        errors.append(f"Invalid maintenance type. Must be one of: {', '.join(valid_types)}")
    
    return len(errors) == 0, errors

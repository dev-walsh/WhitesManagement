import re
from datetime import datetime

def validate_weight(weight):
    """
    Validate vehicle weight in tonnes
    Should be a positive number
    """
    try:
        weight = float(weight)
        if weight > 0:
            return True, ""
        else:
            return False, "Weight must be greater than 0 tonnes"
    except (ValueError, TypeError):
        return False, "Weight must be a valid number"

def validate_year(year):
    """
    Validate vehicle year
    Should be between 1900 and current year + 1
    """
    current_year = datetime.now().year
    
    try:
        year = int(year)
        if 1900 <= year <= (current_year + 1):
            return True, ""
        else:
            return False, f"Year must be between 1900 and {current_year + 1}"
    except (ValueError, TypeError):
        return False, "Year must be a valid number"

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
        if mileage >= 0:
            return True, ""
        else:
            return False, "Mileage cannot be negative"
    except (ValueError, TypeError):
        return False, "Mileage must be a valid number"

def validate_cost(cost):
    """
    Validate maintenance cost
    Should be a non-negative number
    """
    try:
        cost = float(cost)
        if cost >= 0:
            return True, ""
        else:
            return False, "Cost cannot be negative"
    except (ValueError, TypeError):
        return False, "Cost must be a valid number"

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
    required_fields = ['make', 'model', 'year', 'weight', 'license_plate', 'status', 'mileage', 'vehicle_type']
    is_valid, message = validate_required_fields(vehicle_data, required_fields)
    if not is_valid:
        errors.append(message)
    
    # Specific field validations
    if 'weight' in vehicle_data and not validate_weight(vehicle_data['weight']):
        errors.append("Invalid weight - must be a positive number")
    
    if 'year' in vehicle_data and not validate_year(vehicle_data['year']):
        errors.append("Invalid year")
    
    if 'license_plate' in vehicle_data and not validate_license_plate(vehicle_data['license_plate']):
        errors.append("Invalid license plate format")
    
    if 'mileage' in vehicle_data and not validate_mileage(vehicle_data['mileage']):
        errors.append("Invalid mileage")
    
    if 'status' in vehicle_data and vehicle_data['status'] not in ['On Hire', 'Off Hire', 'Maintenance']:
        errors.append("Status must be On Hire, Off Hire, or Maintenance")
    
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

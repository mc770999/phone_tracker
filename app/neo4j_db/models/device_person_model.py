from dataclasses import dataclass
from typing import Dict

from app.neo4j_db.models.location_model import Location


"""
{
'id': '70c23243-0e24-4bb6-aa7b-126467c51b00', 
'name': 'Linda', 
'brand': 'Ramirez, Alvarez and Riley', 
'model': 'Cost Player', 'os': 'ThemOS 4.4', 
'latitude': 43.087172, 
'longitude': -174.92976, 
'altitude_meters': 520, 
'accuracy_meters': 10
}
"""
{'id': 'b5f0f1b7-733e-4eaf-9d0d-beb9acea7264',
 'name': 'Sonya', 'brand': 'Jackson-Molina',
 'model': 'Chance Better', 'os': 'SeriesOS 1.4',
 'device_id': 'b5f0f1b7-733e-4eaf-9d0d-beb9acea7264',
 'latitude': -38.950688,
 'longitude': -97.394564,
 'altitude_meters': 4071,
 'accuracy_meters': 31}

"""
{'devices': 
[{
    'id': '1f420e72-7c53-46f5-916c-209ec72295fd', 
    'name': 'Kelly', 
    'brand': 'Gonzalez Inc', 
    'model': 'Middle Less', 
    'os': 'SoundOS 13.5', 
    'location': {
        'latitude': -47.373776, 
        'longitude': 68.896817, 
        'altitude_meters': 4707, 
        'accuracy_meters': 4
        }}, 
    {
    'id': '7ed1a872-1976-46c7-a700-97e65b854fd0', 
    'name': 'Kevin', 
    'brand': 'Owen-Ramirez', 
    'model': 'Baby Democratic', 
    'os': 'StartOS 9.2', 
        'location': {
        'latitude': -77.1480935, 
        'longitude': -167.669284, 
        'altitude_meters': 0, 
        'accuracy_meters': 47}
        }
    ], 
        'interaction': {
        'from_device': '1f420e72-7c53-46f5-916c-209ec72295fd', 
        'to_device': 
        '7ed1a872-1976-46c7-a700-97e65b854fd0', 
        'method': 'NFC', 
        'bluetooth_version': '5.1', 
        'signal_strength_dbm': -33, 
        'distance_meters': 19.95, 
        'duration_seconds': 187, 
        'timestamp': '2005-09-01T04:38:02'
}}
"""

@dataclass
class DevicePerson:
    device_id: str
    name: str
    brand: str
    model: str
    os: str
    latitude: float
    longitude: float
    altitude_meters: int
    accuracy_meters: int
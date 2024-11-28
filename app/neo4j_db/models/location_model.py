from dataclasses import dataclass
from typing import Dict

@dataclass
class Location:
    latitude: float
    longitude: float
    altitude_meters: int
    accuracy_meters: int


from dataclasses import dataclass
from typing import Dict

from app.neo4j_db.models.location_model import Location




@dataclass
class Device:
    id: str
    brand: str
    model: str
    os: str
    location: Location = None

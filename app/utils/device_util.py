from app.neo4j_db.models.device_model import Device
from app.neo4j_db.models.device_person_model import DevicePerson
from app.neo4j_db.models.location_model import Location


def torn_to_device_person(device_json):
    location_json  = device_json.get('location')
    del device_json['location']
    device_json["device_id"] = device_json["id"]
    del device_json["id"]
    device_location_json = {**device_json, **location_json}
    print(device_location_json)
    device_person = DevicePerson(**device_location_json)
    return device_person

def devices_same(devices):
    return all(d.device_id == devices[0].device_id for d in devices)
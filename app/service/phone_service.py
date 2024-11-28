from app.neo4j_db.models.device_model import Device
from app.neo4j_db.repository.device_person_repository import check_if_device_person_exist, create_device_person, \
    check_timestamp_in_relations, create_relation_device_person, get_device_person_relations
from app.utils.device_util import torn_to_device_person, devices_same


def add_device_phone(message):
    devices_person_list = message.get('devices', [])
    devices_person = list(map(torn_to_device_person, devices_person_list))

    if devices_same(devices_person):
        return


    for dp in devices_person:
        create_device_person(dp)



    from_person = message.get('interaction', {}).get('from_device', "0")
    to_person = message.get('interaction', {}).get('to_device', "0")
    from_person_timestamp = message.get('interaction', {}).get('timestamp', "0")
    if get_device_person_relations(from_person, from_person_timestamp) or get_device_person_relations(to_person,from_person_timestamp):
        return

    prop = message['interaction']

    del prop["from_device"]
    del prop["to_device"]

    create_relation_device_person(from_person,to_person,prop)










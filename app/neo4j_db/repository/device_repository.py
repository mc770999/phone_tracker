from app.neo4j_db.repository.node_repository import create_node, delete_node, update_node, get_all_node, \
    create_relation_node

create_device = create_node

update_device = update_node("Device")

delete_device = delete_node("Device")

get_all_device = get_all_node("Device")

get_device_by_id = get_all_node("Device")

create_relation_between_device = create_relation_node("Device", "Device", "CONNECTED")  #(type_n1, type_n2, relation, n1_id, n2_id, n3_id, prop=""):
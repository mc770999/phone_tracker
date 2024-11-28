from app.neo4j_db.repository.node_repository import create_node, delete_node, update_node, get_all_node

create_location = create_node

update_location = update_node("Location")

delete_location = delete_node("Location")

get_all_location = get_all_node("Location")

get_location_by_id = get_all_node("Location")
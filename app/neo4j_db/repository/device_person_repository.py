from dataclasses import asdict

from app.neo4j_db.database import driver



def create_device_person(device_person):
    properties = asdict(device_person)
    query = """
    merge(n:DevicePerson{
    device_id: $device_id,
    name: $name,
    brand: $brand,
    model: $model,
    os: $os,
    latitude: $latitude,
    longitude: $longitude,
    altitude_meters: $altitude_meters,
    accuracy_meters: $accuracy_meters
    })
    RETURN n
    """
    with driver.session() as session:
        return session.run(query, properties).data()



def get_all_device_person():
    query = f"""
    MATCH (n:DevicePerson)
    WHERE n.device_id = $id
    RETURN n
    """
    with driver.session() as session:
        result = session.run(query).data()
        return [record["n"] for record in result]



def update_device_person(id, updates):
    query = f"""
    MATCH (n:DevicePerson)
    WHERE n.device_id = $id
    with (n) limit 1
    SET $updates
    RETURN n
    """
    with driver.session() as session:
        return session.run(query, {"id" :id, "updates" : updates}).data()


# DELETE operation

def delete_device_person(id):
    query = f"""
    MATCH (n:DevicePerson)
    WHERE n.device_id = $id
    with (n) limit 1
    DELETE n
    """
    with driver.session() as session:
        session.run(query, {"id" : id})
        return True

#
# HAS_MOVIE: Cinema -> Movie (One-to-Many)
# HAS_SEAT: Movie -> Seat (One-to-Many)
# RESERVES: Customer -> Seat (One-to-Many)

def get_device_person_by_id(id):
    query = f"""
    MATCH (n:DevicePerson)
    WHERE n.device_id = $id 
    WITH n LIMIT 1
    RETURN n
    """
    try:
        with driver.session() as session:
            # Pass the filters to the query or an empty dictionary
            result = session.run(query, {'id' : id}).data()
            # Return the device_person if it exists
            return [record["n"] for record in result] if result else []
    except Exception as e:
        print(f"Error executing query: {e}")
        return []


def create_relation_device_person(n1_id, n2_id, prop):
    # filter_query = " AND ".join([f"n.{key} = ${key}" for key in filters]) if filters else "1=1"
    properties = {
    "fnid" :  n1_id,
    "snid" :  n2_id,
        **prop
    }
    query = """
        MATCH (n:DevicePerson {device_id: $fnid}), (n2:DevicePerson {device_id: $snid})
        WITH n, n2 LIMIT 1
        MERGE (n)-[:CONNECTED {
            method: $method, 
            bluetooth_version: $bluetooth_version, 
            signal_strength_dbm: $signal_strength_dbm, 
            distance_meters: $distance_meters, 
            duration_seconds: $duration_seconds, 
            timestamp: $timestamp
        }] -> (n2)
        RETURN *
    """
    with driver.session() as session:
        res = session.run(query, properties).data()
        return res


def check_if_device_person_exist(id):
    query = f"""
        MATCH (n:DevicePerson)
        WHERE n.device_id = $id 
        RETURN COUNT(n) > 0 AS device_personExists
    """
    with driver.session() as session:
        # Run the query with filters as parameters
        res = session.run(query, {"id":id}).single()["device_personExists"]
        return res


#
# def get_device_person_relations(id):
#     query = f"""
#         MATCH (n:DevicePerson) -[rel:CONNECTED] - (n2:DevicePerson)
#         WHERE n.device_id = $id
#         RETURN rel
#     """
#     with driver.session() as session:
#         # Run the query with filters as parameters
#         res = session.run(query, {"id" : id}).single()
#         print(res)
#         relations = [record["rel"] for record in res]
#         return relations
#
#
# def check_timestamp_in_relations(id, timestamp):
#     relations = get_device_person_relations(id)
#     print(relations)
#     return any(r for r in relations if r["properties"]["timestamp"] == timestamp)

def get_device_person_relations(device_id, timestamp):
    query = """
         MATCH (a:DevicePerson{id: $device_id})-[r:CONNECTED]->()
    WHERE r.timestamp = $timestamp
    RETURN COUNT(r) > 0 AS is_busy
    """
    try:
        with driver.session() as session:
            result = session.run(query, {"device_id": device_id, "timestamp": timestamp}).single()
            return result["is_busy"] if result else False
    except Exception as e:
        return {"error": "Database Error", "details": str(e)}


def check_timestamp_in_relations(id, timestamp):
    relations = get_device_person_relations(id)

    # Check if relations is not empty
    if not relations:
        return False


    # Return True if any relation matches the timestamp
    #return any(r["properties"]["timestamp"] == timestamp for r in relations)
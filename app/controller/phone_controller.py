

from flask import Blueprint, request, jsonify

from app.neo4j_db.database import driver
from app.service.phone_service import add_device_phone

phone_blueprint = Blueprint("phone_tracker", __name__)



@phone_blueprint.route("/", methods=['POST'])
def get_interaction():
   add_device_phone(request.json)
   return jsonify({ }), 200


# Cypher query to find all devices connected via Bluetooth and calculate the path's total duration
query = """
    MATCH (n:DevicePerson)-[rel:CONNECTED {method: 'Bluetooth'}]->(n2:DevicePerson)
   RETURN n AS from_device, n2 AS to_device, rel
"""

@phone_blueprint.route('/bluetooth-connected/', methods=['GET'])
def get_bluetooth_connections():
    try:
        with driver.session() as session:
            result = session.run(query).data()
            return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


query1 = """
MATCH (n:DevicePerson)-[rel:CONNECTED]->(n2:DevicePerson)
WHERE rel.signal_strength_dbm > -60
RETURN n AS from_device, n2 AS to_device, rel
"""

@phone_blueprint.route('/signal_strength_dbm/', methods=['GET'])
def get_signal_strength_dbm_connections():
    try:
        with driver.session() as session:
            result = session.run(query1).data()
            return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

query2 = """
MATCH (n:DevicePerson)-[rel:CONNECTED]->(n2:DevicePerson)
WHERE n.device_id = $device_id
RETURN count(n2) AS connected_devices_count
"""

@phone_blueprint.route('/provided_id/<uid>', methods=['GET'])
def get_provided_id_connections(uid):
    try:
        with driver.session() as session:
            result = session.run(query2, {"device_id": uid}).data()
            return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

query3 = """
MATCH (n:DevicePerson)-[rel:CONNECTED]->(n2:DevicePerson)
WHERE n.device_id = $device_id_1 AND n2.device_id = $device_id_2
RETURN COUNT(rel) > 0 AS is_connected
"""

@phone_blueprint.route('/is_connected/<uid1>/<uid2>', methods=['GET'])
def get_is_connected_connections(uid1, uid2):
    try:
        with driver.session() as session:
            result = session.run(query3, {"device_id_1": uid1, "device_id_2": uid2}).data()
            return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


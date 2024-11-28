# CREATE operation
import json
import uuid
from dataclasses import asdict
import toolz as t
from app.neo4j_db.database import driver



# p = """
# create (u:User {name: david, age: 27 }) return u
# """



def create_node(node):
    type_class = node.__class__.__name__
    properties = {"data": dict(asdict(node))}
    query = f"""
    CREATE (n:{type_class} $data)
    RETURN n
    """
    with driver.session() as session:
        return session.run(query, properties).data()


@t.curry
def get_all_node(n_type, filters=None):
    filter_query = " AND ".join([f"n.{key} = ${key}" for key in filters]) if filters else "1=1"
    query = f"""
    MATCH (n:{n_type})
    WHERE {filter_query}
    RETURN n
    """
    with driver.session() as session:
        result = session.run(query, filters or {}).data()
        return [record["n"] for record in result]



# UPDATE operation
@t.curry
def update_node(n_type, filters, updates):
    filter_query = " AND ".join([f"n.{key} = ${key}" for key in filters]) if filters else "1=1"
    update_query = ", ".join([f"n.{key} = ${key}" for key in updates])
    query = f"""
    MATCH (n:{n_type})
    WHERE {filter_query}
    with (n) limit 1
    SET {update_query}
    RETURN n
    """
    with driver.session() as session:
        return session.run(query, {**filters, **updates}).data()


# DELETE operation
@t.curry
def delete_node(n_type,filters):
    filter_query = " AND ".join([f"n.{key} = ${key}" for key in filters]) if filters else "1=1"
    query = f"""
    MATCH (n:{n_type})
    WHERE {filter_query}
    with (n) limit 1
    DELETE n
    """
    with driver.session() as session:
        session.run(query, filters)
        return True

#
# HAS_MOVIE: Cinema -> Movie (One-to-Many)
# HAS_SEAT: Movie -> Seat (One-to-Many)
# RESERVES: Customer -> Seat (One-to-Many)

@t.curry
def create_relation_node(type_n1, type_n2, relation, n1_id, n2_id, prop=""):
    # filter_query = " AND ".join([f"n.{key} = ${key}" for key in filters]) if filters else "1=1"
    properties = {
    "str_n1_id" :  f"{{id:{n1_id}}}",
    "str_n2_id" :  f"{{id:{n2_id}}}",
    "relation" : relation,
    "prop" : prop
    }
    query = f"""
        MATCH (n:{type_n1}$str_n1_id,(n2:{type_n2}$str_n2_id)  
        with (n), (n2) limit 1
        merge (n) -[:$relation$prop]-> (n2)
        return *
        """
    with driver.session() as session:
        res = session.run(query, properties).data()
        print(res)
        return res


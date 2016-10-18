from neo4j.v1 import GraphDatabase, basic_auth

driver = GraphDatabase.driver("bolt://localhost", auth=basic_auth("neo4j", "jkliop"))
session = driver.session()


def insert_followed(user, followed):
    """
    :param followed:
        [('宇宙无敌大羙麗', '15443091'),...]
    """
    session.run("MERGE (a:Person {name:{name}, id:{id}})", {"user":user.name, "id": user.id})
    relation_str = '''
    MATCH (a: Person {id: {id}})
    MERGE (a)-[:FOLLOWED]->(x:Person {name:{fname}, fid: {fid}})
    ''' 
    with session.new_transaction() as tx:
        for f in followed
            session.run(relation_str, {"id", user.id, "fname": f[0], "fid": f[1]})
        tx.success = True

def ls():
    for friend in session.run("MATCH (a:Person {id:'15443091'})-[:KNOWS]->(x) RETURN x"):
    print('Alice says, "hello, %s"' % friend["name"])

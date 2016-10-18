from neo4j.v1 import GraphDatabase, basic_auth


driver = None

if driver is None:
    driver = GraphDatabase.driver("bolt://localhost", auth=basic_auth("neo4j", "jkliop"))


def insert_followed(user, followed):
    """
    :param followed:
        [('宇宙无敌大羙麗', '15443091'),...]
    """
    session = driver.session()

    relation_str = '''
    MATCH (a:Person {id: {id}})
    MERGE (a)-[:FOLLOWED]->(x:Person {name:{fname}, fid: {fid}})
    '''
    # 这条数据必须得在数据库中, 才能执行下边的操作
    session.run("MERGE (a:Person {name:{name}, id:{id}})", {"name": user["name"], "id": user["id"]})
    with session.begin_transaction() as tx:
        for f in followed:
            tx.run(relation_str, {"id": user["id"], "fname": f[0], "fid": f[1]})
        tx.success = True

    session.close()
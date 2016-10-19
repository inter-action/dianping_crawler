from neo4j.v1 import GraphDatabase, basic_auth
from .cypher_builder import *
from ..utils import StringUtils

driver = None

if driver is None:
    driver = GraphDatabase.driver("bolt://localhost", auth=basic_auth("neo4j", "jkliop"))

class PersistentLayer:

    @staticmethod
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

    @staticmethod
    def insert_reviews(user, reviews):
        assert len(reviews) >  0

        session = driver.session()
        """
        {'shop': {'tel': '17710850213',
            'id': '67862761',
            'name': 'AUV真人机械密室逃脱体验馆(芍药居店)',
            'addr': '朝阳区芍药居北里309号B1楼'}
            'href': '..',
         'rate': {'id': '309382395',  # 评论ID
            'image_ls': ['http://www.dianping.com/photos/600819018/member',
            'http://www.dianping.com/photos/600819019/member',
            'http://www.dianping.com/photos/600819020/member',
            'http://www.dianping.com/photos/600819021/member'],
            'rating': 5.0,
            'time': '16-10-16 12:37'},
            'shop': {'addr': '海淀区万泉河路68号紫金庄园7号楼-12A09',
            'id': '/www.dianping.com/shop/24820793',
            'name': '回未轰趴馆(人大店)',
            'tel': '15810026196'},
            'href': '..'}
        """
        shop = reviews[0]["shop"]
        rate = reviews[0]["rate"]
        placeholder_rate = build_placeholders(rate, prefix="r")
        placeholder_shop = build_placeholders(shop, prefix="s")
        relation_str = '''
                MATCH (a:Person {id: {uid}})
                MERGE (a)-[:RATED {%s}]->(:Shop {%s})
                '''

        relation_str = StringUtils.format(relation_str, placeholder_rate, placeholder_shop)
        # # 这条数据必须得在数据库中, 才能执行下边的操作
        session.run("MERGE (a:Person {name:{name}, id:{id}})", {"name": user["name"], "id": user["id"]})
        with session.begin_transaction() as tx:
            for row in reviews:
                shop = row["shop"]
                rate = row["rate"]

                shop_dict = prefix_dict(shop, prefix="s")
                rate_dict = prefix_dict(rate, prefix="r")
                merged = {**shop_dict, **rate_dict}
                merged["uid"] = user["id"]
                tx.run(relation_str, merged)
            tx.success = True

        session.close()

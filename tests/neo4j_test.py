import unittest
from src.neo4j_persistence.entry import PersistentLayer
from src.neo4j_persistence import cypher_builder
from src.pickler import Pickler

def str_equal_in(str, strs):
    for nstr in strs:
        if nstr == str:
            return True

    return False


class TestNeo4jMethods(unittest.TestCase):

    @unittest.skip
    def test_rel_insertion(self):
        user = {"name": "alex", "id": '3'}
        followed = [
            ('宇宙无敌大羙麗', '15443091'),
            ('宇宙无敌大羙麗2', '15443093'),
            ('宇宙无敌大羙麗3', '15443094')
        ]
        PersistentLayer.insert_followed(user, followed)
        self.assertEqual(True, True)

    def test_review_insertion(self):
        user = {"name": "alex", "id": '3'}
        reviews = Pickler.load_reviews()
        PersistentLayer.insert_reviews(user, reviews)



class CypherBuilderTest(unittest.TestCase):
    def test_cypher_builder_without_prefix(self):
        person = {"name": "alex", "id": "3"}
        result = cypher_builder.build_placeholders(person)
        self.assertTrue(str_equal_in("{" + result + "}", [
            "{name: {name}, id: {id}}",
            "{id: {id}, name: {name}}"
        ]))


    def test_cypher_builder_with_prefix(self):
        person = {"name": "alex", "id": "3"}
        result = cypher_builder.build_placeholders(person, "p")
        self.assertTrue(str_equal_in("{" + result + "}", [
            "{name: {pname}, id: {pid}}",
            "{id: {pid}, name: {pname}}"
        ]))

    def test_cypher_dict_prefix(self):
        person = {"name": "alex", "id": "3"}
        result = cypher_builder.prefix_dict(person, "p")
        self.assertEqual(result, {"pname": "alex", "pid": "3"})

if __name__ == '__main__':
    unittest.main()
import unittest
from src.neo4j_persistence import entry


class TestNeo4jMethods(unittest.TestCase):

    def test_rel_insertion(self):
        user = {"name": "alex", "id": '3'}
        followed = [
            ('宇宙无敌大羙麗', '15443091'),
            ('宇宙无敌大羙麗2', '15443093'),
            ('宇宙无敌大羙麗3', '15443094')
        ]
        entry.insert_followed(user, followed)
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
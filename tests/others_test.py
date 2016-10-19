import unittest
from src.utils import StringUtils

class TestStringMethods(unittest.TestCase):

    def test_upper(self):
        person = {"id": 33, "name": "alex"}
        tpl = "%s's id is %s"
        result = StringUtils.format(tpl, person["name"], person["id"])
        self.assertEqual(result, "alex's id is 33")




if __name__ == '__main__':
    unittest.main()
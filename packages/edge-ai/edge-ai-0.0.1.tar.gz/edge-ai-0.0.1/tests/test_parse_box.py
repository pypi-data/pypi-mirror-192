import unittest
from ei.utils.common import parse_box

class TestParseBox(unittest.TestCase):

    def test_parse_box(self):
        # Check that it is a tuple
        self.assertIs(type(parse_box("0,0,10,10")), tuple)


unittest.main()
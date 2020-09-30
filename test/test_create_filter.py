import unittest

from stackexchange import create_filter, base_filters

class TestFilter(unittest.TestCase):
    def test_filter_no_args(self):
        self.assertEqual(create_filter(), "default")

    def test_filter_base_default(self):
        self.assertEqual(create_filter(base_filters.DEFAULT), "default")

    def test_filter_base_withbody(self):
        self.assertEqual(create_filter(base_filters.WITHBODY), "withbody")

    def test_filter_base_none(self):
        self.assertEqual(create_filter(base_filters.NONE), "none")

    def test_filter_base_total(self):
        self.assertEqual(create_filter(base_filters.TOTAL), "total")

if __name__ == "__main__":
    unittest.main()

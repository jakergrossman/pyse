import unittest

from pyse import create_filter, base_filters

class TestDefaultFilters(unittest.TestCase):
    def test_filter_no_args(self):
        default_filter = create_filter()
        self.assertEqual(default_filter, "default")

    def test_filter_base_default(self):
        default_filter = create_filter(base=base_filters.DEFAULT)
        self.assertEqual(default_filter, "default")

    def test_filter_base_withbody(self):
        withbody_filter = create_filter(base=base_filters.WITHBODY)
        self.assertEqual(withbody_filter, "!7tRYRBs6sfcsYU38wnbid8.F5yky8jpmxi")

    def test_filter_base_none(self):
        none_filter = create_filter(base=base_filters.NONE)
        self.assertEqual(none_filter, "none")

    def test_filter_base_total(self):
        total_filter = create_filter(base=base_filters.TOTAL)
        self.assertEqual(total_filter, "total")

if __name__ == "__main__":
    unittest.main()

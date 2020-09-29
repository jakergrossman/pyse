from stackexchange import stackexchange

import unittest

class TestFilter(unittest.TestCase):
    def test_filter_no_args(self):
        self.assertEqual(stackexchange.create_filter(), "default")

if __name__ == "__main__":
    unittest.main()

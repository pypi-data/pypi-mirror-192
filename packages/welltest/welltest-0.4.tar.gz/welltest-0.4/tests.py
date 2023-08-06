from unittest import TestCase, main
from welltest.functions import *

class WellTestCase(TestCase):
    def test_r_from_rd_m(self):
        self.assertEqual(r_from_rd_m(1), 0.1)

    def test_pd_ei(self):
        self.assertAlmostEqual(pd_ei(1), 0.52214132)
        self.assertAlmostEqual(pd_ei(1, 10), 2.67444988e-13)


# Executing the tests in the above test case class
if __name__ == "__main__":
  main()
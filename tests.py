#!/usr/bin/env python3
import unittest
from icestorm_test import IcestormTestToolchain
from trellis_test import TrellisTestToolchain
from oxide_test import OxideTestToolchain

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(IcestormTestToolchain))
    suite.addTest(unittest.makeSuite(TrellisTestToolchain))
    suite.addTest(unittest.makeSuite(OxideTestToolchain))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())

#!/usr/bin/env python3

import os
import unittest

from common import *

class TrellisTestToolchain(unittest.TestCase):

    def test_simple(self):
        target = "lattice_ecp5_evn"
        full_targets_gen([target])
        compare_results(target)

    def test_nextpnr_args(self):
        target = "radiona_ulx3s"
        args= {
            "nextpnr-ignoreloops": True,
        }
        full_targets_gen([target], **args)
        compare_results(target, **args)

    def test_yosys_args(self):
        target = "gsd_orangecrab"
        args= {
            "yosys-nowidelut": True,
            "yosys-abc9":      True,

        }
        full_targets_gen([target], **args)
        compare_results(target, **args)

    def test_ecppack_args(self):
        target = "colorlight_i5"
        args= {
            "ecppack-bootaddr": 0x10,
            "ecppack-spimode": "qspi",
            "ecppack-freq": "19.4",
            "ecppack-compress": True,

        }
        full_targets_gen([target], **args)
        compare_results(target, **args)

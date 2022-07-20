#!/usr/bin/env python3

import os
import unittest

from common import *

class IcestormTestToolchain(unittest.TestCase):

    def test_simple(self):
        full_targets_gen(["icebreaker"])
        compare_results("icebreaker")

    def test_args(self):
        args= {
            "nextpnr-ignoreloops": True,
        }
        full_targets_gen(["tinyfpga_bx"], **args)
        compare_results("tinyfpga_bx", **args)

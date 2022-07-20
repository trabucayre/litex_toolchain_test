#!/usr/bin/env python3

import os
import unittest

from common import *

class OxideTestToolchain(unittest.TestCase):

    def test_simple(self):
        target = "lattice_crosslink_nx_evn"
        args = {
            "toolchain": "oxide",
        }
        full_targets_gen([target], **args)
        compare_results(target, **args)

    def test_es(self):
        target = "lattice_crosslink_nx_evn"
        args = {
            "toolchain": "oxide",
            "nexus-es-device": True,
        }
        full_targets_gen([target], **args)
        compare_results(target, **args)

    def test_nextpnr_args(self):
        target = "lattice_crosslink_nx_vip"
        args= {
            "toolchain": "oxide",
            "nextpnr-ignoreloops": True,
            "nextpnr-seed": 10,
        }
        full_targets_gen([target], **args)
        compare_results(target, **args)

    def test_yosys_args(self):
        target = "lattice_crosslink_nx_vip"
        args= {
            "toolchain": "oxide",
            "yosys-nowidelut": True,
            "yosys-abc9":      True,

        }
        full_targets_gen([target], **args)
        compare_results(target, **args)

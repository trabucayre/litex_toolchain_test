#!/usr/bin/env python3

import argparse
import subprocess
import os

from common import *

icestorm_targets = [
    "lattice_crosslink_nx_evn",
    "lattice_crosslink_nx_vip",
]

def compare_results(target_name, **kwargs):
    for key, value in kwargs.items():
        target_name += f"-{key}_{value}"
    build_dir_name = os.path.join(run_base_dir, target_name, "gateware")
    out_dir_name   = os.path.join(ref_base_dir, target_name)
    ref_files=[]
    for r, d, f in os.walk(out_dir_name):
        #print(f"{r} {d} {f}")
        for file in f:
            dd=os.path.relpath(r, out_dir_name)
            ref_files.append(os.path.join(dd, file))
    test_files=[]
    for r, d, f in os.walk(build_dir_name):
        for file in f:
            dd=os.path.relpath(r, out_dir_name)
            test_files.append(os.path.join(dd, file))

    if len(test_files) != len(ref_files):
        l1 = [os.path.basename(l) for l in test_files]
        l2 = [os.path.basename(l) for l in ref_files]

        print(f"error {build_dir_name} {out_dir_name}");
        #print(l1)
        #print(l2)
        if len(l1) > len(l2):
            t = set(l1) - set(l2)
        else:
            t = set(l2) - set(l1)
        for i in t:
            print(i)
        print("files list mismatch")
        check_list = list(set(ref_files) & set(test_files))
    else:
        check_list = ref_files

    for file in check_list:
        # check if file is not mem.init or verilog file
        constr_extension = os.path.splitext(file)[1][1:]
        if constr_extension in ["v", "init"]:
            continue
        ref_file  = os.path.join(out_dir_name, file)
        test_file = os.path.join(build_dir_name, file)
        with open(ref_file, "r") as fd:
            ref_cnt = [line for line in fd]
        with open(test_file, "r") as fd:
            test_cnt = [line for line in fd]
        for (r, t) in zip(ref_cnt, test_cnt):
            # Date and Auto-generated lines changes with date or hash
            if "Date" in r or "Auto-Generated" in r or "Autogenerated" in r:
                continue
            if r != t:
                print(f"{test_file} {ref_file}")
                min_len = len(r) if len(r) < len(t) else len(t)
                print(min_len)
                for i in range(min_len):
                    if r[i] != t[i]:
                        print(f"{i} {r[i]} {t[i]}")
                raise OSError(f"in {file}:\n{t}\ninstead of\n{r}")
    print("All fine")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--init',    action="store_true", help="init ref build.")
    parser.add_argument('--test',    action="store_true", help="init ref build.")
    parser.add_argument('--compare', action="store_true", help="init ref build.")
    parser.add_argument('--target',  default="",          help="target name. empty to test all")

    args = parser.parse_args()

    if args.target == "":
        targets = icestorm_targets
    else:
        targets = [args.target]

    if args.init:
        # Test targets.
        full_targets_gen(targets, True, toolchain="radiant", synth_mode="yosys")

    if args.test:
        full_targets_gen(targets, False, toolchain="radiant", synth_mode="yosys")

    if args.compare:
        for name in targets:
            if name == "colorlight_5a_75x":
                name = "colorlight_5a_75b"
            compare_results(name, toolchain="radiant", synth_mode="yosys")
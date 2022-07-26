import os
import shutil
import subprocess
from unittest import TestCase

# current directory
tests_dir    = os.path.dirname(__file__)
# references gateware base directory (absolute path)
ref_base_dir = os.path.join(tests_dir, "ref_build")
# test gateware base directory (absolute path)
run_base_dir = os.path.join(tests_dir, "build")

os.environ["PATH"] = os.path.join(tests_dir, "mocks") + ":" + os.environ["PATH"]

def create_dir_if_missing(dir_name):
    if not os.path.isdir(dir_name):
        try:
            os.mkdir(dir_name)
        except OSError:
            pass

def test_and_remove_dir(dir_name):
    if os.path.isdir(dir_name):
        try:
            shutil.rmtree(dir_name, ignore_errors=True)
        except OSError as e:
            print("rmdir failed")
            print(e)

def run_gen(target_name="", dir_name="", **kwargs):
    build_dir_name = os.path.join(run_base_dir, dir_name)
    out_dir_base = "ref_build"

    test_and_remove_dir(build_dir_name)

    cmd = f"python3 -m litex_boards.targets.{target_name} "
    cmd += "--cpu-type=vexriscv --cpu-variant=minimal --build --no-compile-software "
    out_dir_name = dir_name
    for key, value in kwargs.items():
        out_dir_name += f"-{key}_{value}"
        key = key.replace("_", "-")
        if isinstance(value, bool):
            cmd += f"--{key} "
        else:
            cmd += f"--{key} {value} "
    cmd += f"--output-dir build/{out_dir_name}"

    subprocess.check_call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, shell=True)

    if "STORE_REF_DESIGN" in os.environ:
        create_dir_if_missing(out_dir_base)
        ref_dir_name = os.path.join(out_dir_base, out_dir_name)
        test_and_remove_dir(ref_dir_name)
        gateware_dir = os.path.join("build", out_dir_name, "gateware")
        print(f"cp -rf {gateware_dir} {ref_dir_name}")
        os.system(f"cp -rf {gateware_dir} {ref_dir_name}")

def full_targets_gen(tgt_lst, **kwargs):
    for name in tgt_lst:
        dir_name = name
        if name.startswith("kosagi_fomu"):
            name = "kosagi_fomu"
        if kwargs == {}:
            run_gen(target_name=name, dir_name=dir_name)
        else:
            run_gen(target_name=name, dir_name=dir_name, **kwargs)

def compare_results(target_name, **kwargs):
    for key, value in kwargs.items():
        target_name += f"-{key}_{value}"
    build_dir_name = os.path.join(run_base_dir, target_name, "gateware")
    if not os.path.isdir(build_dir_name):
        print(f"Missing directory {build_dir_name}")
        assert False
    out_dir_name   = os.path.join(ref_base_dir, target_name)
    if not os.path.isdir(out_dir_name):
        print(f"Missing directory {out_dir_name}")
        assert False
    ref_files=[]
    for r, d, f in os.walk(out_dir_name):
        for file in f:
            dd=os.path.relpath(r, out_dir_name)
            ref_files.append(os.path.join(dd, file))
    test_files=[]
    for r, d, f in os.walk(build_dir_name):
        for file in f:
            dd=os.path.relpath(r, out_dir_name)
            test_files.append(os.path.join(dd, file))

    #print(f"{len(test_files)} {len(ref_files)}")
    #if len(test_files) != len(ref_files):
    #    l1 = [os.path.basename(l) for l in test_files]
    #    l2 = [os.path.basename(l) for l in ref_files]

    #    print(f"error {build_dir_name} {out_dir_name}");
    #    if len(l1) > len(l2):
    #        t = set(l1) - set(l2)
    #    else:
    #        t = set(l2) - set(l1)
    #    for i in t:
    #        print(i)
    #    print(f"files list mismatch {len(test_files)} {len(ref_files)}")
    #    check_list = list(set(ref_files) & set(test_files))
    #else:
    #    check_list = ref_files
    assert len(test_files) == len(ref_files)

    for file in ref_files:
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
            # read_xxx use absolute path
            if r.startswith("read_") and r.startswith("read_"):
                rl = r.split(' ')
                tl = t.split(' ')
                # read type
                TestCase().assertEqual(rl[0], tl[0])
                # if -include
                if len(rl) > 2:
                    TestCase().assertEqual(rl[1:-1], tl[1:-1])
                # last is always absolute path cut
                r = rl[-1].split('/')[-1]
                t = rl[-1].split('/')[-1]
                TestCase().assertEqual(r, t)
            else:
                tt = ' '.join(t.split(' '))
                rr = ' '.join(r.split(' '))
                if tt[-1] == '\n':
                    tt = tt[:-1]
                if rr[-1] == '\n':
                    rr = rr[:-1]
                TestCase().assertEqual(rr, tt, "Error for file "+ ref_file)


# Autogenerated by LiteX / git: ec05eeaa
set -e
yosys -l tinyfpga_bx.rpt tinyfpga_bx.ys
nextpnr-ice40 --json tinyfpga_bx.json --pcf tinyfpga_bx.pcf --asc tinyfpga_bx.asc  --pre-pack tinyfpga_bx_pre_pack.py --lp8k --package cm81 --timing-allow-fail --ignore-loops --seed 1 
icepack -s tinyfpga_bx.asc tinyfpga_bx.bin
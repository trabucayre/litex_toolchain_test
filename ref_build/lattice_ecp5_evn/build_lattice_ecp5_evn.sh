# Autogenerated by LiteX / git: 7acb6d46
set -e
yosys -l lattice_ecp5_evn.rpt lattice_ecp5_evn.ys
nextpnr-ecp5 --json lattice_ecp5_evn.json --lpf lattice_ecp5_evn.lpf --textcfg lattice_ecp5_evn.config --um5g-85k --package CABGA381 --speed 8 --timing-allow-fail --seed 1 
ecppack lattice_ecp5_evn.config --svf lattice_ecp5_evn.svf --bit lattice_ecp5_evn.bit  --bootaddr 0    

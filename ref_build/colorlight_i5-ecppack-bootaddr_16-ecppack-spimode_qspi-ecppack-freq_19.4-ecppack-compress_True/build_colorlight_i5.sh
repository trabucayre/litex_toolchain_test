# Autogenerated by LiteX / git: 7acb6d46
set -e
yosys -l colorlight_i5.rpt colorlight_i5.ys
nextpnr-ecp5 --json colorlight_i5.json --lpf colorlight_i5.lpf --textcfg colorlight_i5.config --25k --package CABGA381 --speed 6 --timing-allow-fail --seed 1 
ecppack colorlight_i5.config --svf colorlight_i5.svf --bit colorlight_i5.bit  --bootaddr 16 --spimode qspi --freq 19.4 --compress 
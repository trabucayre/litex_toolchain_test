# Autogenerated by LiteX / git: 7acb6d46
set -e
yosys -l gsd_orangecrab.rpt gsd_orangecrab.ys
nextpnr-ecp5 --json gsd_orangecrab.json --lpf gsd_orangecrab.lpf --textcfg gsd_orangecrab.config --25k --package CSFBGA285 --speed 8 --timing-allow-fail --seed 1 
ecppack gsd_orangecrab.config --svf gsd_orangecrab.svf --bit gsd_orangecrab.bit  --bootaddr 0    

# dune-crp-geo-tester
The fcl `checkgeovdtpc.fcl` runs the `CheckCRPGeometry` module. If the "DumpWires" is set to true it will make a dump wire ASCII file. 
The dump file can be drawn with `WireDumpDraw.py`, which needs matplotlib.

To make a dump file grep on "FLAG"
```
lar -c checkgeovdtpc.fcl | grep FLAG > <ascii_dump_file>.txt
```

For matplolib install use venv:
```
python3 -m venv mplot
source mplot/bin/activate
pip install matplotlib PyQt5
```

once the dump file `<ascii_dump_file>.txt` is produced, one can draw its content for a given plane
```
python WireDumpDraw.py -f <ascii_dump_file>.txt -p <0, 1, or 2>
```
optionally one can specify to draw only every ith wire with `-s` argument (default is 16).

Example setup local product (version 09_58_02 and qualifier e20:prof here)
```
source /cvmfs/dune.opensciencegrid.org/products/dune/setup_dune.sh
source localProducts_09_58_02_e20_prof/setup
mrbslp 
setup dunesw v09_58_02d00 -q e20:prof 
```
check with `ups active` that the desired product installed in `localProducts_xxxx` is set up.

# channel checker

The script `ChannelCheck.py` verifies the basic channel counts for CRPs.
```
usage: ChannelCheck.py [-h] -f FILE [-c CHANNELS] [-n NCRP]

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  wire dump file
  -c CHANNELS, --channels CHANNELS
                        number of channels per CRP
  -n NCRP, --ncrp NCRP  number of CRPs
```

Example:
```
ython ChannelCheck.py -f wiredump_1x8x6_v181122.txt -c 3072 -n 12
Analyzing the file wiredump_1x8x6_v181122.txt
Expected number of CRPs            : 12
Expected number of channel per CRP : 3072
Expected number of total channels  : 36864
[ PASS ] [check_totch_count] Total number of channels expected / found: 36864 / 36864
[ PASS ] [check_viewch_count] Number of channels per each CRP view: [952, 952, 1168]
```
Given the number of specified channels per CRP and the total number of CRPs expected for the geometry wire dump file. The script tries to figure out if the channels numbers are consistent per CRP. Example above case of FD2 dump file but with `nCRP = 11` would generate a check failure:
```
python ChannelCheck.py -f wiredump_1x8x6_v181122.txt -c 3072 -n 11
Analyzing the file wiredump_1x8x6_v181122.txt
Expected number of CRPs            : 11
Expected number of channel per CRP : 3072
Expected number of total channels  : 33792
[ FAIL ] [check_totch_count] Total number of channels expected / found: 33792 / 36864
```

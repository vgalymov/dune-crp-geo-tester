# dune-crp-geo-tester
check the list of active products: `ups active`

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

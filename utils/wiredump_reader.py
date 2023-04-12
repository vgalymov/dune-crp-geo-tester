import re
import traceback

def read_dump_file( filename ):
    res = []
    with open(filename) as fin:
        for line in fin:
            try:
                lst = re.findall(r"[-+]?(?:(?:\d*\.\d+)|(?:\d+\.?))(?:[Ee][+-]?\d+)?", line)
                d = {}
                d['ch']    = int(lst[0])
                d['cryo']  = int(lst[1])
                d['tpc']   = int(lst[2])
                d['plane'] = int(lst[3])
                d['wire']  = int(lst[4])
                d['start'] = [float(lst[5]),float(lst[6]),float(lst[7])]
                d['stop']  = [float(lst[8]),float(lst[9]),float(lst[10])]
                res.append(d)
            except:
                print(f"could not process {line}")
                print(traceback.format_exc())
                continue

    return res


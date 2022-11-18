import sys
import re
import math
import argparse
import matplotlib.pyplot as plt

    
class wire:
    def __init__(self, tid, pid, wid, x0, y0, x1, y1):
        self.tpc_   = tid
        self.plane_ = pid
        self.wire_  = wid
        self.start_ = [x0, y0]
        self.end_   = [x1, y1]
        self.len_   = self.__length()
    
    def __length(self):
        x0 = self.start_[0]
        y0 = self.start_[1]
        x1 = self.end_[0]
        y1 = self.end_[1]
        l = math.sqrt((x1 - x0)**2 + (y1 - y0)**2)
        return l



#
#
def get_channels_from_dump( fname ):
    chans = {}
    
    with open(fname) as fin:
        for line in fin:
            lst = line.split(' ')
            sval = 0
            if( line.startswith("FLAG") ): sval = 1
            try:
                ch  = int(lst[sval])
                tid = int(lst[sval+2])
                pid = int(lst[sval+3])
                wid = int(lst[sval+4])
                x0  = float(lst[sval+6])
                y0  = float(lst[sval+7])
                x1  = float(lst[sval+9])
                y1  = float(lst[sval+10])

                w = wire( tid, pid, wid, x0, y0, x1, y1 )
                if( not ch in chans ): chans[ch] = []
                chans[ch].append( w )

            except (ValueError, IndexError):
                continue
    return chans



#
#
def get_strip_len_crp( chan_record, crpch, view ):
    chans = sorted(chan_record)
    ch_sstrip = []
    ch_mstrip = []
    for ch in chans:
        if( ch >= crpch ): break
        plist = [ w.plane_ for w in chan_record[ch] ]
        if( not all( x == plist[0] for x in plist )):
            print(f"mistmatch in plane id for channel {ch}")
        if( plist[0] != view ): continue
        lens = [ w.len_ for w in chan_record[ch] ]
        ltot = sum(lens)
        if( len(lens) == 1 ):
            ch_sstrip.append( [ch, ltot] )
        else:
            ch_mstrip.append( [ch, ltot] )

    return ch_sstrip, ch_mstrip


if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', help='wire dump file',
                        required = True, type=str )
    parser.add_argument('-c', '--channels', help='number of channels per CRP',
                        default = 3072, type=int)
    parser.add_argument('-p', '--plane', help='view plane id',
                        default = 0, type=int)
    
    args  = parser.parse_args()
    crpch = args.channels
    plane = args.plane
    fname = args.file

    print(f"Analyzing the file {fname}");
    print(f"Expected number of channel per CRP : {crpch}")

    
    fig, ax = plt.subplots( figsize=(10,6) )
    ax.set(xlabel=f"CRP channel for plane {plane}", ylabel="strip length (cm)")
    chan_record = get_channels_from_dump( fname )
    sstrip, mstrip = get_strip_len_crp( chan_record, crpch, plane )
    print( "Single wires : ", len(sstrip))
    print( "Multi wires  : ", len(mstrip))
    if( sstrip ):

        x_ss, y_ss = map(list, zip(*sstrip))
        ax.scatter( x_ss, y_ss, marker='o', label = "geo wire single" )
    if( mstrip ):
        x_ms, y_ms = map(list, zip(*mstrip))
        ax.scatter( x_ms, y_ms, marker='o', label = "geo wire multiple" )

    plt.legend() #loc="upper left")
    plt.grid()
    plt.show()

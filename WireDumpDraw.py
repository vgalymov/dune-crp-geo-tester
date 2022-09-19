import sys
import re
import math
import argparse
import numpy as np
import matplotlib.pyplot as plt

##
class geo_wire:
    def __init__(self, ch, wid, endpts ):
        self._ch     = ch
        self._id     = wid
        self._endpts = endpts

##
class geo_plane:
    def __init__(self, pid):
        self._id = pid
        self._wires = []

    def n(self):
        return len(self._wires)

    def add_wire( self, pid, ch, wire, endpts ):
        if( pid != self._id ): return
        self._wires.append( geo_wire(ch, wire, endpts) )

##
class geo_tpc:
    def __init__(self, tid):
        self._id = tid
        self._planes = []

    def n(self):
        return len(self._planes)
    
    def add_plane( self, tid, plane ):
        if( tid != self._id): return
        self._planes.append( geo_plane( plane ) )

    def add_wire( self, tid, pid, ch, wid, endpts ):
        if( tid != self._id): return
        if( pid >= len( self._planes ) ): return
        self._planes[pid].add_wire( pid, ch, wid, endpts)
        
            

def init( fname ):
    tpcs = [geo_tpc(0), geo_tpc(1), geo_tpc(2), geo_tpc(3)]
    for t in tpcs:
        t.add_plane( t._id, 0)
        t.add_plane( t._id, 1)
        t.add_plane( t._id, 2)

    
    with open(fname) as fin:
        for line in fin:
            lst = line.split(' ')
            #print(len(lst))
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
                
                tpcs[tid].add_wire(tid, pid, ch, wid, [[x0,y0], [x1,y1]])
            except (ValueError, IndexError):
                #print("bad format {}".format(line))
                continue
            


    for t in tpcs:
        print(t.n())
        for p in t._planes:
            print('  ',p.n())

    return tpcs

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', help='wire dump file',
                        required = True, type=str )
    
    parser.add_argument('-p', '--plane', help='wire plane',
                        default = 0, type=int)

    parser.add_argument('-s', '--skip', help='skip wires',
                        default = 16, type=int)
    args  = parser.parse_args()

    
    tpcs = init( args.file )
    fig, ax2d = plt.subplots( nrows = 1, ncols = 1, figsize=(16,10),
                              sharex = 'col', sharey = 'row' )
    axs = [ax2d, ax2d, ax2d, ax2d]
    axs[0].set(xlabel="y (cm)", ylabel="z (cm")
    axs[2].set(ylabel="z (cm)")
    axs[1].set(xlabel="y (cm)")
    
    plot_plane = args.plane
    plot_wskip = args.skip  # draw every nth ch
    fig.suptitle(f"{args.file}: Plot plane {plot_plane}")
        
    clrs = ['r', 'b', 'g', 'm']
    for t in tpcs:
        #if( t._id in (2, 3) ): continue
        p  = t._planes[plot_plane]
        ws = p._wires
        for i in range(len(ws)):
            if( i % plot_wskip != 0 and i != (len(ws)+1) ): continue
            xpos = [ ws[i]._endpts[0][0], ws[i]._endpts[1][0] ]
            ypos = [ ws[i]._endpts[0][1], ws[i]._endpts[1][1] ]
            axs[t._id].plot(xpos, ypos, color= clrs[t._id])
            if( plot_plane == 0 ):
                axs[t._id].annotate( f"{ws[i]._ch}:{ws[i]._id}",
                                     [0.5*(xpos[0]+xpos[1]), 0.5*(ypos[0]+ypos[1])],  fontsize=7)
            elif( plot_plane == 1):
                axs[t._id].annotate( f"{ws[i]._ch}:{ws[i]._id}",
                                     [0.5*(xpos[0]+0.99*xpos[1]), 0.5*(ypos[0]+ypos[1])],  fontsize=7, rotation = 90)
            else:
                axs[t._id].annotate( f"{ws[i]._ch}:{ws[i]._id}",
                                    [0.5*(xpos[0]+xpos[1]), 0.5*(ypos[0]+ypos[1])],  fontsize=7)
                                
    #
    #
    plt.subplots_adjust(wspace=0, hspace=0)
    plt.show()

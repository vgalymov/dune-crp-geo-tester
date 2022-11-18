#!/usr/bin/env python3

import sys
import re
import math
import argparse

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

def print_ok(msg):
    print(f"[{bcolors.OKGREEN} PASS {bcolors.ENDC}] {msg}")

def print_fail(msg):
    print(f"[{bcolors.FAIL} FAIL {bcolors.ENDC}] {msg}")
    
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
def check_totch_count( chan_record, nch_exp ):
    chk_name = 'check_totch_count'
    nch    = len(chan_record)
    passed = True
    if( nch != nch_exp ): passed = False
    msg = f"[{chk_name}] Total number of channels expected / found: {nch_exp} / {nch}"
    if( not passed ):
        print_fail( msg )
        return False
    print_ok( msg )
    return True

#
#
def check_viewch_count( chan_record, crpch, ncrp ):
    chk_name = 'check_viewch_count'
    # first check that all channels follow each other
    chans = sorted(chan_record)
    if( len(list(filter(lambda i: i!=-1, [chans[i]-chans[i+1] for i in range(len(chans)-1) ]))) ):
        print_fail( f"[{chk_name}] Channel increment is incorrect" )
        return False

    # check
    crp_chans = []
    for ch in chans:
        if( ch % crpch == 0 ): crp_chans.append({0:0, 1:0, 2:0})
        pids = [ w.plane_ for w in chan_record[ch] ]
        pid  = sum(pids)/len(pids)
        if( not pid.is_integer() ):
            msg = f"Multiple wire planes found {pids}"
            print_fail( f"[{chk_name}] {msg}" )
            return False
        pid = int(pid)
        if( pid not in crp_chans[-1]):
            msg = f"Plane ID {pid} does not appear to be valid"
            print_fail( f"[{chk_name}] {msg}" )
            return False
        crp_chans[-1][pid] += 1

    if( ncrp != len(crp_chans)):
        msg = f"Mistmatch in number of CRPs found"
        print_fail( f"[{chk_name}] {msg}" )
        return False

    # check that all views have the same number of channels
    views  = sorted(crp_chans[0])
    viewch = len(views)*[0]
    for view in views:
        lst = ncrp * [0]
        for i in range(ncrp): lst[i] = crp_chans[i][view]
        if( not all( x == lst[0] for x in lst )):
            msg = f"Mistmatch in channel numbers in view {view}: {lst}"
            print_fail( f"[{chk_name}] {msg}" )
            return False
        viewch[ view ] = lst[0]

    #print(viewch)
    stot = ( sum (viewch) == crpch )
    if( not stot ):
        msg = f"Mistmatch in view channel number sum: {viewch}"
        print_fail( f"[{chk_name}] {msg}" )
        return False

    msg = f"Number of channels per each CRP view: {viewch}"
    print_ok(f"[{chk_name}] {msg}" )
    
    return True


if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', help='wire dump file',
                        required = True, type=str )
    parser.add_argument('-c', '--channels', help='number of channels per CRP',
                        default = 3072, type=int)
    parser.add_argument('-n', '--ncrp', help='number of CRPs',
                        default = 1, type=int)
    
    args  = parser.parse_args()
    ncrp  = args.ncrp
    crpch = args.channels
    totch = ncrp * crpch
    fname = args.file
    
    print(f"Analyzing the file {fname}");
    print(f"Expected number of CRPs            : {ncrp}")
    print(f"Expected number of channel per CRP : {crpch}")
    print(f"Expected number of total channels  : {totch}")
    
    #print_ok(f"{fname} {totch}")
    chan_record = get_channels_from_dump( fname )
    if( not check_totch_count( chan_record, totch ) ): sys.exit(1)
    elif( not check_viewch_count( chan_record, crpch, ncrp )): sys.exit(1)
    

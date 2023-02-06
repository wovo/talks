# ===========================================================================
#
# file     : gf_timing.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2023
# license  : MIT license, see license variable in the __init__.py
#
# This file is part of the Godafoss perhiperal interface library.
#
# This file provides simple benchmarking functions
#
# ===========================================================================

import gc

from godafoss.gf_time import *

last_time = None

def report( s: str = None ):
    global last_time
    if s is None:
        gc.collect()
        last_time = ticks_us()
    else:
        after_call = ticks_us()
        gc.collect()
        after_collect = ticks_us()
        
        elapsed = ticks_us() - last_time
        collect = after_collect - after_call
        
        print( s, elapsed, collect )
        
        last_time = ticks_us()
    

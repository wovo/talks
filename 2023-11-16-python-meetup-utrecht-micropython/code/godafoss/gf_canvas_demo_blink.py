# ===========================================================================
#
# file     : gf_canvas_demo_blink.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2023
# license  : MIT license, see license variable in the __init__.py
#
# This file is part of the Godafoss perhiperal interface library.
#
# This file contains various canvas demos
#
# ===========================================================================

from godafoss.gf_time import *
from godafoss.gf_color import *


# ===========================================================================

def canvas_demo_blink(
    s: canvas,
    pause: int =  1000_000,
    iterations = None, 
    sequence = ( colors.white, colors.black )
):
    print( "canvas demo blink" )
         
    for _ in repeater( iterations ):
        
        for c in sequence:   
            s.clear( c )
            s.flush()
            sleep_us( pause )

# ===========================================================================

# ===========================================================================
#
# file     : gf_moving_text.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2023
# license  : MIT license, see license variable in the __init__.py
#
# This file is part of the Godafoss perhiperal interface library.
#
# This file contains the (abstract) adc class.
#
# ===========================================================================

from godafoss.gf_time import *
from godafoss.gf_timing import *
from godafoss.gf_tools import *
from godafoss.gf_canvas import *
from godafoss.gf_text import *


# ===========================================================================

def moving_text(
    s: canvas,
    t: [str, text ],
    pixel_pause: int =  1_000,
    text_pause: int = 1_000_000,
    iterations = None, 
):
    if isinstance( t, str ):
        t = text( t )
    for _ in repeater( iterations ):
        for x in range( 0, t.size.x - s.size.x ):
            report()
            s.clear()
            report( "clear" )
            s.write( t @ xy( - x, 0 ) )
            report( "write" )
            s.flush()
            report( "flush" )
            sleep_us( pixel_pause )
        sleep_us( text_pause )
            
    
# ===========================================================================
#
# file     : gf_canvas_demos.py
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

from random import randint

from godafoss.gf_time import *
from godafoss.gf_tools import *
from godafoss.gf_xy import *
from godafoss.gf_line import *
from godafoss.gf_rectangle import *
from godafoss.gf_circle import *
from godafoss.gf_text import *
from godafoss.gf_ggf import *

        
# ===========================================================================

def canvas_demo_scrolling_text(
    s: canvas,
    t: [ str, "text" ],
    scroll_pause: int =  100,
    end_pause: int = 1_000_000,
    iterations = None, 
):
    print( "canvas demo scrolling text" )
        
    if isinstance( t, str ):
        t = text( t )
        
    for _ in repeater( iterations ):
        for x in range( 0, t.size.x - s.size.x ):
            s.clear()
            s.write( t @ xy( - x, 0 ) )
            s.flush()
            sleep_us( scroll_pause )
        sleep_us( end_pause )

# ===========================================================================

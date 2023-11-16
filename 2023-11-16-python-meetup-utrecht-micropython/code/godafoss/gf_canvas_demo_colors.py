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

def canvas_demo_colors(
    s: canvas,
    pause: int =  1000_000,
    iterations = None, 
):
    print( "canvas demo colors" )
         
    for _ in repeater( iterations ):
        
        for c, name in (
            ( colors.red, "RED" ),
            ( colors.green, "GREEN" ),
            ( colors.blue, "BLUE" ),
            ( colors.white, "WHITE" ),
            ( colors.black, "BLACK" ),
        ):    
            s.clear( c )
            s.write( name, ink = -c )
            s.flush()
            sleep_us( pause )

# ===========================================================================

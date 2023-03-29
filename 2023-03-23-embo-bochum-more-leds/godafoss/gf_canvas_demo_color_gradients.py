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

def canvas_demo_color_gradients(
    display: canvas,
    pause: int = 50_000,    
    iterations = None, 
):
    print( "canvas demo colors gradients" )
    
    for _ in repeater( iterations ):    
         
        steps = 8
        dx = min( 20, ( display.size.x - 2 ) // steps )
        dy = min( 20, ( display.size.y - 2 ) // steps )

        display.clear()    
        display.flush()
        sleep_us( pause )         

        display.write( rectangle( xy( 2 + steps * dx, 2 + 3 * dy ) ) )
        display.flush()
        sleep_us( pause )
        
        y = 1
        for c in ( colors.red, colors.green, colors.blue ):
            ink = c
            x = 1
            for i in range( steps ):
                display.write(
                    rectangle( xy( dx, dy ), fill = True ),
                    location = xy( x, y ),
                    ink = ink
                )
                display.flush()
                sleep_us( pause )                
                ink = ( ink // 2 ) + ( ink // 4 )
                x += dx
            y += dy
    

# ===========================================================================

# ===========================================================================
#
# file     : gf_canvas_demo_rectangles.py
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
from godafoss.gf_rectangle import *

       
# ===========================================================================

def canvas_demo_rectangles( 
    s : canvas, 
    iterations = None, 
    frame = True 
):

    print( "canvas demo rectangles" )
    
    for _ in repeater( iterations ):    

        s.clear()
        if frame:
            s.write( rectangle( s.size ) )
            s.flush()
            
        for dummy in range( 0, 10 ):
            start = xy(
                randint( 0, s.size.x - 1 ),
                randint( 0, s.size.y - 1 )
            )
            end = xy(
                randint( 0, s.size.x - 1 ),
                randint( 0, s.size.y - 1 )
            )
            s.write( rectangle( end - start ) @ start )
            s.flush()
            sleep_us( 100_000 )            
            
        sleep_us( 2_000_000 )        
        

# ===========================================================================

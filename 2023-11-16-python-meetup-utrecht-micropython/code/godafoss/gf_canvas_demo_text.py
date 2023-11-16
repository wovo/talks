# ===========================================================================
#
# file     : gf_canvas_demo_text.py
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
from godafoss.gf_text import *

        
# ===========================================================================

def canvas_demo_text( 
    s : canvas, 
    iterations = None, 
    frame = True 
):

    print( "canvas demo text" )
    
    for _ in repeater( iterations ):    

        s.clear()
        if frame:
            s.write( rectangle( s.size ) )
            s.flush()
            sleep_us( 500_000 )
        
        s.write( text( "Hello world" ) @ xy( 1, 1 ) )
        s.flush()
        sleep_us( 500_000 )
        
        s.write( text( "Micropython" ) @ xy( 1, 9 ) )
        s.flush()
        sleep_us( 500_000 )
        
        s.write( text(  "+ Godafoss" ) @ xy( 1, 17 ) )
        s.flush()
        sleep_us( 2_000_000 )

# ===========================================================================

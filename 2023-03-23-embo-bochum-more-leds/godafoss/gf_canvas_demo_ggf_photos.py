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

def canvas_demo_ggf_photos( 
    s: canvas,
    location: str,
    iterations = None
):
    import os
    
    print( "canvas demo ggf photos\non %s lcd" % s.size )

    s.clear()
    s.write( text( "SD card photos demo\nfrom %s" % location ) )
    s.flush()

    files = list( os.listdir( location ) )
    files.sort()

    for _ in repeater( iterations ):    

        for name in files:
            print( "next file %s" % name )
            s.clear()
            elapsed = elapsed_us( lambda :
                s.write(
                    ggf( location + "/" + name ),
                    xy( 0, 24 )
                )
            )
            s.write(
                text( "file %s/%s\nloaded in %d ms" %
                    ( location, name, elapsed // 1000 )
                )      
            )
            s.flush()    

# ===========================================================================

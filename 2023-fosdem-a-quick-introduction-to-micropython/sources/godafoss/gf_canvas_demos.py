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
from godafoss.gf_benchmark import *
from godafoss.gf_tools import *
from godafoss.gf_xy import *
from godafoss.gf_line import *
from godafoss.gf_rectangle import *
from godafoss.gf_circle import *
from godafoss.gf_text import *
from godafoss.gf_ggf import *


# ===========================================================================

def canvas_demo_lines(
    s : canvas,
    iterations: None = None,
    frame = True
):

    print( "canvas demo lines" )
    
    for _ in repeater( iterations ):    

        s.clear()
        if frame:
            s.write( rectangle( s.size ) )
            s.flush()
            
        for _ in range( 0, 20 ):
            start = xy(
                randint( 0, s.size.x - 1 ),
                randint( 0, s.size.y - 1 ) )
            end = xy(
                randint( 0, s.size.x - 1 ),
                randint( 0, s.size.y - 1 ) )
            s.write( line( end - start ) @ start )
            s.flush()
            sleep_us( 100_000 )
            
        sleep_us( 2_000_000 )
        
# ===========================================================================

def canvas_demo_rectangles( s : sheet, iterations = None, frame = True ):

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

def canvas_demo_circles( s : sheet, iterations = None, frame = True ):

    print( "canvas demo circles" )
    
    for _ in repeater( iterations ):    

        s.clear()
        if frame:
            s.write( rectangle( s.size ) )
            s.flush()
            
        for _ in range( 0, 20 ):
            start = xy(
                randint( 0, s.size.x - 1 ),
                randint( 0, s.size.y - 1 )
            )
            radius = randint( 0, min( s.size.x, s.size.y ) // 2 )
            end = xy(
                randint( 0, s.size.x - 1 ),
                randint( 0, s.size.y - 1 )
            )
            s.write( circle( radius ) @ start )
            s.flush()
            sleep_us( 100_000 )            
            
        sleep_us( 2_000_000 )
        

# ===========================================================================

def canvas_demo_text( s : sheet, iterations = None, frame = True ):

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

def canvas_demo_scrolling_text(
    s: sheet,
    t: [ str, text ],
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

def canvas_demo_colors(
    s: sheet,
    pause: int =  1000_000,
    iterations = None, 
):
    print( "canvas demo colors" )
         
    for _ in repeater( iterations ):
        for c, name in (
            ( colors.red, "RED" ),
            ( colors.green, "GREEN" ),
            ( colors.blue, "BLUE" ),
        ):    
            s.clear( c )
            s.write( text( name ) )
            s.flush()
            sleep_us( pause )

# ===========================================================================

def canvas_demo_color_gradients(
    display: canvas,
    pause: int =  1000_000
):
    print( "canvas demo colors gradients" )
         
    display.clear()
    display.flush()
    
    y = 1
    dy = 20
    dx = 20
    steps = 8

    display.write( rectangle( xy( 2 + steps * dx, 2 + 3 * dy ) ) )
    for c in ( colors.red, colors.green, colors.blue ):
        ink = c
        x = 1
        for i in range( steps ):
            display.write(
                rectangle( xy( dx, dy ), fill = True ),
                xy( x, y ),
                ink
            )
            ink = ( ink // 2 ) + ( ink // 4 )
            x += dx
        y += dy
    display.flush()
    sleep_us( pause )
    

# ===========================================================================

def canvas_demo( 
    s: sheet,
    iterations = None
):
    print( "canvas demos", s.size )

    for _ in repeater( iterations ):
        if s.is_color:
            canvas_demo_colors( s, iterations = 1 )
            canvas_demo_color_gradients( s )
        canvas_demo_lines( s, iterations = 1 )
        canvas_demo_rectangles( s, iterations = 1 )
        canvas_demo_circles( s, iterations = 1 )
        canvas_demo_text( s, iterations = 1 )
        if 0: canvas_demo_scrolling_text(
            s,
            "Hello fantastic brave new world!\nusing Godafoss",
            iterations = 1
        )
        
    
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

import godafoss as gf
import edge

neopixels = gf.ws281x( edge.p5, 500 )
          
while True:

    neopixels.clear( gf.colors.white )
    neopixels.flush()
    gf.sleep_us( 500_000 )    
    
    neopixels.clear( gf.colors.black )
    neopixels.flush()
    gf.sleep_us( 500_000 ) 
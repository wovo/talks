import godafoss as gf
import edge

neopixels = gf.ws281x( edge.p5, 500 )
          
neopixels.clear( )
neopixels.flush()

# ===========================================================================

class tcs3472:

    def __init__( self, bus, address = 0x29, leds = pin_out_dummy ):
        self.bus = bus
        self.address = address
        self.leds = leds
        self.bus.writeto( self.address, b'\x80\x03' )
        self.bus.writeto( self.address, b'\x81\x2B' )

    def read( self ):
        self.bus.writeto( self.address, b'\xB4' )
        data = self.bus.readfrom( self.address, 8 )
        clear = data[ 0 ] + ( data[ 1 ] << 8 )
        red = data[ 2 ] + ( data[ 3 ] << 8 )
        green = data[ 4 ] + ( data[ 5 ] << 8 )
        blue = data[ 6 ] + ( data[ 7 ] << 8 )
        m = max( red, green, blue )
        print( clear, red, green, blue )
        return color( red, green, blue )      
        
    def demo( self ):
        print( "tcs3472 color sensor demo" )
        while True:
            # print( self.read() )
            self.read()
            time.sleep_us( 500_000 )
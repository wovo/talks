from godafoss.gf_tools import *
from godafoss.gf_make_pins import *

import machine

# ===========================================================================


class mrfc522:
    "Hello"

    class status:
        OK = 0
        NOTAGERR = 1
        ERR = 2

    class cmd:
        REQIDL = 0x26
        REQALL = 0x52
        AUTHENT1A = 0x60
        AUTHENT1B = 0x61

    def __init__( 
        self, 
        spi, 
        cs: [ int, pin_out, pin_in_out, pin_oc ], 
        rst: [ int, pin_out, pin_in_out, pin_oc ], 
    ):
        "hello"
        self._spi = spi
        self._cs = make_pin_out( cs )
        self._rst = make_pin_out( rst )
        self.reset()
        
    def reset( self ):        
        self._rst.write( 0 )
        self._cs.write( 1 )
        self._rst.write( 1 )

        self.register_write( 0x01, 0x0F )
        
        self.register_write( 0x2A, 0x8D )
        self.register_write( 0x2B, 0x3E )
        self.register_write( 0x2D,   30 )
        self.register_write( 0x2C,    0 )
        self.register_write( 0x15, 0x40 )
        self.register_write( 0x11, 0x3D )
        self.antenna_on()

    def register_write( self, reg, val ):
        "hello"
        self._cs.write( 0 )
        self._spi.write( b'%c' % int(0xff & ((reg << 1) & 0x7e)) )
        self._spi.write( b'%c' % int(0xff & val) )
        self._cs.write( 1 )

    def register_read( self, reg ):
        "hello"
        self._cs.write( 0 )
        self._spi.write(b'%c' % int(0xff & (((reg << 1) & 0x7e) | 0x80)))
        val = self._spi.read( 1 )
        self._cs.write( 1 )
        return val[ 0 ]

    def _sflags(self, reg, mask):
        "hello"
        self.register_write( reg, self.register_read( reg ) | mask )

    def _cflags(self, reg, mask):
        "hello"
        self.register_write( reg, self.register_read( reg ) & (~mask) )

    def _tocard( self, cmd, send ):
        "hello"
        recv = []
        bits = irq_en = wait_irq = n = 0
        stat = self.status.ERR

        if cmd == 0x0E:
            irq_en = 0x12
            wait_irq = 0x10
        elif cmd == 0x0C:
            irq_en = 0x77
            wait_irq = 0x30

        self.register_write( 0x02, irq_en | 0x80 )
        self._cflags( 0x04, 0x80 )
        self._sflags( 0x0A, 0x80 )
        self.register_write( 0x01, 0x00 )

        for c in send:
            self.register_write( 0x09, c )
        self.register_write( 0x01, cmd )

        if cmd == 0x0C:
            self._sflags( 0x0D, 0x80 )

        i = 2000
        while True:
            n = self.register_read( 0x04 )
            i -= 1
            if ~(( i != 0 ) and ~( n & 0x01 ) and ~( n & wait_irq )):
                break

        self._cflags( 0x0D, 0x80 )

        if i:
            if ( self.register_read( 0x06) & 0x1B ) == 0x00:
                stat = self.status.OK

                if n & irq_en & 0x01:
                    stat = self.status.NOTAGERR
                elif cmd == 0x0C:
                    n = self.register_read( 0x0A )
                    lbits = self.register_read( 0x0C ) & 0x07
                    if lbits != 0:
                        bits = ( n - 1 ) * 8 + lbits
                    else:
                        bits = n * 8

                    if n == 0:
                        n = 1
                    elif n > 16:
                        n = 16

                    for _ in range( n ):
                        recv.append( self.register_read( 0x09 ) )
            else:
                stat = self.status.ERR

        return stat, recv, bits

    def _crc( self, data ):
        "hello"
        self._cflags( 0x05, 0x04 )
        self._sflags( 0x0A, 0x80 )

        for c in data:
            self.register_write( 0x09, c )

        self.register_write( 0x01, 0x03 )

        i = 0xFF
        while True:
            n = self.register_read( 0x05 )
            i -= 1
            if not (( i != 0 ) and not ( n & 0x04 )):
                break

        return [self.register_read( 0x22 ), self.register_read( 0x21 ) ]

    def antenna_on( self, on = True ):
        "hello"
        if on and ~( self.register_read(0x14) & 0x03 ):
            self._sflags( 0x14, 0x03 )
        else:
            self._cflags( 0x14, 0x03 )

    def request( self, mode ):
        "hello"
        self.register_write( 0x0D, 0x07 )
        ( stat, recv, bits ) = self._tocard( 0x0C, [ mode ] )

        if ( stat != self.status.OK ) | ( bits != 0x10 ):
            stat = self.status.ERR

        return stat, bits

    def anticoll( self ):
        "hello"
        ser_chk = 0
        ser = [ 0x93, 0x20 ]

        self.register_write( 0x0D, 0x00 )
        ( stat, recv, bits ) = self._tocard( 0x0C, ser )

        if stat == self.status.OK:
            if len( recv ) == 5:
                for i in range( 4 ):
                    ser_chk = ser_chk ^ recv[ i ]
                if ser_chk != recv[ 4 ]:
                    stat = self.status.ERR
            else:
                stat = self.status.ERR

        return stat, recv

    def select_tag( self, ser ):
        "hello"
        buf = [ 0x93, 0x70 ] + ser[ : 5 ]
        buf += self._crc( buf )
        ( stat, recv, bits ) = self._tocard( 0x0C, buf )
        if ( stat == self.status.OK ) and ( bits == 0x18 ):
            return self.status.OK
        else:
            return self.status.ERR

    def auth( self, mode, addr, sect, ser ):
        "hello"
        return self._tocard(0x0E, [ mode, addr ] + sect + ser[ : 4 ] )[ 0 ]

    def stop_crypto1( self ):
        "hello"
        self._cflags( 0x08, 0x08 )

    def read( self, addr ):
        "hello"
        data = [ 0x30, addr ]
        data += self._crc( data )
        ( stat, recv, _ ) = self._tocard( 0x0C, data )
        return recv if stat == self.status.OK else None

    def write( self, addr, data ):
        "hello"
        buf = [ 0xA0, addr ]
        buf += self._crc( buf )
        ( stat, recv, bits ) = self._tocard( 0x0C, buf )

        if ( stat != self.status.OK ) or (bits != 4) or ((recv[0] & 0x0F) != 0x0A):
            stat = self.status.ERR
        else:
            buf = []
            for i in range( 16 ):
                buf.append( data[ i ] )
            buf += self._crc( buf )
            ( stat, recv, bits ) = self._tocard( 0x0C, buf )
            if ( stat != self.status.OK ) or (bits != 4) or ((recv[0] & 0x0F) != 0x0A):
                stat = self.status.ERR

        return stat
        
    def read_uid( self ):
        ( stat, tag_type ) = self.request( self.cmd.REQIDL )
        if stat != self.status.OK:
            return None
            
        ( stat, raw_uid ) = self.anticoll()
        if stat != self.status.OK:
            return None
            
        return ( raw_uid[ 0 ] << 24 ) + ( raw_uid[ 1 ] << 16 ) + ( raw_uid[ 2 ] << 8 ) + raw_uid[ 3 ]  

    def demo( self ):
        "hello"
        print( "mrfc522 card reader demo" )
        n = 0
        while True:

            ( stat, tag_type ) = self.request( self.cmd.REQIDL )

            if stat == self.status.OK:

                ( stat, raw_uid ) = self.anticoll()

                if stat == self.status.OK:
                    n += 1
                    print( "%d New card detected" % n )
                    print( "  - tag type: 0x%02x" % tag_type)
                    print( "  - uid     : 0x%02x%02x%02x%02x" %
                        (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3]))
                    print()

                    if self.select_tag( raw_uid ) == self.status.OK:

                        key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]

                        if ( self.auth(self.cmd.AUTHENT1A, 8, key, raw_uid)
                            == self.status.OK 
                        ):
                            print( "Address 8 data: %s" % self.read( 8 ) )
                            self.stop_crypto1()
                        else:
                            print( "Authentication error" )
                    else:
                        print( "Failed to select tag" )

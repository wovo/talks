# ===========================================================================
#
# file     : gf_slf3s_1300f.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2023
# license  : MIT license, see license variable in the __init__.py
#
# This file is part of the Godafoss perhiperal interface library.
#
# This file contains the pcd8544 LCD driver class.
#
# ===========================================================================

from micropython import const
import machine
from godafoss.gf_tools import *
from godafoss.gf_time import *
from godafoss.gf_temperature import *


# ===========================================================================

class slf3s_1300f:
    """
    sensirion slf3s_1300f flow sensor
    
    can nack (ENODEV) when polled to fast (500us pause)
   
    """
    
    # =======================================================================    

    class commands:   
        """chip commands"""
    
        # common
        start_measuring_water         = const( 0x3608 )
        start_measuring_isopropyl     = const( 0x3615 )
        stop_measuring                = const( 0x3FF9 )
        read_id_and_serial_1          = const( 0x367C )
        read_id_and_serial_2          = const( 0xE102 )
        measure_thermal_conductivity  = const( 0x3646 )
        
    # =======================================================================    

    def __init__( 
        self, 
        i2c: machine.I2C,
        address: int = 8
    ) -> None:
        self.i2c = i2c
        self.address = address
        self.fluid = self.commands.start_measuring_water
        
        # general call reset and reset time
        # this seems to be required
        self.i2c.writeto( 0x00, bytes( [ 0x06 ] ) )
        sleep_us( 25_000 )
        
        self._reading = False
        
    # =======================================================================    

    def write_command( 
        self, 
        command: int
    ) -> None:
        """
        write a 16-bit command
        """
        
        self.i2c.writeto(
            self.address,
            bytes( ( ( command >> 8 ) & 0xFF, command & 0xFF ) )
        )
        
    # =======================================================================    

    def read_data( 
        self,
        n: int 
    ):
        return self.i2c.readfrom( self.address, n )
    
    # =======================================================================    

    def start_reading(
        self,
        fluid: int = None
    ):
        if fluid is not None:
            self.fluid = fluid
        self.write_command( self.fluid )
        sleep_us( 15_000 )
        self._reading = True
        
    # =======================================================================    

    def stop_reading( self ):
        self.write_command( self.commands.stop_measuring )
        sleep_us( 500 )
        self.reading = False
        
    # =======================================================================
    
    def get_product_id_and_serial_number( self ):
        if self._reading:
            self.stop_reading()
        self.write_command( self.commands.read_id_and_serial_1 )
        self.write_command( self.commands.read_id_and_serial_2 )
        return self.read_data( 18 )    
    
    # =======================================================================
    
    def get_flow_data(
        self,
        n_bytes: int
    ):
        if not self._reading:
            self.start_reading()
        return self.read_data( n_bytes )    

    # =======================================================================    

    def get_flow( self ):
        d = self.get_flow_data( 3 )
        return int_from_bytes(
            ( d[ 1 ], d[ 0 ] ),
            signed = True
        )
    
    # =======================================================================    

    def get_temperature( self ):
        d = self.get_flow_data( 6 )
        return temperature(
            int_from_bytes(
                ( d[ 4 ], d[ 3 ] ),
                signed = True
            ) / 200.0,
            temperature.scale.celcius
        )
    
    # =======================================================================    

    def get_flags( self ):
        d = self.get_flow_data( 9 )
        return int_from_bytes( ( d[ 8 ], d[ 7 ] ) )
    
    # =======================================================================
    
    def get_product_id( self ):
        d = self.get_product_id_and_serial_number()
        return int_from_bytes( ( 
            d[ 4 ], d[ 3 ], 
            d[ 1 ], d[ 0 ] 
        ) )
    
    # =======================================================================
    
    def get_serial_number( self ):
        d = self.get_product_id_and_serial_number()
        return int_from_bytes( ( 
            d[ 16 ], d[ 15 ], 
            d[ 13 ], d[ 12 ],
            d[ 10 ], d[ 9 ], 
            d[ 7 ], d[ 6 ]             
        ) )
    
    # =======================================================================
    
    def demo(
        self,
        fluid: int = None
    ):
        print( "Sensirion SLF3S_1300F demo" )
        print( "product id 0x%08X" % self.get_product_id() )
        print( "serial number %d" % self.get_serial_number() )
        
        cumulative = 0
        n = 0
        last = ticks_us()
        while True:
            n += 1
            now = ticks_us()
            flow = self.get_flow()
            cumulative += flow * ( now - last ) / 1_000_000.0
            last = now
            sleep_us( 1_000 )
            temp = self.get_temperature()
            print( "[%04d] flow %5d;  cumulative %f ml;  temp %s" %
                ( n, flow, cumulative / ( 500.0 * 60.0 ), temp ) )
            sleep_us( 1_000_000 )
        
         
# ===========================================================================

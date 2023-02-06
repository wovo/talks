import godafoss as gf
import machine, os
from machine import Pin

uname = os.uname()

if uname.sysname == "rp2":
    
    v = gf.gpio_adc( 28 ).read().scaled( 0, 65535 )
    print( v )
    
    # 10k, 10k
    if gf.within( v, 31000, 35000 ):

        print( "system is original RP2040 rp2 or rp2w" )
        p0 =  18
        p1 =  19 
        p2 =  16
        p3 =  17
        p4 =  26
        p5 =  27
        p6 =  13
        p7 =  12
        
    # 10k, 15k        
    elif gf.within( v, 26000, 26400 ): 

        print( "system is 01Space RP2040-0.42 OLED" )
        p0 =  20
        p1 =  24
        p2 =  25
        p3 =  26
        p4 =  5
        p5 =  6
        p6 =  4
        p7 =  3
        
        # p6 =  23
        # p7 =  22

    else:
        print( "rp2 unrecognized adc( 28 ) = ", v )
    
elif ( uname[ 0 ] == "esp32" ) and ( uname[ 4 ] == "ESP32C3 module with ESP32C3" ):
    
    v = gf.gpio_adc( 0 ).read().scaled( 0, 65535 )
    print( v )
    
    # 10k, 15k
    # ADC doesn't seem to work??
    if True:
    # if gf.within( v, 26000, 26400 ):    
    
        print( "system is 01Space ESP32-C3-0.42 OLED" )
        p0 =   3
        p1 =   4
        p2 =   5
        p3 =   6
        p4 =   7
        p5 =   8
        p6 =  10
        p7 =   1
        
        p6 =  6
        p7 =  5
        
    else:
        print( "esp32c3 unrecognized adc( 0 ) = ", v )        
    
elif ( uname[ 0 ] == "esp32" ) and ( uname[ 4 ] == "LOLIN_C3_MINI with ESP32-C3FH4" ):
    
    v = gf.gpio_adc( 0 ).read().scaled( 65535 )
    print( v )
    
    # 10k, 15k        
    if gf.within( v, 26000, 26400 ): 

        print( "system is 01Space ESP32C3-0.42 OLED" )
        p0 =   0
        p1 =   1
        p2 =   2
        p3 =   3
        p4 =   4
        p5 =   5
        p6 =   8
        p7 =   6
    
elif uname[ 0 ] == "esp32":
    # generic ESP32
    # differentiate according to the resistor divide on analog input 0
    
    v = gf.gpio_adc( 0 ).read()
    
    # 1k / 10 k -> 1/11 or around 9 of 100
    if ( v > 5 ) and ( v < 15 ):
        print( "system is ESP32- TTGO T-DISPLAY with 240x135 color LCD" )

        p0 =  21
        p1 =  22
        p2 =  17
        p3 =  2
        p4 =  15
        p5 =  13
        p6 =  12
        p7 =  27
        
        # lcd = 

    else:    
        print( "system is a generic ESP32" )
    
        p0 =  14
        p1 =  13
        p2 =  12
        p3 =  15
        p4 =  33
        p5 =  21
        p6 =  18
        p7 =  19
    
elif uname[ 0 ] == "esp8266":
    # generic ESP8266
    p0 =   3
    p1 =   3
    p2 =   3
    p3 =   3
    p4 =   3
    p5 =   3
    p6 =   1
    p7 =   2
    
elif uname[ 0 ] == "mimxrt":
    
    print( "system is a Teensy 4.1" )
    p0 =   27
    p1 =   26
    p2 =   1
    p3 =   17
    p4 =   18
    p5 =   19
    p6 =   20
    p7 =   21
    
    def hard_spi( n = 0, f = 1_000_000 ):
        return machine.SPI( n, f )
    
else:
    print( "unknown target", uname )

# spi
spi_sck = p0
spi_mosi = p1
spi_miso = p2

# lcd
chip_select = p3
data_command = p4
reset = p5
backlight = p6

# i2c
i2c_scl = p6
i2c_sda = p7

# neopixels
neopixel_data = p5

def port():
    return gf.port_out( p0, p1, p2, p3, p4, p5, p6, p7 )

def soft_spi():
    return machine.SoftSPI( 
        baudrate=10_000_000,
        polarity=1,
        phase=1,
        sck = machine.Pin( spi_sck, machine.Pin.OUT ),
        mosi = machine.Pin( spi_mosi, machine.Pin.OUT ),
        miso = machine.Pin( spi_miso, machine.Pin.IN )
    )
    
def xhard_spi():
    return machine.SPI( 
        baudrate=4000000,
        polarity=1,
        phase=1,
        sck = spi_sck,
        mosi = spi_mosi,
        miso = spi_miso
    )

def soft_i2c():
    return machine.SoftI2C(
        scl = machine.Pin( i2c_scl, machine.Pin.OUT ),
        sda = machine.Pin( i2c_sda, machine.Pin.OUT )
    )
    
def hard_i2c():
    return machine.SoftI2C( 
        scl = machine.Pin( i2c_scl, machine.Pin.OUT ),
        sda = machine.Pin( i2c_sda, machine.Pin.OUT )
    )                            

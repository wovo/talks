# ===========================================================================
#
# demos
#
# ===========================================================================

def timing():
    print_timing( lambda: onboard_led.write( 1 ), n = 1, msg = "write gpo" )
    onboard_led_inverted = onboard_led.inverted()
    print_timing( lambda: onboard_led_inverted.write( 1 ), n = 1, msg = "write gpo inverted" )
    onboard_led_inverted_twice = onboard_led.inverted().inverted()
    print_timing( lambda: onboard_led_inverted_twice.write( 1 ), n = 1, msg = "write gpo inverted twice" )
    
    print_timing( lambda: time.sleep_us( 1 ), n = 1, msg = "1 us wait" )
    print_timing( lambda: time.sleep_us( 10 ), n = 1, msg = "10 us wait" )
    print_timing( lambda: time.sleep_us( 100 ), n = 1, msg = "100 us wait" )
    
    green_leds = port_out( [ 
        gpio_out( p ) for p in [ 0, 1, 4, 5, 10, 11, 14, 15] ] )
    print_timing( lambda: green_leds.write( 12 ), n = 1, msg = "write 8 pin port" )    
    green_leds_inverted  = green_leds.inverted()
    print_timing( lambda: green_leds_inverted.write( 12 ), n = 1, msg = "write 8 pin port inverted" )    
    
    neo_1 = neopixels( gpio_out( 7 ), 1 )
    neo_8 = neopixels( gpio_out( 7 ), 8 )
    neo_64 = neopixels( gpio_out( 7 ), 64 )
    print_timing( lambda: neo_1.flush(), n = 1, msg = "write 1 neopixel" )
    print_timing( lambda: neo_8.flush(), n = 1, msg = "write 8 neopixels" )
    print_timing( lambda: neo_64.flush(), n = 1, msg = "write 64 neopixels" )
    
    i2c_bus = machine.SoftI2C( scl = machine.Pin( 27 ), sda = machine.Pin( 26 ) )
    pcf = pcf8574( i2c_bus, 7 )
    print_timing( lambda: pcf.write( 99 ), n = 1, msg = "pcf8574 write port" )
    pcf2 = pcf.selection( [ 3, 2, 1, 0, 7, 6, 5, 4 ] )
    print_timing( lambda: pcf.write( 99 ), n = 1, msg = "pcf8574 rearranged write port" )
    def pcf_write_pins():
        for pin in pcf:
            pin.write( 1 )
    print_timing( pcf_write_pins, n = 1, msg = "pcf8574 write 8 pins" )
    
def pico():    
    
    green_leds = port_out( [ 
        gpio_out( p ) for p in [ 0, 1, 4, 5, 10, 11, 14, 15] ] )
    neo_8 = neopixels( gpio_out( 7 ), 8 )
    neo_ring = neopixels( gpio_out( 6 ), 24 )
    i2c_bus = machine.SoftI2C( scl = machine.Pin( 27 ), sda = machine.Pin( 26 ) )
        
    # print_info()
    timing()
    
    # onboard_led.demo()
    # blink( - onboard_led, 100_000, 900_000, 3 )
    
    # green_leds.demo()
    
    # sr04( gpio_out( 13 ), gpio_in( 12 ) ).demo()
    
    # servo( gpio_out( 8 ) ).demo()
    
    # neo_8.demo()
    # blink( neo_8[ 0 ].as_pin( color.green // 100 ) )
    
    # walk( neo_ring.as_port( color.red, color.blue / 100 ), 10_000 )
    
    # mrfc522( sck = 18, mosi = 19, miso = 16, rst = 21, cs = 22 ).demo()
    
    # pcf8574( i2c_bus, 7 ).demo()
    # (-pcf8574( i2c_bus, 7 ).selection( [ 3, 2, 1, 0, 7, 6, 5, 4 ] )).demo()
    
    # ssd1306_i2c( xy( 128, 64 ), i2c_bus, 0x3c ).demo()
    
    # ssd1306_i2c( xy( 64, 32 ), i2c_bus, 0x3c ).demo()
    
    # mrfc522( sck=19, mosi=18, miso=17, rst=16, cs=20 ).demo()
    # blink( neo8[ 0 ].as_pin( color.green // 100 ) )

#i2c_bus = machine.SoftI2C( scl = machine.Pin( 27 ), sda = machine.Pin( 26 ) )
#t = hd44780_pcf8547( xy( 20, 4 ), i2c_bus, address = 7 )
#t.demo()

#tcs3472( i2c_bus ).demo()
    
#(-pcf8574( i2c_bus, 7 ).selection( [ 3, 2, 1, 0, 7, 6, 5, 4 ] )).demo()



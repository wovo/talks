# ===========================================================================
#
# file     : gf_modules.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2023
# license  : MIT license, see license variable in the code
#
# This file is part of the Godafoss perhiperal interface library.
#
# ===========================================================================
#
# This is the list of modules that is loaded by the __init__.py.
# Each line that is not empty or a comment contains the name of a module,
# function or class.
#
# Names prefixed by * are modules, loaded by exec'ing a
# "from godafoss.<name> import *" line.
#
# Names prefixed with a + are files that contain a single
# class or functions of the same name.
# They are imported by a trampoline function.
#
# Names prefixed with a = are files that contains multiple
# classes or functions. The indented names following such a line
# are each imported by a trampoline function.
#
# The aim of this rather elaborate loading mechanism is to:
#
# - divide the code in to separate files, which makes for a 
#   cleaner organization and less update time during development
#   of the library
#
# - limit the loading time and RAM footprint by loading only
#   the required files
#
# This file is also used by the tests and documentation generation.
# For this purpose files that are part of godafoss, but are not
# loaded by the __init__,py, are mentioned with a = prefix.
#
# ===========================================================================

modules = ""


# ===========================================================================
#
# basics and tooling
#
# ===========================================================================

modules += """
= intro
= modules
= typing
= native
= gc
= print_info

# should be called embedded as contrast to native?
# import problem on native
# = gc
# * print_info 
* time 
* tools
* invertible
* report
"""


# ===========================================================================
#
# abstract data types
#
# ===========================================================================

modules += """
* xy
* xyz
* color
* fraction
* temperature
"""


# ===========================================================================
#
# abstract peripheral interfaces
#
# ===========================================================================

modules += """
* adc
* dac
* spi
"""


# ===========================================================================
#
# pins & ports
#
# ===========================================================================

modules += """
# cleanup starts from here
* pins
= gpio
+ gpio_adc
= make_pins
    make_pin_out
    make_pin_in
    make_pin_in_out
    make_pin_oc
"""

modules += """
* ports
= port_buffers
= pin_port_demos
    show
    blink
    walk
    kitt
"""


# ===========================================================================
#
# graphics
#
# ===========================================================================

modules += """
* canvas
= canvas_add
= canvas_extended
= canvas_folded
= canvas_inverted
= canvas_part
= canvas_rotated
= canvas_transformed

+ canvas_demo_lines
+ canvas_demo_rectangles
+ canvas_demo_circles
+ canvas_demo_text
+ canvas_demo_scrolling_text
+ canvas_demo_colors
+ canvas_demo_color_gradients
+ canvas_demo_ggf_photos
+ canvas_demo

* shape
* glyph

+ font
= font_default

+ line
+ rectangle
+ circle
+ text
+ ggf
+ image

+ moving_text
+ terminal
"""


# ===========================================================================
#
# digits and characters
#
# ===========================================================================

modules += """
= digits
= digits_demos
"""


# ===========================================================================
#
# neopixels
#
# ===========================================================================

modules += """
= neopixels
    ws281x
    apa102
+ ws2801    
"""

    
# ===========================================================================
#
# I/O extenders
#
# ===========================================================================

modules += """
+ pcf8575
= pcf8574x 
    pcf8574
    pcf8574a
"""

    
# ===========================================================================
#
# LED matrices
#
# ===========================================================================

modules += """
= tm16xx   
+ tm1637   
+ tm1638   
+ tm1640   
+ max7219
+ hub75
"""


# ===========================================================================
#
# LCD & oled
#
# ===========================================================================

modules += """
= lcd_reset_backlight_power
= lcd_spi
"""

modules += """
+ hd44780
= hd44780_pcf8574x 
    hd44780_pcf8574
    hd44780_pcf8574a
+ pcd8544
= ssd1306 
    ssd1306_i2c
    ssd1306_spi
= ssd1309 
    ssd1309_i2c
    ssd1309_spi
+ st7567         
"""

modules += """
+ lcd
= lcd_driver_st7735
= lcd_driver_st7785
= lcd_driver_st7789
= lcd_driver_ili9341
"""

# ===========================================================================
#
# touch ADC
#
# ===========================================================================

modules += """
= touch
+ xpt2046
+ ft6236
"""

    
# ===========================================================================
#
# misc. external things
#
# ===========================================================================

modules += """
+ servo
+ sr04
+ tcs3472
+ sx127x
"""
  
  
# ===========================================================================
#
# boards
#
# ===========================================================================

modules += """
+ board
= board_01space_esp32_c3_042lcd 
= board_01space_rp2040_042lcd
= board_lilygo_ttgo_t_display
= board_lilygo_ttgo_t_watch_2020
= board_lilygo_ttgo_t_wristband
= board_sunton_esp32_2432s028
= board_waveshare_rp2040_lcd_096
"""


# ===========================================================================
#
# under development
#
# ===========================================================================

modules += """
+ mrfc522 
+ slf3s_1300f
= hub75
"""


# ===========================================================================
#
# proprietary
#
# ===========================================================================

modules += """
+ edge 
"""

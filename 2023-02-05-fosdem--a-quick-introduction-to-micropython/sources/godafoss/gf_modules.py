# ===========================================================================
#
# file     : _gf_modules.py
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
= modules
* time 
* tools
* invertible
* benchmark
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
"""


# ===========================================================================
#
# pins & ports
#
# ===========================================================================

modules += """
# cleanup starts from here
* pins
* gpio
+ gpio_adc
* make_pins
"""

modules += """
* ports
* port_buffers
* pin_port_demos
"""


# ===========================================================================
#
# graphics and characters
#
# ===========================================================================

modules += """
* digits
# display
* canvas
#drawable
#terminal
#sheet
"""

modules += """
* line
+ rectangle
+ circle
* text
+ moving_text
+ ggf
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
# Led matrices
#
# ===========================================================================

modules += """
+ tm1637   
+ tm1638   
+ tm1640   
+ max7219
"""


# ===========================================================================
#
# LCD & oled
#
# ===========================================================================

modules += """
+ hd44780
= hd44780_pcf8574x 
    hd44780_pcf8574
    hd44780_pcf8574a
+ pcd8544
= ssd1306 
    ssd1306_i2c
    ssd1306_spi
+ st7735    
+ st7789       
+ st7789_monochrome       
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
"""
    
# ===========================================================================
#
# under development
#
# ===========================================================================

modules += """
+ mrfc522 
"""

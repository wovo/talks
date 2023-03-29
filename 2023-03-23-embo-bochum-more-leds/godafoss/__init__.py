# ===========================================================================
#
# file     : __init__.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2023
# license  : MIT license, see license variable in the code
#
# This file is part of the Godafoss perhiperal interface library.
#
# ===========================================================================
#
# This is the root file of the library.
# The core parts of the library are imported directly.
# Others parts are imported on-demand by trampoline functions,
# to limit loading time and RAM footprint.
# gf_modules.py specifies which parts are loaded and how.
#
# ===========================================================================

"""
NOTES & TODO

hub75 shifts 3 pixels when using bytes???
check with simulator, re-read documentation
use asyncio for servo
use rp2040 for servo
rp2040 pio management

ggf color problem is byte order for 24 bit color

hub75 color depth
snakie is still color inversed (at least on hub75)

hub75 cleanup
hub75 board

snake logo 64 * 64 color
cat in color
hub75 write logo speedup
pre-packed hub75
ggf must produce in-lineable images (only import godafoss, from x import y )
rp2040 vga/hdmi generation
https://learn.pimoroni.com/article/getting-started-with-interstate-75 graph lib

pyMCU v1.11 on 2020-11-26; VCC-GND(R)pyboard412-12m with STM32F412RE
pyboard v1.1 stm32f405rg, ik heb sytm32f412
memfree 204944, but free flash space only 40k
use with flash card; direct edit possible!
comes with pyMCU, put a decent uPython on it?

pico/rp2040 support file -> use in LCD
- reserve/release interrupt, dma, pio

lcd monochrome pio pin-independent

class trampoline via superclass?

spiram https://www.esp32.com/viewtopic.php?t=5450

https://github.com/lemariva/micropython-camera-driver
https://lemariva.com/blog/2020/06/micropython-support-cameras-m5camera-esp32-cam-etc

https://www.espressif.com/en/products/modules
https://vanhunteradams.com/Pico/VGA/VGA.html

lcd drivers handle colors & inversion
gf.spi afmaken, gebruik het overal
i2c like spi

lcd.backlight should be a pin, not a method?

lessons from 'efficient' for monochrome flush

camera:
https://lemariva.com/blog/2020/06/micropython-support-cameras-m5camera-esp32-cam-etc

lcd margin -> offset everywhere
esp32 link to python page modules page

test canvas features, make separate (static) demo

is edge just another board??

make color from internet color value

https://www.lilygo.cc/products/pauls-3d-things-open-smartwatch
https://github.com/minyiky/lvgl_esp32_gc9a01/blob/main/gc9a01.py
https://forum.lvgl.io/t/gc9a01-driver-for-esp32/5600
https://www.waveshare.com/wiki/1.28inch_LCD_Module
https://open-smartwatch.github.io/watches/light-edition/

add sx127x driver
add lora board
https://lemariva.com/blog/2018/10/micropython-esp32-sending-data-using-lora
https://github.com/lemariva/uPyLoRaWAN/blob/LoRaWAN/sx127x.py

lilygo-ttgo-t-camera-mini-esp32
TTGO_Camera_Mini

print something larger by 2 * ??

pine64 risc v

the small and large st7789 are different....
st7789 128x128 doesn't work?
monochrome lookup could be in flash only??

demo colors letters are NOT in inverse color??
python now very weird colors - now OK??

ggf reverses red/green??
esp32_2432s028 LCD is very sloooow (due to monochrome)

t-watch-2020 afmaken
t-wristband afmaken

board demo comment headers
board i2c speed parameter

PCF8563 and RTC abstraction

https://github.com/Sensirion/sensirion-i2c-rs/blob/master/src/crc8.rs polynominal
check @Property decorator
https://github.com/Sensirion/python-i2c-sf06-lf has some style check info

slf3s_1300f
t-display (esp32) hard spi werkt niet? - niet boven 1 MHz??
st7567 werkt niet lang goed!
sd1309 cleanup needed, merge with sd1306?
betere demo voor kleine displays, bv 8x8 en 8x16, alleen lines en bouncing en G?
does a display initially clear and flush??
copy bouncing boxes demo from ssd1309

st7735 80 160 lijkt nergens op
st7735 f demo colors not quite right yet
must have a 1:1 python picture....

kleinere st7789 is verkeerde kleur volgorde en gespiegeld
st7789 128x128 voorbeelden

single pin from buffer (pcf8575) doesn't exist?

ili9341 mirror & rotate
bw & color in same file or class?

pca9685 servo drivers, 'wave' demo
https://github.com/russhughes/gc9a01_mpy - has jpeg decoder

build esp32, pass spiram parameter
automate downloading?
check files in attic/meuk, might be more recent
arg pause + iterations for all demos, add type hints
demos should pass *args **kwargs

original pyboard (STM32F411) only 47k flashs free 39k RAM
but .... flash keeps being visible as USB mass storage!

try arduino 33 ble

make/build make/load <esp32> <rp2040>
add pyboard
github talk
zigzag canvas has to be merged!
https://arduinojson.org/v6/how-to/use-external-ram-on-esp32/

st8879 initialiseert 1e keer niet
digits still takes 5k, factor demo out? formatting? demand loaded!

talks:
- verbose writing style
- compilation takes temporay RAM depending on file size (?) -> split
- also because transfer takes time
- not all parts are needed -> trampolines (46 bytes?)
- pre-compile speeds up loading
- freezing frees up RAM (run from flash)
- spi-ram is SLOOOW
- I2C is slow (contrast SD1306)
- hardware SPI can be much faster than software SPI (and I2C)
- use a fast & large RAM target for development (teensy 4.1)
- watch out where the latest version of your code is!

- use powered hub for eg. displays, or watch current consumption

- wish list: const for class objects

- effect of @native??

- thonny: I can't get used to upload/download direction

for the compiled version, automatically disable logging
big RAM eaters: pins, ports, canvas port_buffers
pin_port_demos: why loaded at all?
should xy be allowed with floats?
https://github.com/Xinyuan-LilyGO/
    TTGO_TWatch_Library/blob/master/docs/watch_2020_v3.md
https://github.com/d03n3rfr1tz3/TTGO.T-Watch.2020
https://gitlab.com/mooond/t-watch2020-esp32-with-micropython
https://github.com/uraich/twatch-2020-micropython
whats up with ft6236 include?
touch macro text for the touch chips
1e module load has negative RAM use -> not on teensy
support i2c register read/write via i2c base class, avoid mavhine.I2C
heatmap gray -> color
b/w formaat met bv 256 grijstinten, bv voor camera beeld??
pcf8593 as in the watch, abstract date/time

photos klopt nog niet helemaal
always-loaded kan best nog wat minder

ESP32-4827S043 download link:http://www.jczn1688.com/zlxz
Downloaden wachtwoord: jczn1688

https://github.com/peterhinch/micropython-nano-gui
https://github.com/peterhinch/micropython-micro-gui
https://github.com/rdagger/
    micropython-ili9341/blob/master/ili9341.py - draw polygon
https://github.com/adafruit/Adafruit_CircuitPython_Bundle
https://www.webucator.com/article/python-color-constants-module/
type hints for alternatives: |
do the same for the documentation
print demo text only when itertations is not None?

gebruik framebuffer direct voor line, rectangle, ellipse, text?
st8879 0x51 brightness
st8879 color invert p300
abstracte servo, pcf, bb servo
Godafoss Graphics Format
https://docs.openmv.io/library/omv.lcd.html - also check for choices
hoe de parameter type aan te geven, (), of niets?
verwijder: addable
spi class that can be re-speeded? (maybe always before use??)
no () for return types because that is a tuple
st77xx: flush, pixel_write, _encode, commands
touch chip edit
benchmark edit
rectangle often draws not complete?
lcd spi parammeters macro
time de flush st7735
idem met HW spi
default LED matrices moet gedimd
better canvas test for small (8 high etc)
dim neopixels by default?
create files-list for documentation from the lists in here
add more complex examples  to the Use section:
    blink, sr04/servo, sheet scrolling text, color graphics
https://github.com/01Space document targets
pcd8544 type for eg make_pin_out( x )
all types () should be references
continue html documentation from: lcd_spi
(lot of files not yet included!)
double empty line before or after the # =========== ?
pcd8544 shows doc inheritance??
- should eg lcd_spi be visible??
terminal itself is not buffered, but sheet below it might be -> offer flush?

commands don't make sense outside the driver, so _commands?
of een raw interface daarvoor? (commands + write command)

gpio should have examples?

doc inheritance
- hidden base class: copy doc verbatim, both class and methods
- public base class: copy only the ref text, with a

text write optimizations could be in glyph?
scrolling text way too slow
b/w images are different from colored ones, don't mix?
    gives problem now with font, color should not be part of it
test images with create-image
sr04 often gives 'no start'
should pin both be +, and & | for combining pin_pin?
port must support similar operations
canvas modifiers? invert, part, fold?
neopixels -> ws2812
neopixels & ws2801: generalize the order
pin & pin should be pin + pin ? same as graphics
"""

from micropython import const

# ===========================================================================
#
# Load the core parts of the library and create the trampolines
# for the on-demand loaded optional parts.
#
# ===========================================================================

# Set to True for for debugging and getting resource statistics
_show_loading = const( True )

# Idem, but also for the on-demand parts (works only on large-RAM targets)
_load_all = const( False )

import godafoss.gf_modules

if _show_loading:
    def _mem_free():
        import godafoss.gf_gc
        godafoss.gf_gc.collect()
        return godafoss.gf_gc.mem_free()

    def _elapsed_ms():
        import godafoss.gf_time
        return godafoss.gf_time.ticks_us() // 1_000

    print( "module               ram     total      ms   total" )
    _mem_before_all = _mem_free()
    _time_before_all = _elapsed_ms()
    _n_trampolines = 0

    def _show_loading_line( item: str ):
        _mem_after = _mem_free()
        _time_after = _elapsed_ms()
        print(
           "%-18s %5d    %6d    %5d   %5d" % (
           item,
           _mem_before - _mem_after, _mem_before_all - _mem_after,
           _time_after - _time_before, _time_after - _time_before_all ) )

# ===========================================================================
#
# always-loaded part: import
#
# ===========================================================================

for _line in godafoss.gf_modules.modules.split( "\n" ):

    if _line.strip() == "":
        pass

    elif _line[ 0 ] == "*" or ( _load_all and _line[ 0 ] in ( '+', '=' ) ):

        _module = _line[ 1 : ].strip()

        if _show_loading:
            _mem_before = _mem_free()
            _time_before = _elapsed_ms()

        exec( "from godafoss.gf_%s import *" % _module )

        if _show_loading:
            _show_loading_line( _module )

    elif _line[ 0 ] in [ '+', ' ', '=', '#' ]:
        pass

    else:
        raise ValueError( _line )

# ===========================================================================
#
# on-demand loaded part: create the trampoline function that
# on-demand load a module and return an object created by
# the function or class constructor in that module.
#
# ===========================================================================

if _show_loading:
    _mem_before = _mem_free()
    _time_before = _elapsed_ms()

for _line in godafoss.gf_modules.modules.split( "\n" ):

    if(
        _load_all
        or ( _line.strip() == "" )
        or ( _line[ 0 ] in [ '#', '*' ] )
    ):
        pass

    elif _line[ 0 ] in [ '+', ' ' ]:

        if _line[ 0 ] == '+':
            _module = _line[ 1 : ].strip()
        _line = _line[ 1 : ].strip()

        exec( """def $f( *args, **kwargs ):
                import godafoss.gf_$m
                return gf_$m.$f( *args, **kwargs )
        """.replace ( "$m", _module ).replace( "$f", _line ) )
        if _show_loading:
            _n_trampolines += 1

    elif _line[ 0 ] in [ '=' ]:
        _module = _line[ 1 : ].strip()

    else:
        raise ValueError( _line )

if _show_loading:

    _show_loading_line( "%d trampolines" % _n_trampolines )

    print(
        "initial free %d; after loading %d; using %d" %
        ( _mem_before_all, _mem_free(), _mem_before_all - _mem_free()  ) )

    del _mem_free, _elapsed_ms
    del _mem_before_all, _time_before_all
    del _mem_before, _time_before
    del _n_trampolines

del _line, _module


# ===========================================================================
#
# mandatory MIT license text
#
# ===========================================================================

license = """
Copyright 2023 Wouter van Ooijen (wouter@voti.nl) - emBO++
 
Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without
limitation the rights to use, copy, modify, merge, publish, distribute,
sublicense, and/or sell copies of the Software, and to permit persons to
whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE
OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""


# ===========================================================================

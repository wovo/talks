# ===========================================================================
#
# file     : gf_time.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2023
# license  : MIT license, see license variable in the __init__.py
#
# This file is part of the Godafoss perhiperal interface library.
#
# ===========================================================================
#
# This file exists to make it possible to mock the MicroPython
# timing functions in the test suite, and to limit the use
# of timing functions within Godafoss to the microseconds-based ones.
#
# ===========================================================================

from time import ticks_us
from time import sleep_us

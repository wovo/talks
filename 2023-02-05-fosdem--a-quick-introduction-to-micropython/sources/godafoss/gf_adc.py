# ===========================================================================
#
# file     : gf_adc.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2023
# license  : MIT license, see license variable in the __init__.py
#
# This file is part of the Godafoss perhiperal interface library.
#
# ===========================================================================
#
# This file contains the (abstract) adc class.
#
# ===========================================================================

from godafoss.gf_tools import *
from godafoss.gf_invertible import *
from godafoss.gf_fraction import *


# ===========================================================================

class adc( invertible ):
    """
    analog input pin

    An adc reads the voltage level on the pin
    as a fraction of the full scale.

    $macro_insert invertible

    examples::
    $insert_example( "test_adc.py", "adc examples", 1 )
    """

    # =======================================================================

    def __init__( self ) -> None:
        invertible.__init__( self )

    # =======================================================================

    def read( self ) -> fraction:
        """
        the adc value as a fraction

        :result: :class:~`godafoss.fraction`
            adc value as a fraction of the full scale
        """
        raise NotImplementedError

    # =======================================================================

    def inverted( self ) -> "adc":
        """
        adc that retruns negative (complement) of the value

        :result: :class:~`godafoss.adc`
            adc that, when read, reads the complement of what the
            original adc would read

        This function returns an adc that reads the complement
        of what the original adc would have read.
        When the original adc would for example read 10/1023,
        the inverted adc reads 1013/1023.
        """

        return _adc_inverted( self )

    # =======================================================================


# ===========================================================================

class _adc_inverted( adc ):
    """proxy that inverts an adc"""

    # =======================================================================

    def __init__(
        self,
        pin: adc
    ):
        self._pin = pin
        adc.__init__( self )

    # =======================================================================

    def read( self ) -> fraction:
        return - self._pin.read()

    # =======================================================================

    def inverted( self ) -> adc:
        return self._pin

    # =======================================================================

# ===========================================================================

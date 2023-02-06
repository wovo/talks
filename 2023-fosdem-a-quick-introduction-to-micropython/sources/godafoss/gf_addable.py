# ===========================================================================
#
# file     : gf_addable.py
# part of  : godafoss micropython library
# url      : https://www.github.com/wovo/godafoss
# author   : Wouter van Ooijen (wouter@voti.nl) 2023
# license  : MIT license, see license variable in the __init__.py
#
# This file is part of the Godafoss perhiperal interface library.
#
# This file contains the (abstract) addable class.
#
# ===========================================================================


# ===========================================================================

class addable:
    """
    object that can be added

    Addable objects can be added by the + operator.
    
    The effect of adding objects is intended to be that certain actions
    on the addition are equivalent to performing the action on each
    consituent.
    
    Concrete addable classes must implement this by applying such
    actions on all objects in the _list member.
    This list defaults to just the object itself.
    
    The result of an addition is the type that was passed to the
    addable constructor. This type must have a constructor that can
    be called without parameters.
    
    examples::
    $insert_example( "test_invertible.py", "invertible examples", 1 )
    """

    def __init__( self, subclass ):
        self._list = [ self ]
        self._subclass = subclass()
        pass
        
    # =======================================================================        

    def __add__( self, other: "addable" ) -> "addable":
        result = self._subclass()
        result._list = self._list + other._list
        return result  

    # =======================================================================        

# ===========================================================================

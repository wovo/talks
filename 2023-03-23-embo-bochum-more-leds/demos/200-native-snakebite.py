from functools import reduce

def plus_one( x, y = [ 1 ] ):
    y.append( x )
    return reduce( lambda a, b: a + b, y )

print( plus_one( 1 ) )


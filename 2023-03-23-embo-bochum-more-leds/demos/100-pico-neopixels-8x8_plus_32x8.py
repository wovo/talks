import godafoss as gf
edge = gf.edge()

p = gf.ws281x( edge.p5, 320 ).folded( 40, zigzag = True ).xy_swapped()
                               
p.clear()                               
p.write( gf.text( "emBO++" ) )
p.flush()
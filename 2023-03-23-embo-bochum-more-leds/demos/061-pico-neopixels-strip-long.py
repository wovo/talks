import godafoss as gf
edge = gf.edge()

# number of pixels:
# rings 8, 16, 24
# strip 56
# matrix 64
# long strip 300

p = gf.ws281x( edge.p5, 300 )
                                
#p.demo_color_wheel( dim = 24 )
gf.canvas_demo_blink(
    p,
    sequence = (
        gf.colors.white // 2,
        gf.colors.black
    )
) 
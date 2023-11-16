import godafoss as gf
edge = gf.edge()

p = gf.ws281x( edge.p5, 300 )
                                
p.demo_color_wheel(
    color_list = (
        gf.colors.red,
        gf.colors.green,
        gf.colors.blue,
    ),    
    dim = 24,
    delay = 1_000,
    iterations = 1,
    blackout = False
)
gf.canvas_demo_blink(
    p,
    sequence = (
        gf.colors.white // 2,
        gf.colors.black
    ),
    pause = 200_000
) 
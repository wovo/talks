import godafoss as gf
edge = gf.edge()

spi = edge.spi( frequency = 20_000_000 )

display = gf.lcd(
    chip = "st7789",      
    size = gf.xy( 240, 320 ),
    spi = spi,
    data_command = edge.data_command,
    chip_select = edge.chip_select,
    reset = edge.reset,
    backlight = edge.backlight,
    color_order = None,
    mirror_x = True,
)

display.demo()
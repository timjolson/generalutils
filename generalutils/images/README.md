# generalutils.images

    hex_to_rgb(hex):
        Convert a hex string to rgb tuple.
        :param hex: string, e.g. '#F0F0F0' or '0xf0f0f0'
        :return: (r, g, b)

    rgb_to_hex(rg):
        Convert an rgb tuple to a hex string.
        :param rgb: (int, int, int), rgb tuple
        :return: string, hex color string, e.g. '#F0F0F0'

    find_color(color):
        Finds a color in colorList by name, rgb, or hex string.
        If a name string is passed, it must match exactly.
        If rgb (int, int, int) tuple is passed, if no exact match, returns closest color
            by tuple_distance between values.
        If hex string passed, if no exact match, converts to rgb and runs with that tuple.
    
        :param color: hex string, color name string, or rgb (int, int, int)
        :return tuple: ( [possible color name strings], hex string, (r,g,b) )
                or `None` in the case of a name string without exact match

    colorList[
        (
            ['color name1', 'color name2', ...],
            'hex color string',
            (red, blue, green)
        ),
        ...
        ]

        ex.
        (['darkgray', 'darkgrey'], '#A9A9A9', (169, 169, 169))

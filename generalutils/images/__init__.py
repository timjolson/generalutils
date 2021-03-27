"""
Color utilities.
Convert hex <-> rgb.
Find a color name, hex, or rgb from any of these.

Functions:
    hex_to_rgb(hex) - hex: string, e.g. '#F0F0F0' or '0xf0f0f0'
    rgb_to_hex(rg) - rgb: (int, int, int)
    find_color(color) - color: hex string, color name string, or rgb (int, int, int)

Lists:
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

"""
from generalutils.math import tuple_distance


colorList = \
[(['aliceblue'], '#F0F8FF', (240, 248, 255)),
 (['antiquewhite'], '#FAEBD7', (250, 235, 215)),
 (['aqua', 'cyan'], '#00FFFF', (0, 255, 255)),
 (['aquamarine'], '#7FFFD4', (127, 255, 212)),
 (['azure'], '#F0FFFF', (240, 255, 255)),
 (['beige'], '#F5F5DC', (245, 245, 220)),
 (['bisque'], '#FFE4C4', (255, 228, 196)),
 (['black'], '#000000', (0, 0, 0)),
 (['blanchedalmond'], '#FFEBCD', (255, 235, 205)),
 (['blue'], '#0000FF', (0, 0, 255)),
 (['blueviolet'], '#8A2BE2', (138, 43, 226)),
 (['brown'], '#A52A2A', (165, 42, 42)),
 (['burlywood'], '#DEB887', (222, 184, 135)),
 (['cadetblue'], '#5F9EA0', (95, 158, 160)),
 (['chartreuse'], '#7FFF00', (127, 255, 0)),
 (['chocolate'], '#D2691E', (210, 105, 30)),
 (['coral'], '#FF7F50', (255, 127, 80)),
 (['cornflowerblue'], '#6495ED', (100, 149, 237)),
 (['cornsilk'], '#FFF8DC', (255, 248, 220)),
 (['crimson'], '#DC143C', (220, 20, 60)),
 (['darkblue'], '#00008B', (0, 0, 139)),
 (['darkcyan'], '#008B8B', (0, 139, 139)),
 (['darkgoldenrod'], '#B8860B', (184, 134, 11)),
 (['darkgray', 'darkgrey'], '#A9A9A9', (169, 169, 169)),
 (['darkgreen'], '#006400', (0, 100, 0)),
 (['darkkhaki'], '#BDB76B', (189, 183, 107)),
 (['darkmagenta'], '#8B008B', (139, 0, 139)),
 (['darkolivegreen'], '#556B2F', (85, 107, 47)),
 (['darkorange'], '#FF8C00', (255, 140, 0)),
 (['darkorchid'], '#9932CC', (153, 50, 204)),
 (['darkred'], '#8B0000', (139, 0, 0)),
 (['darksalmon'], '#E9967A', (233, 150, 122)),
 (['darkseagreen'], '#8FBC8F', (143, 188, 143)),
 (['darkslateblue'], '#483D8B', (72, 61, 139)),
 (['darkslategray', 'darkslategrey'], '#2F4F4F', (47, 79, 79)),
 (['darkturquoise'], '#00CED1', (0, 206, 209)),
 (['darkviolet'], '#9400D3', (148, 0, 211)),
 (['deeppink'], '#FF1493', (255, 20, 147)),
 (['deepskyblue'], '#00BFFF', (0, 191, 255)),
 (['dimgray', 'dimgrey'], '#696969', (105, 105, 105)),
 (['dodgerblue'], '#1E90FF', (30, 144, 255)),
 (['firebrick'], '#B22222', (178, 34, 34)),
 (['floralwhite'], '#FFFAF0', (255, 250, 240)),
 (['forestgreen'], '#228B22', (34, 139, 34)),
 (['gainsboro'], '#DCDCDC', (220, 220, 220)),
 (['ghostwhite'], '#F8F8FF', (248, 248, 255)),
 (['gold'], '#FFD700', (255, 215, 0)),
 (['goldenrod'], '#DAA520', (218, 165, 32)),
 (['gray', 'grey'], '#808080', (128, 128, 128)),
 (['green'], '#008000', (0, 128, 0)),
 (['greenyellow'], '#ADFF2F', (173, 255, 47)),
 (['honeydew'], '#F0FFF0', (240, 255, 240)),
 (['hotpink'], '#FF69B4', (255, 105, 180)),
 (['indianred'], '#CD5C5C', (205, 92, 92)),
 (['indigo'], '#4B0082', (75, 0, 130)),
 (['ivory'], '#FFFFF0', (255, 255, 240)),
 (['khaki'], '#F0E68C', (240, 230, 140)),
 (['lavender'], '#E6E6FA', (230, 230, 250)),
 (['lavenderblush'], '#FFF0F5', (255, 240, 245)),
 (['lawngreen'], '#7CFC00', (124, 252, 0)),
 (['lemonchiffon'], '#FFFACD', (255, 250, 205)),
 (['lightblue'], '#ADD8E6', (173, 216, 230)),
 (['lightcoral'], '#F08080', (240, 128, 128)),
 (['lightcyan'], '#E0FFFF', (224, 255, 255)),
 (['lightgoldenrodyellow'], '#FAFAD2', (250, 250, 210)),
 (['lightgray', 'lightgrey'], '#D3D3D3', (211, 211, 211)),
 (['lightgreen'], '#90EE90', (144, 238, 144)),
 (['lightpink'], '#FFB6C1', (255, 182, 193)),
 (['lightsalmon'], '#FFA07A', (255, 160, 122)),
 (['lightseagreen'], '#20B2AA', (32, 178, 170)),
 (['lightskyblue'], '#87CEFA', (135, 206, 250)),
 (['lightslategray', 'lightslategrey'], '#778899', (119, 136, 153)),
 (['lightsteelblue'], '#B0C4DE', (176, 196, 222)),
 (['lightyellow'], '#FFFFE0', (255, 255, 224)),
 (['lime'], '#00FF00', (0, 255, 0)),
 (['limegreen'], '#32CD32', (50, 205, 50)),
 (['linen'], '#FAF0E6', (250, 240, 230)),
 (['magenta', 'fuchsia'], '#FF00FF', (255, 0, 255)),
 (['maroon'], '#800000', (128, 0, 0)),
 (['mediumaquamarine'], '#66CDAA', (102, 205, 170)),
 (['mediumblue'], '#0000CD', (0, 0, 205)),
 (['mediumorchid'], '#BA55D3', (186, 85, 211)),
 (['mediumpurple'], '#9370DB', (147, 112, 219)),
 (['mediumseagreen'], '#3CB371', (60, 179, 113)),
 (['mediumslateblue'], '#7B68EE', (123, 104, 238)),
 (['mediumspringgreen'], '#00FA9A', (0, 250, 154)),
 (['mediumturquoise'], '#48D1CC', (72, 209, 204)),
 (['mediumvioletred'], '#C71585', (199, 21, 133)),
 (['midnightblue'], '#191970', (25, 25, 112)),
 (['mintcream'], '#F5FFFA', (245, 255, 250)),
 (['mistyrose'], '#FFE4E1', (255, 228, 225)),
 (['moccasin'], '#FFE4B5', (255, 228, 181)),
 (['navajowhite'], '#FFDEAD', (255, 222, 173)),
 (['navy'], '#000080', (0, 0, 128)),
 (['oldlace'], '#FDF5E6', (253, 245, 230)),
 (['olive'], '#808000', (128, 128, 0)),
 (['olivedrab'], '#6B8E23', (107, 142, 35)),
 (['orange'], '#FFA500', (255, 165, 0)),
 (['orangered'], '#FF4500', (255, 69, 0)),
 (['orchid'], '#DA70D6', (218, 112, 214)),
 (['palegoldenrod'], '#EEE8AA', (238, 232, 170)),
 (['palegreen'], '#98FB98', (152, 251, 152)),
 (['paleturquoise'], '#AFEEEE', (175, 238, 238)),
 (['palevioletred'], '#DB7093', (219, 112, 147)),
 (['papayawhip'], '#FFEFD5', (255, 239, 213)),
 (['peachpuff'], '#FFDAB9', (255, 218, 185)),
 (['peru'], '#CD853F', (205, 133, 63)),
 (['pink'], '#FFC0CB', (255, 192, 203)),
 (['plum'], '#DDA0DD', (221, 160, 221)),
 (['powderblue'], '#B0E0E6', (176, 224, 230)),
 (['purple'], '#800080', (128, 0, 128)),
 (['red'], '#FF0000', (255, 0, 0)),
 (['rosybrown'], '#BC8F8F', (188, 143, 143)),
 (['royalblue'], '#4169E1', (65, 105, 225)),
 (['saddlebrown'], '#8B4513', (139, 69, 19)),
 (['salmon'], '#FA8072', (250, 128, 114)),
 (['sandybrown'], '#F4A460', (244, 164, 96)),
 (['seagreen'], '#2E8B57', (46, 139, 87)),
 (['seashell'], '#FFF5EE', (255, 245, 238)),
 (['sienna'], '#A0522D', (160, 82, 45)),
 (['silver'], '#C0C0C0', (192, 192, 192)),
 (['skyblue'], '#87CEEB', (135, 206, 235)),
 (['slateblue'], '#6A5ACD', (106, 90, 205)),
 (['slategray', 'slategrey'], '#708090', (112, 128, 144)),
 (['snow'], '#FFFAFA', (255, 250, 250)),
 (['springgreen'], '#00FF7F', (0, 255, 127)),
 (['steelblue'], '#4682B4', (70, 130, 180)),
 (['tan'], '#D2B48C', (210, 180, 140)),
 (['teal'], '#008080', (0, 128, 128)),
 (['thistle'], '#D8BFD8', (216, 191, 216)),
 (['tomato'], '#FF6347', (255, 99, 71)),
 (['turquoise'], '#40E0D0', (64, 224, 208)),
 (['violet'], '#EE82EE', (238, 130, 238)),
 (['wheat'], '#F5DEB3', (245, 222, 179)),
 (['white'], '#FFFFFF', (255, 255, 255)),
 (['whitesmoke'], '#F5F5F5', (245, 245, 245)),
 (['yellow'], '#FFFF00', (255, 255, 0)),
 (['yellowgreen'], '#9ACD32', (154, 205, 50)),
 (['disabled-gray', 'disabled-grey'], '#F0F0F0', (240, 240, 240))
 ]


def hex_to_rgb(hex):
    """Convert a hex string to rgb tuple.

    :param hex: string, e.g. '#F0F0F0' or '0xf0f0f0'
    :return: (r, g, b)
    """
    hex = hex.split('#')[-1].split('0x')[-1]
    r = int(hex[:2], 16)
    g = int(hex[2:4], 16)
    b = int(hex[4:6], 16)
    return r, g, b


def rgb_to_hex(rgb):
    """Convert an rgb tuple to a hex string.

    :param rgb: (int, int, int), rgb tuple
    :return: string, hex color string, e.g. '#F0F0F0'
    """
    r, g, b = rgb[0], rgb[1], rgb[2]
    r, g, b = hex(r), hex(g), hex(b)
    r, g, b = r.split('0x')[-1].upper(), g.split('0x')[-1].upper(), b.split('0x')[-1].upper()
    if len(r) == 1:
        r = '0' + r
    if len(g) == 1:
        g = '0' + g
    if len(b) == 1:
        b = '0' + b
    return '#'+r+g+b


def find_color(color):
    """Finds a color in colorList by name, rgb, or hex string.
    If a name string is passed, it must match exactly.
    If rgb (int, int, int) tuple is passed, if no exact match, returns closest color
        by tuple_distance between values.
    If hex string passed, if no exact match, converts to rgb and runs with that tuple.

    :param color: hex string, color name string, or rgb (int, int, int)
    :return tuple: ( [possible color name strings], hex string, (r,g,b) )
            or `None` in the case of a name string without exact match
    """
    if isinstance(color, str) and (color.startswith('#') or color.startswith('0x')):
        # handle hex string
        for c in colorList:
            if c[1] == color:
                return c

        # convert to (r,g,b) and try search
        return find_color(hex_to_rgb(color))

    if isinstance(color, str):
        # handle color name string
        for c in colorList:
            for n in c[0]:
                if n.upper() == color.upper():
                    return c[0], c[1].upper(), c[2]

        # no exact match
        return None

    if isinstance(color, tuple) and len(color) == 3 and all([isinstance(c, int) for c in color]):
        for c in colorList:
            if c[2] == color:
                # exact match
                return c[0], c[1].upper(), c[2]

        # do a proximity search
        _min = 1.1e16
        _min_c = ''
        for c in colorList:
            d = tuple_distance(color, c[2])
            if d < _min:
                _min = d
                _min_c = c
        return (_min_c[0], _min_c[1].upper(), _min_c[2]) if _min_c else None

    raise TypeError("color: {} is not the correct format for query".format(color))


def draw_circle(img, center, radius, color, thickness=None):
    """Similar to cv2.circle .
    https://www.geeksforgeeks.org/python-opencv-cv2-circle-method/

    :param img: 2d array on which to draw
    :param center: tuple (x_center, y_center)
    :param radius: int
    :param color: int, value to assign where circle is drawn
    :param thickness: line thickness (beyond radius)
    :return: img with circle drawn
    """
    height, width = img.shape
    xc, yc = center

    xc, yc, radius, thickness = int(xc), int(yc), int(radius), int(thickness) if thickness is not None else 0

    def fill_line(x0, x1, y):
        if 0 <= y < height:
            minx, maxx = max(min(x0,width), 0), min(max(x1,0), width)
            img[y, minx:maxx] = color

    def color_pixel(x, y):
        if 0 <= x < width and 0 <= y < height:
            img[y][x] = color

    thickness = thickness if (thickness is not None and thickness != 0) else 1

    if thickness > 1:
        draw_circle(img, center, radius+thickness, color, -1)
        draw_circle(img, center, radius, 0, -1)
    else:
        dx, dy = radius, 0
        err = 1 - dx

        if thickness == 1:
            while dx >= dy:
                color_pixel(dx + xc, dy + yc)  # 1
                color_pixel(dy + xc, dx + yc)  # 2
                color_pixel(-dy + xc, dx + yc)  # 3
                color_pixel(-dx + xc, dy + yc)  # 4
                color_pixel(-dx + xc, -dy + yc)  # 5
                color_pixel(-dy + xc, -dx + yc)  # 6
                color_pixel(dx + xc, -dy + yc)  # 7
                color_pixel(dy + xc, -dx + yc)  # 8

                dy += 1
                if err < 0:
                    err += 2 * dy + 1
                else:
                    dx -= 1
                    err += 2 * (dy - dx + 1)
        else:
            while dx >= dy:
                fill_line(xc - dx, xc + dx, yc + dy)  # bottom big
                fill_line(xc - dx, xc + dx, yc - dy)  # top big
                fill_line(xc - dy, xc + dy, yc + dx)  # bottom small
                fill_line(xc - dy, xc + dy, yc - dx)  # top small

                dy += 1
                if err < 0:
                    err += 2 * dy + 1
                else:
                    dx -= 1
                    err += 2 * (dy - dx + 1)
    return img


def flatten(base, *layers):
    """Combine `layers` down onto `base`, all 2d arrays. Adds layer values to base where applicable.

    :param base: 2d array of int
    :param layers: sequence of 2d array of int
    :return: base with layer values added
    """
    for mask in layers[::-1]:
        startx, starty = int(mask.x+mask.offset), int(mask.y+mask.offset)
        endy = min(base.shape[0] - starty, mask.shape[0])
        endx = min(base.shape[1] - startx, mask.shape[1])
        # print('{},{}'.format(starty, startx))
        # print('{},{}'.format(endy, endx))

        # for r, row in enumerate(mask):
        #     R = r + starty
        #     # print('r {}'.format(R))
        #     if R>=0 and R<base.shape[0]:
        #         # print('row {}'.format(row))
        #         for c, val in enumerate(row):
        #             C = c + startx
        #             # print('c {}'.format(C))
        #             if C>=0 and C<base.shape[1]:
        #                 # print('val {}'.format(val))
        #                 # print('*** {} {} {}'.format(r+starty, c+startx, base[r+starty][c+startx] +val))
        #                 base[R].__setitem__(C, base[R][C] + val)

        [[base[r+starty].__setitem__(c+startx, base[r+starty][c+startx] + val)
           for c, val in enumerate(row) if c+startx>=0 and c+startx<base.shape[1]]
            for r, row in enumerate(mask) if r+starty>=0 and r+starty<base.shape[0]]

        # [print(row) for row in mask]
        # [[base[r+starty].__setitem__(c+startx, base[r+starty][c+startx]+val) for c, val in enumerate(row)] for r, row in enumerate(mask)]
        # [[[print(item) for item in row] for row in col] for col in mask]

        # for Y in np.arange(0, min(base.shape[0] - starty, mask.shape[0]), 1):
        #     for X in np.arange(0, min(base.shape[1] - startx, mask.shape[1]), 1):
        #         if Y + starty >= 0 and X + startx >= 0:
        #             base[Y + starty][X + startx] += mask[Y][X]

        # for Y in np.arange(0, min(base.shape[0] - starty, mask.shape[0]), 1):
        #     Y += starty
        #     if Y >=0 :
        #         for X in np.arange(0, min(base.shape[1] - startx, mask.shape[1]), 1):
        #             X += startx
        #             if X >= 0:
        #                 base[Y][X] += mask[Y][X]

    return base


__all__ = ['colorList', 'hex_to_rgb', 'rgb_to_hex', 'find_color', 'draw_circle', 'flatten']

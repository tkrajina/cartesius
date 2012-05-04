# -*- coding: utf-8 -*-

""" Utility functions folr colors """

def get_color(color):
    """ Can convert from integer to (r, g, b) """
    if not color:
        return None

    if isinstance(color, int):
        temp = color
        blue = temp % 256

        temp = temp / 256
        green = temp % 256

        temp = temp / 256
        red = temp % 256

        return (red, green, blue)

    if not len(color) == 3:
        raise Exception('Invalid color {0}'.format(color))

    return color

def brighten(color, n):
    return (int((color[0] + n) % 256), int((color[1] + n) % 256), int((color[2] + n) % 256))

def darken(color, n):
    return brighten(color, -n)

def get_color_between(color1, color2, i):
    """ i is a number between 0 and 1, if 0 then color1, if 1 color2, ... """
    if i <= 0:
        return color1
    if i >= 1:
        return color2
    return (int(color1[0] + (color2[0] - color1[0]) * i),
            int(color1[1] + (color2[1] - color1[1]) * i),
            int(color1[2] + (color2[2] - color1[2]) * i))

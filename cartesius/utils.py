# -*- coding: utf-8 -*-

def cartesius_to_image_coord(x, y, bounds):
    assert bounds.is_set()
    assert bounds.image_width
    assert bounds.image_height
    assert x != None
    assert y != None

    x = float(x)
    y = float(y)

    x_ratio = (x - bounds.left) / (bounds.right - bounds.left)
    y_ratio = (y - bounds.bottom) / (bounds.top - bounds.bottom)

    return (x_ratio * bounds.image_width, bounds.image_height - y_ratio * bounds.image_height)

def min_max(*n):
    if not n:
        return None

    min_result = n[0]
    max_result = n[0]
    for i in n:
        if i != None:
            if min_result == None or i < min_result:
                min_result = i
            if max_result == None or i > max_result:
                max_result = i

    return min_result, max_result



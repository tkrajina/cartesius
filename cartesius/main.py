# -*- coding: utf-8 -*-

import logging as mod_logging
import os as mod_os

import Image as mod_image
import ImageDraw as mod_imagedraw
import ImageFont as mod_imagefont

import utils as mod_utils
import colors as mod_colors

# Get the package location:
package_location = mod_utils.__file__[: mod_utils.__file__.rfind('/')]

# use a truetype font included with cartesius:
DEFAULT_FONT_NAME = 'Oxygen-Regular.ttf'
DEFAULT_FONT_LOCATION = package_location + mod_os.sep + 'fonts' + mod_os.sep + DEFAULT_FONT_NAME

DEFAULT_FONT_SIZE = 10

# Default colors for important elements:
DEFAULT_AXES_COLOR = (150, 150, 150)
DEFAULT_LABEL_COLOR = (150, 150, 150)
DEFAULT_POINT_COLOR = (150, 150, 150)
DEFAULT_GRID_COLOR = (235, 235, 235)
DEFAULT_ELEMENT_COLOR = (50, 50, 50)

# Possible label positions:
LEFT_UP       = -1, 1
LEFT_CENTER   = -1, 0
LEFT_DOWN     = -1, -1
CENTER_UP     = 0, 1
CENTER        = 0, 0
CENTER_DOWN   = 0, -1
RIGHT_UP      = 1, 1
RIGHT_CENTER  = 1, 0
RIGHT_DOWN    = 1, -1

class Bounds:
    """
    Bounds for coordinate system and image size. If the user don't explicitly set hiw own bounds, those
    will be resized with each new element.
    """

    image_width = None
    image_height = None

    left = None
    right = None
    bottom = None
    top = None

    def __init__(self, left=None, right=None, bottom=None, top=None, image_width=None, image_height=None):
        self.reset()

        self.left = left
        self.right = right
        self.bottom = bottom
        self.top = top

        if self.bottom != None and self.top != None:
            if not self.bottom < self.top:
                raise Exception('Bottom bound ({0}) greater than top bound ({1})'.format(self.bottom, self.top))
        if self.left != None and self.right != None:
            if not self.left < self.right:
                raise Exception('Left bound ({0}) greater than right bound ({1})'.format(self.left, self.right))

        self.image_width = image_width
        self.image_height = image_height

    def get_width_height(self):
        assert self.left != None
        assert self.right != None
        assert self.bottom != None
        assert self.top != None
        assert self.right > self.left
        assert self.top > self.bottom

        return self.right - self.left, self.top - self.bottom

    def reset(self):
        self.left_bound, self.right_bound, self.lower_bound, self.upper_bound = None, None, None, None

    def update_to_image_size(self):
        assert self.image_width
        assert self.image_height

        width, height = self.get_width_height()

        desired_width_height_ratio = self.image_width / float(self.image_height)

        if desired_width_height_ratio < width / float(height):
            desired_height = width / desired_width_height_ratio
            self.bottom = self.bottom - (desired_height - height) / 2
            self.top = self.top + (desired_height - height) / 2
        else:
            desired_width = height * desired_width_height_ratio
            self.left = self.left - (desired_width - width) / 2
            self.right = self.right + (desired_width - width) / 2

    def update(self, bounds=None, x=None, y=None, point=None):
        if point != None:
            if not len(point) == 2:
                raise Exception('Invalid point: {0}'.format(point))
            x = point[0]
            y = point[1]

        if x != None:
            self.left, self.right = mod_utils.min_max(x, self.left, self.right)
        if y != None:
            self.bottom, self.top = mod_utils.min_max(y, self.bottom, self.top)

        if bounds:
            self.update(x=bounds.left, y=bounds.top)
            self.update(x=bounds.right, y=bounds.bottom)

        if self.bottom != None and self.top != None:
            assert self.bottom <= self.top
        if self.left != None and self.right != None:
            assert self.left <= self.right

    def is_set(self):
        return self.left != None and self.right != None and self.bottom != None and self.top != None

    def __str__(self):
        return '[bounds:{0},{1},{2},{3}, image:{4},{5}]'.format(self.left, self.right, self.bottom, self.top, self.image_width, self.image_height)

class CoordinateSystem:

    elements = None

    bounds = None

    # x axis element:
    x_axis = None

    # y axis element:
    y_axis = None

    resize_bounds = None

    def __init__(self, bounds=None):
        """ If custom bounds are given, they won't be resized according to new elements. """
        import elements as mod_elements
        self.elements = []

        # Set default bounds
        if bounds:
            if isinstance(bounds, Bounds):
                self.bounds = bounds
                self.resize_bounds = False
            else:
                if not len(bounds) == 4:
                    raise Exception('Bounds must be a 4 element tuple/list')
                self.bounds = Bounds(left=bounds[0], right=bounds[1], bottom=bounds[2], top=bounds[3])
                self.resize_bounds = False
        else:
            self.bounds = Bounds()
            self.resize_bounds = True

        # By default, axes are on:
        self.x_axis = mod_elements.Axis(horizontal=True, points=1)
        self.y_axis = mod_elements.Axis(vertical=True, points=1)

    def add(self, element):
        """
        Add element on coordinate system.

        Note that if you add n default axis, it will remove a previous existing horizontal/vertical axis,
        but the same does not apply for detached axes.
        """
        import elements as mod_elements

        if not element or not isinstance(element, CoordinateSystemElement):
            raise Exception('Invalid element: {0}'.format(element))

        if isinstance(element, mod_elements.Axis):
            if element.is_detached():
                self.elements.append(element)
            else:
                if element.is_horizontal():
                    self.x_axis = element
                else:
                    self.y_axis = element
        else:
            element.reload_bounds()
            self.elements.append(element)
            self.reload_bounds()

    def reload_bounds(self):
        if not self.resize_bounds:
            return

        if not self.elements:
            self.bounds.left = -1
            self.bounds.right = 1
            self.bounds.bottom = -1
            self.bounds.top = 1
            return

        for element in self.elements:
            self.bounds.update(element.bounds)

        assert self.bounds

    def __draw_elements(self, image, draw, draw_handler=None, hide_x_axis=False, hide_y_axis=False):
        for element in self.elements:
            draw_handler.update_pil_image_draw(image, draw)
            element.draw(image=image, draw=draw, draw_handler=draw_handler)

        if not hide_x_axis and self.x_axis:
            self.x_axis.draw(image=image, draw=draw, draw_handler=draw_handler)

        if not hide_y_axis and self.y_axis:
            self.y_axis.draw(image=image, draw=draw, draw_handler=draw_handler)

    def draw(self, width, height, axis_units_equal_length=True, hide_x_axis=False, hide_y_axis=False,
            antialiasing=None):
        """ Returns a PIL image """

        # Antialiasing works like this. If it is set, the image will be drawn double the size (that's
        # why antialiasing_coef is 2). Only later it will be resized to one half with PIL's ANTIALIAS
        # flag:
        antialiasing_coef = 1
        if antialiasing:
            antialiasing_coef = 2
            width = int(width * antialiasing_coef)
            height = int(height * antialiasing_coef)

        self.bounds.image_width = width
        self.bounds.image_height = height

        if axis_units_equal_length:
            self.reload_bounds()

        image = mod_image.new('RGBA', (width, height), (255, 255, 255, 255))
        draw = mod_imagedraw.Draw(image)

        draw_handler = PILHandler(antialiasing_coef, self.bounds)

        if self.resize_bounds:
            self.bounds.update_to_image_size()

        self.__draw_elements(image=image, draw=draw, draw_handler=draw_handler, hide_x_axis=hide_x_axis, hide_y_axis=hide_y_axis)

        if antialiasing:
            image = image.resize((int(width / antialiasing_coef), int(height / antialiasing_coef)), mod_image.ANTIALIAS)

        return image

class CoordinateSystemElement:
    """ Abstract class, every subclass should detect bounds and have the code to draw this item """

    bounds = None
    transparency_mask = None

    def __init__(self, transparency_mask=None):
        self.bounds = Bounds()

        self.transparency_mask = transparency_mask if transparency_mask else 255

    def reload_bounds(self):
        """
        Will be called after the element is added to the coordinate system. By default (if the CS
        don't have his own custom bounds, elements should resize the bounds so that all of them
        fits on the image.
        """
        raise Exception('Not implemented in {0}'.format(self.__class__))

    def process_image(self, draw_handler):
        """ Will be called when the image is drawn """
        raise Error('Not implemented in {0}'.format(self.__class__))

    def get_color(self, color):
        """ Do use this method on all colors given in constructors. Possible color values are integers
        (best given as hex 0xRRGGBB) or tuples (RRR, GGG, BB)"""
        return mod_colors.get_color(color)

    def get_color_with_transparency(self, color):
        """ Use this to get color with appropriate transparency taken from this element. """
        if not color:
            return None

        if not len(color) >= 3:
            raise Exception('Invalid color: {0}'.format(color))

        return (color[0], color[1], color[2], self.transparency_mask)

    def draw(self, image, draw, draw_handler):
        """ Draw this element. All custom code must be implemented in process_image() """

        if self.transparency_mask == 255:
            # If no transparency, draw on same PIL draw object:
            tmp_image, tmp_draw = image, draw
        else:
            # If transparency, draw on new PIL's draw object:
            tmp_image = mod_image.new('RGBA', (draw_handler.bounds.image_width, draw_handler.bounds.image_height))
            tmp_draw = mod_imagedraw.Draw(tmp_image)

        draw_handler.update_pil_image_draw(tmp_image, tmp_draw)

        self.process_image(draw_handler)

        if tmp_image != image or tmp_draw != draw:
            # Transparency => paste this PIL's image over the old one:
            image.paste(tmp_image, mask=tmp_image)

class PILHandler:
    """
    Elements are not expected to draw directly to PIL draw, but through methods in this class.
    This class also contains all other data needed for different elements to be drawn (coordinate
    system bounds, antialiasing_coef, and so on).
    """

    # Those two values may be changed during the lifetime of this object. If transparency
    # is used then it will happen:
    pil_image = None
    pil_draw = None

    antialiasing_coef = None

    bounds = None

    __font = None

    def __init__(self, antialiasing_coef, bounds):
        assert antialiasing_coef
        assert bounds

        self.antialiasing_coef = antialiasing_coef
        self.bounds = bounds

    def get_font(self):
        """ Load the font to be used for labels and point names. """
        if not self.__font:
            self.__font = mod_imagefont.truetype(DEFAULT_FONT_LOCATION, int(DEFAULT_FONT_SIZE * self.antialiasing_coef))

        return self.__font

    def update_pil_image_draw(self, image, draw):
        """
        When drawing the coordinate system for a custom element, the CS will "decide" if to use existing
        PIL image and draw or set new ones with this method
        """
        self.pil_image = image
        self.pil_draw = draw

    def draw_point(self, x, y, color, style='+', label=None, label_position=None):
        """
        Draw single point.

        style: can be '.' (single pixel), '+', 'x', and 'o' (small circle)
        label: text to be displayed
        label_position: one of the label position constants (CENTER_UP, RIGHT_DOWN, ...). The default
        is set in draw_text()
        """
        image_x, image_y = mod_utils.cartesius_to_image_coord(x, y, self.bounds)

        if label_position:
            assert len(label_position) == 2

        if not color:
            color = DEFAULT_POINT_COLOR

        if style == '.' or style == None:
            self.pil_draw.point((image_x, image_y), color)
        elif style == 'x':
            delta = 2 * self.antialiasing_coef
            self.pil_draw.line((image_x - delta, image_y - delta, image_x + delta, image_y + delta), color)
            self.pil_draw.line((image_x - delta, image_y + delta, image_x + delta, image_y - delta), color)
        elif style == '+':
            delta = 2 * self.antialiasing_coef
            self.pil_draw.line((image_x - delta, image_y, image_x + delta, image_y), color)
            self.pil_draw.line((image_x, image_y + delta, image_x, image_y - delta), color)
        elif style == ' ':
            # No point
            pass
        elif style == 'o':
            delta = 2 * self.antialiasing_coef
            self.pil_draw.ellipse(
                    (image_x - delta, image_y - delta, image_x + delta, image_y + delta),
                    fill=None,
                    outline=color)
        else:
            mod_logging.error('Invalid style: {0}, valid: ".", "x", "+" and "o"'.format(style))
            self.pil_draw.point((image_x, image_y), color)

        if label:
            self.draw_text(x, y, label, color, label_position=label_position)

    def draw_line(self, x1, y1, x2, y2, color):
        image_x1, image_y1 = mod_utils.cartesius_to_image_coord(x1, y1, self.bounds)
        image_x2, image_y2 = mod_utils.cartesius_to_image_coord(x2, y2, self.bounds)

        self.pil_draw.line((image_x1, image_y1, image_x2, image_y2), color)

    def draw_polygon(self, points, fill_color):
        image_points = []
        for x, y in points:
            image_coordinates = mod_utils.cartesius_to_image_coord(x, y, self.bounds)
            image_points.append(image_coordinates)
        self.pil_draw.polygon(
            image_points,
            fill=fill_color)

    def draw_text(self, x, y, text, color, label_position=None):
        """
        Draw text.

        label_position: one of the label position constants (CENTER_UP, RIGHT_DOWN, ...). The default
        is set in draw_text()
        """
        label_position = label_position if label_position else RIGHT_DOWN

        image_x, image_y = mod_utils.cartesius_to_image_coord(x, y, self.bounds)

        font = self.get_font()

        label_width, label_height = font.getsize(text)

        if label_position[0] == -1:
            image_x = image_x - label_width - 4. * self.antialiasing_coef
        elif label_position[0] == 0:
            image_x = image_x - label_width / 2.
        elif label_position[0] == 1:
            image_x += 4 * self.antialiasing_coef

        if label_position[1] == -1:
            image_y += 2 * self.antialiasing_coef
        elif label_position[1] == 0:
            image_y = image_y - label_height / 2.
        elif label_position[1] == 1:
            image_y = image_y - label_height - 2 * self.antialiasing_coef

        self.pil_draw.text((image_x, image_y), text, color, font)

    def draw_circle(self, x, y, radius, line_color, fill_color):
        x1, y1 = mod_utils.cartesius_to_image_coord(
                x = x - radius / 2.,
                y = y + radius / 2.,
                bounds = self.bounds)
        x2, y2 = mod_utils.cartesius_to_image_coord(
                x = x + radius / 2.,
                y = y - radius / 2.,
                bounds = self.bounds)

        self.pil_draw.ellipse(
                (x1, y1, x2, y2),
                fill = fill_color,
                outline = line_color)

    def draw_pieslice(self, x, y, radius, start_angle, end_angle, fill_color=None, color=None):
        x1, y1 = mod_utils.cartesius_to_image_coord(
                x=x - radius,
                y=y + radius,
                bounds=self.bounds)
        x2, y2 = mod_utils.cartesius_to_image_coord(
                x=x + radius,
                y=y - radius,
                bounds=self.bounds)

        self.pil_draw.pieslice(
                (int(x1), int(y1), int(x2), int(y2)),
                int(start_angle),
                int(end_angle),
                fill=fill_color,
                outline=color)


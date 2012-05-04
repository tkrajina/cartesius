# -*- coding: utf-8 -*-

import re as mod_re
import math as mod_math

import main as mod_main

"""
# Element class template (use this for new elements):

class MyElement(mod_main.CoordinateSystemElement):
    \"\"\" Abstract class, every subclass should detect bounds and have the code to draw this item \"\"\"

    def __init__(self, ...params..., transparency_mask=None):
        mod_main.CoordinateSystemElement.__init__(self, transparency_mask=transparency_mask)

        ...set local params...

        # If this element will resize the current bounds, execute:
        self.reload_bounds()

    def reload_bounds(self):
        # Code to reload current bounds based on this element data:
        ...

    def process_image(self, draw_handler):
        # Use methods in draw_handler to draw this element.
        # If you need the bounds of the current coordinate system, use draw_handler.bounds
"""

class Axis(mod_main.CoordinateSystemElement):
    """
    Axis class.

    Axis can be horizontal or vertical.

    Axis can, also, be default ((0,0) as center) or detached (if (0,0) if not the center).
    """

    horizontal = None
    color = None
    label_color = None

    # If set, draw label every:
    labels = None
    labels_suffix = None

    # If set, draw point every:
    points = None

    hide_positive = None
    hide_negative = None

    center = None

    def __init__(self, horizontal=False, vertical=False, color=None, labels=None, label_color=None,
            label_position=None, points=None, transparency_mask=None, hide_positive=False,
            hide_negative=False, hide=False, detached_center=None):
        """
        labels: May be an integer, or string like '100m' or dict like {1000:'one km', 500:'half km'}
        """
        mod_main.CoordinateSystemElement.__init__(self, transparency_mask=transparency_mask)

        if bool(horizontal) == bool(vertical):
            raise Exception('Axis must be set to be horizontal or vertical')

        self.horizontal = horizontal

        self.color = self.get_color(color if color else mod_main.DEFAULT_AXES_COLOR)
        self.label_color = self.get_color(label_color if label_color else mod_main.DEFAULT_LABEL_COLOR)

        if isinstance(labels, str) or isinstance(labels, unicode):
            groups = mod_re.findall('([0-9\.]+)(.*)', labels)

            if not len(groups) == 1 and len(groups[0]) == 2:
                raise Exception('Invalid label string: {0}'.format(label))

            self.labels = float(groups[0][0])
            self.labels_suffix = groups[0][1]
        elif isinstance(labels, dict):
            self.labels = labels
        else:
            self.labels = float(labels) if labels else None

        self.points = float(points) if points else 1

        if self.horizontal:
            self.label_position = label_position if label_position else mod_main.CENTER_DOWN
        else:
            self.label_position = label_position if label_position else mod_main.LEFT_CENTER

        if not len(self.label_position) == 2:
            raise Exception('Invalid label position: {0}'.format(self.label_position))

        self.hide_positive = hide_positive
        self.hide_negative = hide_negative

        if hide:
            self.hide_positive = True
            self.hide_negative = True

        if detached_center:
            if not len(detached_center) == 2:
                raise Exception('Invalid detached center: {0}'.format(detached_center))
            self.center = detached_center
        else:
            self.center = (0, 0)

        #Bounds are not important for axes:
        #self.reload_bounds()

    def is_detached(self):
        return self.center[0] != 0 or self.center[1] != 0

    def reload_bounds(self):
        # not important
        pass

    def is_horizontal(self):
        return bool(self.horizontal)

    def is_vertical(self):
        return not self.is_horizontal()

    def get_start_end(self, step, lower_bound, higher_bound):
        start = int(mod_math.floor(lower_bound / float(step)) * step)
        end = int(mod_math.ceil(higher_bound / float(step)) * step)

        if self.hide_negative:
            start = max(start, 0)
        if self.hide_positive:
            end = min(end, 0)

        if self.hide_negative:
            start = max(start, 0)
        if self.hide_positive:
            end = min(end, 0)

        return start, end

    def draw_points(self, draw_handler):
        if not self.points:
            return

        if self.horizontal:
            points_from, points_to = self.get_start_end(
                    self.points,
                    draw_handler.bounds.left - self.center[0],
                    draw_handler.bounds.right - self.center[0])
        else:
            points_from, points_to = self.get_start_end(
                    self.points,
                    draw_handler.bounds.bottom - self.center[1],
                    draw_handler.bounds.top - self.center[1])

        i = points_from
        while i <= points_to:
            self.draw_point(i, draw_handler)
            i += self.points

    def draw_point(self, i, draw_handler):
        if self.horizontal:
            x, y = self.center[0] + i, self.center[1] + 0
        else:
            x, y = self.center[0] + 0, self.center[1] + i

        draw_handler.draw_point(x, y, color=self.color, style='+')

    def draw_labels(self, draw_handler):
        if not self.labels:
            return

        if isinstance(self.labels, dict):
            for i, label in self.labels.items():
                self.draw_label(i, draw_handler, label=label)
        else:
            if self.horizontal:
                labels_from, labels_to = self.get_start_end(
                        self.labels,
                        draw_handler.bounds.left - self.center[0],
                        draw_handler.bounds.right - self.center[0])
            else:
                labels_from, labels_to = self.get_start_end(
                        self.labels,
                        draw_handler.bounds.bottom - self.center[1],
                        draw_handler.bounds.top - self.center[1])

            i = labels_from
            while i <= labels_to:
                self.draw_label(i, draw_handler)
                i += self.labels

    def draw_label(self, i, draw_handler, label=None):
        if i == 0:
            return

        if i == int(i):
            i = int(i)

        if label:
            label = str(label)
        else:
            label = str(i)
            if self.labels_suffix:
                label += self.labels_suffix

        x, y = self.get_point(i)
        x, y = x + self.center[0], y + self.center[1]

        draw_handler.draw_text(x, y, label, mod_main.DEFAULT_LABEL_COLOR, label_position=self.label_position)

    def get_point(self, n):
        if self.horizontal:
            return n, 0
        else:
            return 0, n

    def process_image(self, draw_handler):
        if self.horizontal:
            start = draw_handler.bounds.left
            end = draw_handler.bounds.right

            if self.hide_negative:
                start = max(start, self.center[0])
            if self.hide_positive:
                end = min(end, self.center[0])

            axe_from_point = start, self.center[1]
            axe_to_point = end, self.center[1]
        else:
            start = draw_handler.bounds.bottom
            end = draw_handler.bounds.top

            if self.hide_negative:
                start = max(start, self.center[1])
            if self.hide_positive:
                end = min(end, self.center[1])

            axe_from_point = self.center[0], start
            axe_to_point = self.center[0], end

        self.draw_points(draw_handler)
        self.draw_labels(draw_handler)

        draw_handler.draw_line(axe_from_point[0], axe_from_point[1], axe_to_point[0], axe_to_point[1], self.color)

class Point(mod_main.CoordinateSystemElement):

    style = None
    label_position = None
    position = None
    color = None

    def __init__(self, position, label=None, label_position=None, style=None,
            color=None, transparency_mask=None):
        mod_main.CoordinateSystemElement.__init__(self, transparency_mask=transparency_mask)

        if not position or not len(position) == 2:
            raise Exception('Invalid position {0}'.format(position))

        if label_position:
            if not len(label_position) == 2:
                raise Exception('Invalid label position {0}'.format(label_position))
        else:
            label_position = mod_main.CENTER_DOWN

        self.position = position
        self.label = str(label) if label else None
        self.label_position = label_position
        self.style = style
        self.color = self.get_color(color)

        self.reload_bounds()

    def reload_bounds(self):
        self.bounds.update(point=self.position)

    def process_image(self, draw_handler):
        draw_handler.draw_point(self.position[0], self.position[1], style=self.style,
                color = self.color, label = self.label, label_position = self.label_position)

class Grid(mod_main.CoordinateSystemElement):

    horizontal = None
    vertical = None
    color = None

    def __init__(self, horizontal, vertical, color=None, transparency_mask=None):
        mod_main.CoordinateSystemElement.__init__(self, transparency_mask=transparency_mask)

        if not horizontal and not vertical:
            raise Exception('Grid must have horizontal or vertical distance.')

        self.horizontal = float(horizontal) if horizontal else None
        self.vertical = float(vertical) if vertical else None
        self.color = self.get_color(color if color else mod_main.DEFAULT_GRID_COLOR)

        #Bounds are not important for axes:
        #self.reload_bounds()

    def reload_bounds(self):
        # not important
        pass

    def process_image(self, draw_handler):
        if self.vertical:
            axe_from_point = 0, draw_handler.bounds.bottom
            axe_to_point = 0, draw_handler.bounds.top
            i = mod_math.floor(draw_handler.bounds.left / self.vertical)
            while i < mod_math.ceil(draw_handler.bounds.right):
                x, y = i, 0
                if i != 0 and i != draw_handler.bounds.left and i != draw_handler.bounds.right:
                    draw_handler.draw_line(x, axe_from_point[1], x, axe_to_point[1], self.get_color_with_transparency(self.color))
                i += self.vertical

        if self.horizontal:
            axe_from_point = draw_handler.bounds.left, 0
            axe_to_point = draw_handler.bounds.right, 0
            i = mod_math.floor(draw_handler.bounds.bottom / self.horizontal)
            while i < mod_math.ceil(draw_handler.bounds.top):
                x, y = 0, i
                if i != 0 and i != draw_handler.bounds.bottom and i != draw_handler.bounds.top:
                    draw_handler.draw_line(axe_from_point[0], y, axe_to_point[0], y, self.get_color_with_transparency(self.color))
                i += self.horizontal

class Line(mod_main.CoordinateSystemElement):

    start = None
    end = None
    color = None

    def __init__(self, start, end, color=None, transparency_mask=None):
        mod_main.CoordinateSystemElement.__init__(self, transparency_mask=transparency_mask)

        if not start or len(start) != 2:
            raise Exception('Invalid start of line: {0}'.format(start))
        if not end or len(end) != 2:
            raise Exception('Invalid end of line: {0}'.format(end))

        self.start = start
        self.end = end
        self.color = self.get_color(color if color else mod_main.DEFAULT_ELEMENT_COLOR)

        self.reload_bounds()

    def reload_bounds(self):
        self.bounds.update(point=self.start)
        self.bounds.update(point=self.end)

    def process_image(self, draw_handler):
        draw_handler.draw_line(self.start[0], self.start[1], self.end[0], self.end[1], self.get_color_with_transparency(self.color))

class Circle(mod_main.CoordinateSystemElement):

    center = None
    radius = None
    color = None
    fill_color = None

    def __init__(self, center, radius, color=None, fill_color=None, transparency_mask=None):
        mod_main.CoordinateSystemElement.__init__(self, transparency_mask=transparency_mask)

        if not center or len(center) != 2:
            raise Exception('Invalid center: {0}'.format(center))

        if not radius > 0:
            raise Exception('Invalid radius: {0}'.format(radius))

        self.center = center
        self.radius = radius

        self.color = self.get_color(color if color else DEFAULT_ELEMENT_COLOR)
        self.fill_color = self.get_color(fill_color)

        self.reload_bounds()

    def reload_bounds(self):
        self.bounds.update(point=(self.center[0] + self.radius, self.center[1]))
        self.bounds.update(point=(self.center[0] - self.radius, self.center[1]))
        self.bounds.update(point=(self.center[0], self.center[1] + self.radius))
        self.bounds.update(point=(self.center[0], self.center[1] - self.radius))

    def process_image(self, draw_handler):
        draw_handler.draw_circle(
                self.center[0],
                self.center[1],
                self.radius,
                fill_color = self.get_color_with_transparency(self.fill_color),
                line_color = self.get_color_with_transparency(self.color))



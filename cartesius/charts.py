# -*- coding: utf-8 -*-

""" Charts are normal CoordinateSystemElements """

import math as mod_math
import collections as mod_collections
import types as mod_types

import main as mod_main
import colors as mod_colors

# Default color palete from: http://www.colourlovers.com/pattern/2429885/Spring_flower_aerial
DEFAULT_COLORS = (
        (141, 198, 183),
        (207, 249, 117),
        (230, 193, 238),
        (242, 229, 229),
)

ChartData = mod_collections.namedtuple(
        'ChartData',
        ('key', 'value', 'size', 'label', 'label_position', 'color', 'fill_color'))

def get_generator(data):
    """
    In case of a big dataset, no need to load the entire list in memory, it can be given to
    cartesius as a generator function.

    In case data is callable and the result is a generator, then data is returned, oherwisea the
    result is a function that returns a generator through data.
    """
    if callable(data):
        if isinstance(data(), mod_types.GeneratorType):
            return data

    if not data:
        raise Exception('Invalid or empty data: {0}'.format(data))

    def generator():
        for i in data:
            yield i
    return generator

def data(key, value, size=None, label=None, label_position=None, color=None, fill_color=None):
    """
    Use this function to prepare data for all charts.
    """
    return ChartData(key, value, size, label, label_position, mod_colors.get_color(color),
                     mod_colors.get_color(fill_color))

class BarChart(mod_main.CoordinateSystemElement):

    horizontal = None

    color = None

    data_generator = None
    width = None

    def __init__(self, data, horizontal=None, vertical=None, width=None, color=None, 
                 transparency_mask=None):
        mod_main.CoordinateSystemElement.__init__(self, transparency_mask=transparency_mask)

        if bool(horizontal) == bool(vertical):
            raise Exception('Bar chart must be be horizontal or vertical')
        if not data:
            raise Exception('Data must be set')

        self.horizontal = horizontal

        self.data_generator = get_generator(data)
        self.width = width
        self.color = self.get_color(color)

        self.reload_bounds()

    def is_horizontal(self):
        return bool(self.horizontal)

    def is_vertical(self):
        return not self.is_horizontal()

    def get_point(self, x, y):
        if self.horizontal:
            return y, x
        else:
            return x, y

    def reload_bounds(self):
        for item in self.data_generator():
            if self.width:
                if self.horizontal:
                    self.bounds.update(y=item.key)
                    self.bounds.update(y=item.key + self.width)
                    self.bounds.update(x=item.value)
                else:
                    self.bounds.update(x=item.key)
                    self.bounds.update(x=item.key + self.width)
                    self.bounds.update(y=item.value)
            else:
                if self.horizontal:
                    self.bounds.update(y=item.key)
                    self.bounds.update(y=item.value)
                    self.bounds.update(x=item.size)
                else:
                    self.bounds.update(x=item.key)
                    self.bounds.update(x=item.value)
                    self.bounds.update(y=item.size)

    def process_image(self, draw_handler):
        for index, item in enumerate(self.data_generator()):
            if self.width:
                start, end, value = item.key, item.key + self.width, item.value
            else:
                start, end, value = item.key, item.value, item.size

            if item.fill_color:
                fill_color = item.fill_color
            else:
                fill_color = DEFAULT_COLORS[index % len(DEFAULT_COLORS)]

            draw_handler.draw_polygon(
                (self.get_point(start, 0), self.get_point(start, value), self.get_point(end, value), self.get_point(end, 0)),
                fill_color = fill_color)

            if item.label:
                if self.horizontal:
                    if item.label_position:
                        label_position = item.label_position
                    elif value > 0:
                        label_position = mod_main.LEFT_CENTER
                    else:
                        label_position = mod_main.RIGHT_CENTER
                    draw_handler.draw_text(0, (start + end) / 2., item.label, mod_main.DEFAULT_LABEL_COLOR, label_position)
                else:
                    if item.label_position:
                        label_position = item.label_position
                    elif value > 0:
                        label_position = mod_main.CENTER_DOWN
                    else:
                        label_position = mod_main.CENTER_UP
                    draw_handler.draw_text((start + end) / 2., 0, item.label, mod_main.DEFAULT_LABEL_COLOR, label_position)

            if self.color:
                if self.horizontal:
                    draw_handler.draw_line(0, start, value, start, self.color)
                    draw_handler.draw_line(value, end, 0, end, self.color)
                    draw_handler.draw_line(value, start, value, end, self.color)
                else:
                    draw_handler.draw_line(start, 0, start, value, self.color)
                    draw_handler.draw_line(end, value, end, 0, self.color)
                    draw_handler.draw_line(start, value, end, value, self.color)


class PieChart(mod_main.CoordinateSystemElement):

    color = None

    data_generator = None
    center = None
    radius = None

    def __init__(self, data, color=None, center=None, radius=None,
            transparency_mask=None):
        mod_main.CoordinateSystemElement.__init__(self, transparency_mask=transparency_mask)

        if not data:
            raise Exception('Invalid data {0}'.format(data))

        self.data_generator = get_generator(data)

        self.color = self.get_color(color)

        if center:
            if len(center) != 2:
                raise Exception('Invalid center {0}'.format(center))
            self.center = center
        else:
            self.center = (0, 0)

        if radius:
            self.radius = radius
        else:
            self.radius = 1

        # If this element will resize the current bounds, execute:
        self.reload_bounds()

    def reload_bounds(self):
        self.bounds.update(x=self.center[0] - self.radius * 1.25)
        self.bounds.update(x=self.center[0] + self.radius * 1.25)
        self.bounds.update(y=self.center[1] - self.radius * 1.25)
        self.bounds.update(y=self.center[1] + self.radius * 1.25)

    def draw_label(self, angle, label, draw_handler):
        assert label
        assert draw_handler

        angle = (angle + 360) % 360

        # TODO
        color = (100, 100, 100)

        radian_angle = angle / 180. * mod_math.pi

        x = mod_math.sin(radian_angle)
        y = mod_math.cos(radian_angle)

        x_from = x# * 0.9
        y_from = y# * 0.9
        x_to = x * 1.1
        y_to = y * 1.1

        draw_handler.draw_line(x_from, y_from, x_to, y_to, color)

        if angle < 180:
            draw_handler.draw_line(x_to, y_to, x_to + 0.3, y_to, color)
            if angle < 90 or angle > 270:
                draw_handler.draw_text(x_to, y_to, label, (0, 0, 0), mod_main.RIGHT_UP)
            else:
                draw_handler.draw_text(x_to, y_to, label, (0, 0, 0), mod_main.RIGHT_DOWN)
        else:
            draw_handler.draw_line(x_to, y_to, x_to - 0.3, y_to, color)
            if angle < 90 or angle > 270:
                draw_handler.draw_text(x_to, y_to, label, (0, 0, 0), mod_main.LEFT_UP)
            else:
                draw_handler.draw_text(x_to, y_to, label, (0, 0, 0), mod_main.LEFT_DOWN)

    def process_image(self, draw_handler):
        sum_values = 0.

        for item in self.data_generator():
            sum_values += item.value

        current_angle = 0
        for index, item in enumerate(self.data_generator()):
            if item.value > 0:
                label = str(item.key)
                delta = 360 * item.value / sum_values

                start_angle = current_angle
                end_angle = current_angle + delta

                if item.fill_color:
                    fill_color = item.fill_color
                else:
                    fill_color = DEFAULT_COLORS[index % len(DEFAULT_COLORS)]

                draw_handler.draw_pieslice(
                        self.center[0],
                        self.center[1],
                        radius = 1,
                        start_angle = start_angle - 90,
                        end_angle = end_angle - 90,
                        fill_color = fill_color,
                        color = self.color)

                self.draw_label((start_angle + end_angle) / 2., label, draw_handler)

                current_angle += delta

class LineChart(mod_main.CoordinateSystemElement):

    color = None
    fill_color = None

    data_generator = None

    def __init__(self, data, color=None, fill_color=False, transparency_mask=None):
        mod_main.CoordinateSystemElement.__init__(self, transparency_mask=transparency_mask)

        if not data:
            raise Exception('Invalid data {0}'.format(data))

        self.color = self.get_color(color)
        self.fill_color = self.get_color(fill_color)

        prepared_data = data

        self.data_generator = get_generator(prepared_data)

        self.reload_bounds()

    def reload_bounds(self):
        for item in self.data_generator():
            self.bounds.update(point=(item.key, item.value))

    def process_image(self, draw_handler):
        for i, point in enumerate(self.data_generator()):
            if i > 0:
                x1, y1 = previous[0], previous[1]
                x2, y2 = point[0], point[1]
                if self.fill_color:
                    draw_handler.draw_polygon(
                        [(x1, 0), (x1, y1), (x2, y2), (x2, 0)],
                        fill_color = self.get_color_with_transparency(self.fill_color)
                   )
                draw_handler.draw_line(x1, y1, x2, y2, self.get_color_with_transparency(self.color))

            if point.label:
                if point.label_position:
                    label_position = point.label_position
                else:
                    label_position = mod_main.CENTER_UP

                draw_handler.draw_text(point.key, point.value, point.label, mod_main.DEFAULT_LABEL_COLOR, label_position)
                

            previous = point

class Function(mod_main.CoordinateSystemElement):

    function = None
    step = None
    start = None
    end = None
    points = None
    color = None
    fill_color = None

    def __init__(self, function, start=None, end=None, step=None, fill_color=False, color=None, transparency_mask=None):
        mod_main.CoordinateSystemElement.__init__(self, transparency_mask=transparency_mask)

        if not function:
            raise Exception('Invalid function: {0}'.format(function))

        self.function = function
        self.step = float(step if step else 0.1)
        self.start = start if start != None else -1
        self.end = end if end != None else -1

        self.fill_color = self.get_color(fill_color)
        self.color = self.get_color(color if color else mod_main.DEFAULT_ELEMENT_COLOR)

        self.points = []

        if not self.start < self.end:
            raise Exception('Invalid function start ({0}) and end ({1})'.format(self.start, self.end))
        if not self.step > 0:
            raise Exception('Invalid function step: {0}'.format(self.step))

        self.compute()

    def compute(self):
        self.points = []
        # TODO: int or floor/ceil ?
        for i in range(int((self.end - self.start) / self.step)):
            x = self.start + i * self.step
            y = self.function(x)
            point = (x, y)
            self.points.append(point)

    def reload_bounds(self):
        for point in self.points:
            self.bounds.update(point=point)

    def process_image(self, draw_handler):

        for i, point in enumerate(self.points):
            if i > 0:
                previous = self.points[i - 1]

                x1, y1 = previous[0], previous[1]
                x2, y2 = point[0], point[1]

                if self.fill_color:
                    draw_handler.draw_polygon(
                        [(x1, 0), (x1, y1), (x2, y2), (x2, 0)],
                        fill_color = self.get_color_with_transparency(self.fill_color)
                   )
                draw_handler.draw_line(x1, y1, x2, y2, self.get_color_with_transparency(self.color))



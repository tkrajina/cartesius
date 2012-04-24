# -*- coding: utf-8 -*-

""" Charts are normal CoordinateSystemElements """

import math as mod_math

import main as mod_main

# Default color palete from: http://www.colourlovers.com/pattern/2429885/Spring_flower_aerial
DEFAULT_COLORS = (
        ( 141, 198, 183 ),
        ( 207, 249, 117 ),
        ( 230, 193, 238 ),
        ( 242, 229, 229 ),
)

class BarChart( mod_main.CoordinateSystemElement ):

    # TODO: vertical

    color = None
    fill_colors = None

    data = None
    width = None

    def __init__( self, data = None, width = None, color = None, fill_colors = None, transparency_mask = None ):
        mod_main.CoordinateSystemElement.__init__( self, transparency_mask = transparency_mask )

        assert data, 'Data must be set'

        self.data = data
        self.width = width
        self.color = color
        self.fill_colors = fill_colors if fill_colors else DEFAULT_COLORS

        self.reload_bounds()

    def reload_bounds( self ):
        for item in self.data:
            if self.width:
                assert item and len( item ) == 2, \
                        'With width, data must countain (key, value) tuples, found {0}'.format( item )
                self.bounds.update( x = item[ 0 ] )
                self.bounds.update( x = item[ 0 ] + self.width )
                self.bounds.update( y = item[ 1 ] )
            else:
                assert item and len( item ) == 3, \
                        'Without width, data must contain (from, to, value) tuples, found {0}'.format( item )
                self.bounds.update( x = item[ 0 ] )
                self.bounds.update( x = item[ 1 ] )
                self.bounds.update( y = item[ 2 ] )

    def process_image( self, draw_handler ):
        for index, item in enumerate( self.data ):
            if self.width:
                assert item and len( item ) == 2, 'With width given, data must countain (key, value) tuples, found {0}'.format( item )
                start, end, value = item[ 0 ], item[ 0 ] + self.width, item[ 1 ]
            else:
                assert item and len( item ) == 3, 'Without with given, data must contain (from, to, value) tuples, found {0}'.format( item )
                start, end, value = item[ 0 ], item[ 1 ], item[ 2 ]

            draw_handler.draw_polygon(
                ( ( start, 0 ), ( start, value ), ( end, value ), ( end, 0 ) ), fill_color = self.fill_colors[ index % len( self.fill_colors ) ] )

            if self.color:
                draw_handler.draw_line( start, 0, start, value, self.color )
                draw_handler.draw_line( end, value, end, 0, self.color )
                draw_handler.draw_line( start, value, end, value, self.color )

class PieChart( mod_main.CoordinateSystemElement ):

    color = None
    fill_colors = None

    data = None
    center = None
    radius = None

    def __init__( self, data, color = None, fill_colors = None, center = None, radius = None,
            transparency_mask = None ):
        mod_main.CoordinateSystemElement.__init__( self, transparency_mask = transparency_mask )

        self.data = data

        self.color = color
        self.fill_colors = fill_colors if fill_colors else DEFAULT_COLORS

        if center:
            assert len( center ) == 2, 'Invalid center {0}'.format( center )
            self.center = center
        else:
            self.center = ( 0, 0 )

        if radius:
            self.radius = radius
        else:
            self.radius = 1

        # If this element will resize the current bounds, execute:
        self.reload_bounds()

    def reload_bounds( self ):
        self.bounds.update( x = self.center[ 0 ] - self.radius * 1.25 )
        self.bounds.update( x = self.center[ 0 ] + self.radius * 1.25 )
        self.bounds.update( y = self.center[ 1 ] - self.radius * 1.25 )
        self.bounds.update( y = self.center[ 1 ] + self.radius * 1.25 )

    def draw_label( self, angle, label, draw_handler ):
        assert label
        assert draw_handler

        angle = ( angle + 360 ) % 360

        # TODO
        color = ( 100, 100, 100 )

        radian_angle = angle / 180. * mod_math.pi

        x = mod_math.sin( radian_angle )
        y = mod_math.cos( radian_angle )

        x_from = x# * 0.9
        y_from = y# * 0.9
        x_to = x * 1.1
        y_to = y * 1.1

        draw_handler.draw_line( x_from, y_from, x_to, y_to, color )

        if angle < 180:
            draw_handler.draw_line( x_to, y_to, x_to + 0.3, y_to, color )
            if angle < 90 or angle > 270:
                draw_handler.draw_text( x_to, y_to, label, ( 0, 0, 0 ), mod_main.RIGHT_UP )
            else:
                draw_handler.draw_text( x_to, y_to, label, ( 0, 0, 0 ), mod_main.RIGHT_DOWN )
        else:
            draw_handler.draw_line( x_to, y_to, x_to - 0.3, y_to, color )
            if angle < 90 or angle > 270:
                draw_handler.draw_text( x_to, y_to, label, ( 0, 0, 0 ), mod_main.LEFT_UP )
            else:
                draw_handler.draw_text( x_to, y_to, label, ( 0, 0, 0 ), mod_main.LEFT_DOWN )

    def process_image( self, draw_handler ):
        sum_values = 0.
        for item in self.data:
            value = item[ 0 ]
            sum_values += value

        current_angle = 0
        for index, item in enumerate( self.data ):
            value = item[ 0 ]
            label = str( item[ 1 ] )
            delta = 360 * value / sum_values

            start_angle = current_angle
            end_angle = current_angle + delta

            fill_color = self.fill_colors[ index % len( self.fill_colors ) ]

            draw_handler.draw_pieslice(
                    self.center[ 0 ],
                    self.center[ 1 ],
                    radius = 1,
                    start_angle = start_angle - 90,
                    end_angle = end_angle - 90,
                    fill_color = fill_color,
                    color = self.color )

            self.draw_label( ( start_angle + end_angle ) / 2., label, draw_handler )

            current_angle += delta

class LineChart( mod_main.CoordinateSystemElement ):

    color = None
    fill_color = None

    items = None

    def __init__( self, values, color = None, fill_color = False, transparency_mask = None ):
        mod_main.CoordinateSystemElement.__init__( self, transparency_mask = transparency_mask )

        assert values

        self.color = color
        self.fill_color = fill_color

        self.items = []

        if hasattr( values, 'keys' ) and callable( getattr( values, 'keys' ) ):
            keys = values.keys()
            keys.sort()

            for key in keys:
                item = ( key, values[ key ] )
                self.items.append( item )
        else:
            self.items = values

        for item in self.items:
            assert len( item ) == 2

        self.reload_bounds()

    def reload_bounds( self ):
        assert self.items
        for key, value in self.items:
            self.bounds.update( point = ( key, value ) )

    def process_image( self, draw_handler ):
        assert self.items

        for i, point in enumerate( self.items ):
            if i > 0:
                previous = self.items[ i - 1 ]
                x1, y1 = previous[ 0 ], previous[ 1 ]
                x2, y2 = point[ 0 ], point[ 1 ]
                if self.fill_color:
                    draw_handler.draw_polygon(
                        [ ( x1, 0 ), ( x1, y1 ), ( x2, y2 ), ( x2, 0 ) ],
                        fill_color = self.get_color_with_transparency( self.fill_color )
                    )
                draw_handler.draw_line( x1, y1, x2, y2, self.get_color_with_transparency( self.color ) )

class Function( mod_main.CoordinateSystemElement ):

    function = None
    step = None
    start = None
    end = None
    points = None
    color = None
    fill_color = None

    def __init__( self, function, start = None, end = None, step = None, fill_color = False, color = None, transparency_mask = None ):
        mod_main.CoordinateSystemElement.__init__( self, transparency_mask = transparency_mask )

        assert function

        self.function = function
        self.step = float( step if step else 0.1 )
        self.start = start if start != None else -1
        self.end = end if end != None else -1

        self.fill_color = fill_color
        self.color = color if color else mod_main.DEFAULT_ELEMENT_COLOR

        self.points = []

        assert self.start < self.end
        assert self.step > 0

        self.compute()

    def compute( self ):
        self.points = []
        # TODO: int or floor/ceil ?
        for i in range( int( ( self.end - self.start ) / self.step ) ):
            x = self.start + i * self.step
            y = self.function( x )
            point = ( x, y )
            self.points.append( point )

    def reload_bounds( self ):
        for point in self.points:
            self.bounds.update( point = point )

    def process_image( self, draw_handler ):

        for i, point in enumerate( self.points ):
            if i > 0:
                previous = self.points[ i - 1 ]

                x1, y1 = previous[ 0 ], previous[ 1 ]
                x2, y2 = point[ 0 ], point[ 1 ]

                if self.fill_color:
                    draw_handler.draw_polygon(
                        [ ( x1, 0 ), ( x1, y1 ), ( x2, y2 ), ( x2, 0 ) ],
                        fill_color = self.get_color_with_transparency( self.fill_color )
                    )
                draw_handler.draw_line( x1, y1, x2, y2, self.get_color_with_transparency( self.color ) )


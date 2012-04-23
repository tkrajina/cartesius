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
		self.bounds.update( x = self.center[ 0 ] - self.radius )
		self.bounds.update( x = self.center[ 0 ] + self.radius )
		self.bounds.update( y = self.center[ 1 ] - self.radius )
		self.bounds.update( y = self.center[ 1 ] + self.radius )

	def draw_label( self, angle, label, draw_handler, color ):
		assert label
		assert draw_handler

		angle = ( angle + 360 ) % 360
		print label, angle

		radian_angle = angle / 180. * mod_math.pi

		x = mod_math.sin( radian_angle )
		y = mod_math.cos( radian_angle )

		draw_handler.draw_line( 0, 0, x, y, color )

		if angle < 180:
			draw_handler.draw_line( x, y, x + 0.5, y, color )
			draw_handler.draw_text( x, y, label, ( 0, 0, 0 ), mod_main.RIGHT_UP )
		else:
			draw_handler.draw_line( x, y, x - 0.5, y, color )
			draw_handler.draw_text( x, y, label, ( 0, 0, 0 ), mod_main.LEFT_UP )
	
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

			self.draw_label( ( start_angle + end_angle ) / 2., label, draw_handler, fill_color )

			current_angle += delta

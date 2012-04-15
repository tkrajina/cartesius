# -*- coding: utf-8 -*-

""" Charts are normal CoordinateSystemElements """

import main as mod_main

class BarChart( mod_main.CoordinateSystemElement ):

	color = None
	fill_color = None

	data = None
	width = None

	def __init__( self, data = None, width = None, color = None, fill_color = None, transparency_mask = None ):
		mod_main.CoordinateSystemElement.__init__( self, transparency_mask = transparency_mask )

		assert data, 'Data must be set'

		self.data = data
		self.width = width
		self.color = color
		self.fill_color = fill_color if fill_color else mod_main.DEFAULT_ELEMENT_COLOR

		self.reload_bounds()

	def reload_bounds( self ):
		for item in self.data:
			if self.width:
				assert item and len( item ) == 2, 'With width given, data must countain (key, value) tuples'
				self.bounds.update( x = item[ 0 ] )
				self.bounds.update( x = item[ 0 ] + self.width )
				self.bounds.update( y = item[ 1 ] )
			else:
				assert item and len( item ) == 3, 'Without with given, data must contain (from, to, value) tuples'
				self.bounds.update( x = item[ 0 ] )
				self.bounds.update( x = item[ 1 ] )
				self.bounds.update( y = item[ 2 ] )

	def process_image( self, draw_handler ):
		for item in self.data:
			if self.width:
				assert item and len( item ) == 2, 'With width given, data must countain (key, value) tuples, found {0}'.format( item )
				start, end, value = item[ 0 ], item[ 0 ] + self.width, item[ 1 ]
			else:
				assert item and len( item ) == 3, 'Without with given, data must contain (from, to, value) tuples, found {0}'.format( item )
				start, end, value = item[ 0 ], item[ 1 ], item[ 2 ]

			draw_handler.draw_polygon( 
				( ( start, 0 ), ( start, value ), ( end, value ), ( end, 0 ) ), fill_color = self.fill_color )

			if self.color:
				draw_handler.draw_line( start, 0, start, value, self.color )
				draw_handler.draw_line( end, value, end, 0, self.color )
				draw_handler.draw_line( start, value, end, value, self.color )

# TODO:
"""
class PieChart( mod_main.CoordinateSystemElement ):

	def __init__( self, ...params..., transparency_mask = None ):
		mod_main.CoordinateSystemElement.__init__( self, transparency_mask = transparency_mask )

		...set local params...

		# If this element will resize the current bounds, execute:
		self.reload_bounds()

	def reload_bounds( self ):
		# Code to reload current bounds based on this element data:
		...
	
	def process_image( self, draw_handler ):
		# Use methods in draw_handler to draw this element.
		# If you need the bounds of the current coordinate system, use draw_handler.bounds
"""

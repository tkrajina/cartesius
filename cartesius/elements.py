# -*- coding: utf-8 -*-

import re as mod_re
import math as mod_math

import main as mod_main
import utils as mod_utils

class Axis( mod_main.CoordinateSystemElement ):
	"""
	Axis class.

	Axis can be horizontal or vertical.

	Axis can, also, be default ( (0,0) as center) or detached (if (0,0) if not the center).
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

	def __init__( self, horizontal = False, vertical = False, color = None, labels = None, label_color = None,
			label_position = None, points = None, transparency_mask = None, hide_positive = False,
			hide_negative = False, hide = False, detached_center = None ):
		"""
		labels: May be an integer, or string like '100m' or dict like {1000:'one km', 500:'half km'}
		"""
		mod_main.CoordinateSystemElement.__init__( self, transparency_mask = transparency_mask )

		assert bool( horizontal ) != bool( vertical ), 'Axis must be set to be horizontal or vertical'

		self.horizontal = horizontal

		self.color = color if color else mod_main.DEFAULT_AXES_COLOR
		self.label_color = label_color if label_color else mod_main.DEFAULT_LABEL_COLOR

		if isinstance( labels, str ) or isinstance( labels, unicode ):
			groups = mod_re.findall( '([0-9\.]+)(.*)', labels )
			assert len( groups ) == 1 and len( groups[ 0 ] ) == 2, 'Invalid label string: {0}'.format( label )
			self.labels = float( groups[ 0 ][ 0 ] )
			self.labels_suffix = groups[ 0 ][ 1 ]
		elif isinstance( labels, dict ):
			self.labels = labels
		else:
			self.labels = float( labels ) if labels else None

		self.points = float( points ) if points else 1

		if self.horizontal:
			self.label_position = label_position if label_position else mod_main.CENTER_DOWN
		else:
			self.label_position = label_position if label_position else mod_main.LEFT_CENTER

		assert len( self.label_position ) == 2

		self.hide_positive = hide_positive
		self.hide_negative = hide_negative

		if hide:
			self.hide_positive = True
			self.hide_negative = True

		if detached_center:
			assert len( detached_center ) == 2
			self.center = detached_center
		else:
			self.center = ( 0, 0 )

		#Bounds are not important for axes:
		#self.reload_bounds()

	def is_detached( self ):
		return self.center[ 0 ] != 0 or self.center[ 1 ] != 0
	
	def reload_bounds( self ):
		# not important
		pass

	def is_horizontal( self ):
		return bool( self.horizontal )

	def is_vertical( self ):
		return not self.is_horizontal()

	def get_start_end( self, step, lower_bound, higher_bound ):
		start = int( mod_math.floor( lower_bound / float( step ) ) * step )
		end = int( mod_math.ceil( higher_bound / float( step ) ) * step )

		if self.hide_negative:
			start = max( start, 0 )
		if self.hide_positive:
			end = min( end, 0 )

		if self.hide_negative:
			start = max( start, 0 )
		if self.hide_positive:
			end = min( end, 0 )

		return start, end

	def draw_dots( self, bounds, draw ):
		if not self.points:
			return

		if self.horizontal:
			dots_from, dots_to = self.get_start_end(
					self.points,
					bounds.left - self.center[ 0 ],
					bounds.right - self.center[ 0 ] )
		else:
			dots_from, dots_to = self.get_start_end(
					self.points,
					bounds.bottom - self.center[ 1 ],
					bounds.top - self.center[ 1 ] )

		i = dots_from
		while i <= dots_to:
			self.draw_dot( i, bounds, draw )
			i += self.points

	def draw_dot( self, i, bounds, draw ):
		if self.horizontal:
			x, y = mod_utils.cartesius_to_image_coord( self.center[ 0 ] + i, self.center[ 1 ] + 0, bounds )
		else:
			x, y = mod_utils.cartesius_to_image_coord( self.center[ 0 ] + 0, self.center[ 1 ] + i, bounds )

		draw.line( ( x - 2, y, x + 2, y ), mod_main.DEFAULT_AXES_COLOR )
		draw.line( ( x, y + 2, x, y - 2 ), mod_main.DEFAULT_AXES_COLOR )

	def draw_labels( self, bounds, draw ):
		if not self.labels:
			return

		if isinstance( self.labels, dict ):
			for i, label in self.labels.items():
				self.draw_label( i, bounds, draw, label = label )
		else:
			if self.horizontal:
				labels_from, labels_to = self.get_start_end(
						self.labels,
						bounds.left - self.center[ 0 ],
						bounds.right - self.center[ 0 ] )
			else:
				labels_from, labels_to = self.get_start_end(
						self.labels,
						bounds.bottom - self.center[ 1 ],
						bounds.top - self.center[ 1 ] )

			i = labels_from
			while i <= labels_to:
				self.draw_label( i, bounds, draw )
				i += self.labels

	def draw_label( self, i, bounds, draw, label = None ):
		if i == 0:
			return

		if i == int( i ):
			i = int( i )

		if label:
			label = str( label )
		else:
			label = str( i )
			if self.labels_suffix:
				label += self.labels_suffix
		label_width, label_height = draw.textsize( label )

		x, y = self.get_point( i )
		x, y = x + self.center[ 0 ], y + self.center[ 1 ]
		x, y = mod_utils.cartesius_to_image_coord( x, y, bounds )

		if self.label_position[ 0 ] == -1:
			x = x - label_width - 4
		elif self.label_position[ 0 ] == 0:
			x = x - label_width / 2.
		elif self.label_position[ 0 ] == 1:
			x += 4

		if self.label_position[ 1 ] == -1:
			y += 2
		elif self.label_position[ 1 ] == 0:
			y = y - label_height / 2.
		elif self.label_position[ 1 ] == 1:
			y = y - label_height - 2

		draw.text( ( x, y ), label, mod_main.DEFAULT_LABEL_COLOR )

	def get_point( self, n ):
		if self.horizontal:
			return n, 0
		else:
			return 0, n

	def process_image( self, image, draw, bounds ):
		if self.horizontal:
			start = bounds.left
			end = bounds.right

			if self.hide_negative:
				start = max( start, self.center[ 0 ] )
			if self.hide_positive:
				end = min( end, self.center[ 0 ] )

			axe_from_point = mod_utils.cartesius_to_image_coord( start, self.center[ 1 ], bounds )
			axe_to_point = mod_utils.cartesius_to_image_coord( end, self.center[ 1 ], bounds )
		else:
			start = bounds.bottom
			end = bounds.top

			if self.hide_negative:
				start = max( start, self.center[ 1 ] )
			if self.hide_positive:
				end = min( end, self.center[ 1 ] )

			axe_from_point = mod_utils.cartesius_to_image_coord( self.center[ 0 ], start, bounds )
			axe_to_point = mod_utils.cartesius_to_image_coord( self.center[ 0 ], end, bounds )

		self.draw_dots( bounds, draw )
		self.draw_labels( bounds, draw )

		draw.line( ( axe_from_point[ 0 ], axe_from_point[ 1 ], axe_to_point[ 0 ], axe_to_point[ 1 ] ), self.color )

class Dot( mod_main.CoordinateSystemElement ):

	# TODO

	pass

class Label( mod_main.CoordinateSystemElement ):

	# TODO

	pass

class Grid( mod_main.CoordinateSystemElement ):

	horizontal = None
	vertical = None
	color = None

	def __init__( self, horizontal, vertical, color = None, transparency_mask = None ):
		mod_main.CoordinateSystemElement.__init__( self, transparency_mask = transparency_mask )

		assert horizontal or vertical, 'Grid must have horizontal or vertical distance.'

		self.horizontal = float( horizontal ) if horizontal else None
		self.vertical = float( vertical ) if vertical else None
		self.color = color if color else mod_main.DEFAULT_GRID_COLOR

		#Bounds are not important for axes:
		#self.reload_bounds()
	
	def reload_bounds( self ):
		# not important
		pass

	def process_image( self, image, draw, bounds ):
		if self.vertical:
			axe_from_point = mod_utils.cartesius_to_image_coord( 0, bounds.bottom, bounds )
			axe_to_point = mod_utils.cartesius_to_image_coord( 0, bounds.top, bounds )
			i = mod_math.floor( bounds.left / self.vertical )
			while i < mod_math.ceil( bounds.right ):
				x, y = mod_utils.cartesius_to_image_coord( i, 0, bounds )
				if i != 0 and i != bounds.left and i != bounds.right:
					draw.line( ( x, axe_from_point[ 1 ], x, axe_to_point[ 1 ] ), self.get_color_with_transparency( self.color ) )
				i += self.vertical

		if self.horizontal:
			axe_from_point = mod_utils.cartesius_to_image_coord( bounds.left, 0, bounds )
			axe_to_point = mod_utils.cartesius_to_image_coord( bounds.right, 0, bounds )
			i = mod_math.floor( bounds.bottom / self.horizontal )
			while i < mod_math.ceil( bounds.top ):
				x, y = mod_utils.cartesius_to_image_coord( 0, i, bounds )
				if i != 0 and i != bounds.bottom and i != bounds.top:
					draw.line( ( axe_from_point[ 0 ], y, axe_to_point[ 0 ], y ), self.get_color_with_transparency( self.color ) )
				i += self.horizontal

class Line( mod_main.CoordinateSystemElement ):

	start = None
	end = None
	color = None

	def __init__( self, start, end, color = None, transparency_mask = None ):
		mod_main.CoordinateSystemElement.__init__( self, transparency_mask = transparency_mask )

		assert start
		assert len( start ) == 2
		assert end
		assert len( end ) == 2

		self.start = start
		self.end = end
		self.color = color if color else mod_main.DEFAULT_ELEMENT_COLOR

		self.reload_bounds()
	
	def reload_bounds( self ):
		self.bounds.update( point = self.start )
		self.bounds.update( point = self.end )

	def process_image( self, image, draw, bounds ):
		x1, y1 = mod_utils.cartesius_to_image_coord( x = self.start[ 0 ], y = self.start[ 1 ], bounds = bounds )
		x2, y2 = mod_utils.cartesius_to_image_coord( x = self.end[ 0 ], y = self.end[ 1 ], bounds = bounds )
		draw.line( ( x1, y1, x2, y2 ), self.get_color_with_transparency( self.color ) )

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
	
	def process_image( self, image, draw, bounds ):

		zero_point = mod_utils.cartesius_to_image_coord( 0, 0, bounds )
		for i, point in enumerate( self.points ):
			if i > 0:
				previous = self.points[ i - 1 ]
				x1, y1 = mod_utils.cartesius_to_image_coord( previous[ 0 ], previous[ 1 ], bounds )
				x2, y2 = mod_utils.cartesius_to_image_coord( point[ 0 ], point[ 1 ], bounds )
				if self.fill_color:
					draw.polygon(
						[ ( x1, zero_point[ 1 ] ), ( x1, y1 ), ( x2, y2 ), ( x2, zero_point[ 1 ] ) ], 
						fill = self.get_color_with_transparency( self.fill_color )
					)
					draw.line( ( x1, y1, x2, y2 ), self.get_color_with_transparency( self.color ) )
				else:
					draw.line( ( x1, y1, x2, y2 ), self.get_color_with_transparency( self.color ) )

class Circle( mod_main.CoordinateSystemElement ):

	x = None
	y = None
	radius = None
	color = None
	fill_color = None

	def __init__( self, x, y, radius, color = None, fill_color = None, transparency_mask = None ):
		mod_main.CoordinateSystemElement.__init__( self, transparency_mask = transparency_mask )

		assert x != None
		assert y != None
		assert radius > 0

		self.x = x
		self.y = y
		self.radius = radius

		self.color = color if color else DEFAULT_ELEMENT_COLOR
		self.fill_color = fill_color

		self.reload_bounds()
	
	def reload_bounds( self ):
		self.bounds.update( point = ( self.x + self.radius, self.y ) )
		self.bounds.update( point = ( self.x - self.radius, self.y ) )
		self.bounds.update( point = ( self.x, self.y + self.radius ) )
		self.bounds.update( point = ( self.x, self.y - self.radius ) )

	def process_image( self, image, draw, bounds ):
		x1, y1 = mod_utils.cartesius_to_image_coord(
				x = self.x - self.radius / 2.,
				y = self.y + self.radius / 2.,
				bounds = bounds )
		x2, y2 = mod_utils.cartesius_to_image_coord(
				x = self.x + self.radius / 2.,
				y = self.y - self.radius / 2.,
				bounds = bounds )

		draw.ellipse(
				( x1, y1, x2, y2 ),
				fill = self.get_color_with_transparency( self.fill_color ),
				outline = self.get_color_with_transparency( self.color ) )

class KeyValueGraph( mod_main.CoordinateSystemElement ):

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

	def process_image( self, image, draw, bounds ):
		assert self.items

		zero_point = mod_utils.cartesius_to_image_coord( 0, 0, bounds )

		for i, point in enumerate( self.items ):
			if i > 0:
				previous = self.items[ i - 1 ]
				x1, y1 = mod_utils.cartesius_to_image_coord( previous[ 0 ], previous[ 1 ], bounds )
				x2, y2 = mod_utils.cartesius_to_image_coord( point[ 0 ], point[ 1 ], bounds )
				if self.fill_color:
					draw.polygon(
						[ ( x1, zero_point[ 1 ] ), ( x1, y1 ), ( x2, y2 ), ( x2, zero_point[ 1 ] ) ], 
						fill = self.get_color_with_transparency( self.fill_color )
					)
					draw.line( ( x1, y1, x2, y2 ), self.get_color_with_transparency( self.color ) )
				else:
					draw.line( ( x1, y1, x2, y2 ), self.get_color_with_transparency( self.color ) )

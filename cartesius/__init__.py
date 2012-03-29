# -*- coding: utf-8 -*-

import pdb as mod_pdb
import logging as mod_logging
import math as mod_math

import Image as mod_image
import ImageDraw as mod_imagedraw
import ImageFont as mod_imagefont

DEFAULT_AXES_COLOR = ( 150, 150, 150 )
DEFAULT_LABEL_COLOR = ( 150, 150, 150 )
DEFAULT_GRID_COLOR = ( 235, 235, 235 )
DEFAULT_ELEMENT_COLOR = ( 0, 0, 0 )

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

def cartesisus_to_image_coord( x, y, bounds ):
	assert bounds.is_set()
	assert bounds.image_width
	assert bounds.image_height
	assert x != None
	assert y != None

	x = float( x )
	y = float( y )

	x_ratio = ( x - bounds.left ) / ( bounds.right - bounds.left )
	y_ratio = ( y - bounds.bottom ) / ( bounds.top - bounds.bottom )

	return ( x_ratio * bounds.image_width, bounds.image_height - y_ratio * bounds.image_height )

def min_max( *n ):
	#mod_logging.debug( 'n = {0}'.format( n ) )
	if not n:
		return None

	min_result = n[ 0 ]
	max_result = n[ 0 ]
	for i in n:
		if i != None:
			if min_result == None or i < min_result:
				min_result = i
			if max_result == None or i > max_result:
				max_result = i
				
	return min_result, max_result
			
class Bounds:
	""" Bounds for coordinate system and image size. """

	image_width = None
	image_height = None

	left = None
	right = None
	bottom = None
	top = None

	def __init__( self, left = None, right = None, bottom = None, top = None, image_width = None, image_height = None ):
		self.reset()

		self.left = left
		self.right = right
		self.bottom = bottom
		self.top = top

		if self.bottom != None and self.top != None:
			assert self.bottom < self.top, 'Bottom bound ({0}) greater than top bound ({1})'.format( self.bottom, self.top )
		if self.left != None and self.right != None:
			assert self.left < self.right, 'Left bound ({0}) greater than right bound ({1})'.format( self.left, self.right )

		self.image_width = image_width
		self.image_height = image_height

	def get_width_height( self ):
		assert self.left != None
		assert self.right != None
		assert self.bottom != None
		assert self.top != None
		assert self.right > self.left
		assert self.top > self.bottom

		return self.right - self.left, self.top - self.bottom

	def reset( self ):
		self.left_bound, self.right_bound, self.lower_bound, self.upper_bound = None, None, None, None

	def update_to_image_size( self ):
		assert self.image_width
		assert self.image_height

		width, height = self.get_width_height()

		desired_width_height_ratio = self.image_width / float( self.image_height )

		if desired_width_height_ratio < width / float( height ):
			desired_height = width / desired_width_height_ratio
			self.bottom = self.bottom - ( desired_height - height ) / 2
			self.top = self.top + ( desired_height - height ) / 2
		else:
			desired_width = height * desired_width_height_ratio
			self.left = self.left - ( desired_width - width ) / 2
			self.right = self.right + ( desired_width - width ) / 2

	def update( self, bounds = None, x = None, y = None, point = None ):
		if point != None:
			assert len( point ) == 2
			x = point[ 0 ]
			y = point[ 1 ]

		if x != None:
			self.left, self.right = min_max( x, self.left, self.right )
		if y != None:
			self.bottom, self.top = min_max( y, self.bottom, self.top )

		if bounds:
			self.update( x = bounds.left, y = bounds.top )
			self.update( x = bounds.right, y = bounds.bottom )

		if self.bottom != None and self.top != None:
			assert self.bottom <= self.top
		if self.left != None and self.right != None:
			assert self.left <= self.right

	def is_set( self ):
		return self.left != None and self.right != None and self.bottom != None and self.top != None

	def __str__( self ):
		return '[bounds:{0},{1},{2},{3}, image:{4},{5}]'.format( self.left, self.right, self.bottom, self.top, self.image_width, self.image_height )

class CoordinateSystem:

	elements = None

	bounds = None

	# x axis element:
	x_axis = None

	# y axis element:
	y_axis = None

	resize_bounds = None

	def __init__( self, bounds = None ):
		""" If custom bounds are given, they won't be resized according to new elements. """
		self.elements = []

		# Set default bounds
		if bounds:
			if isinstance( bounds, Bounds ):
				self.bounds = bounds
				self.resize_bounds = False
			else:
				assert len( bounds ) == 4, 'Bounds must be a 4 element tuple/list'
				self.bounds = Bounds( left = bounds[ 0 ], right = bounds[ 1 ], bottom = bounds[ 2 ], top = bounds[ 3 ] )
				self.resize_bounds = False
		else:
			self.bounds = Bounds()
			self.resize_bounds = True

		# By default, axes are on:
		self.x_axis = Axis( horizontal = True, points = 1 )
		self.y_axis = Axis( horizontal = False, points = 1 )

	def add( self, element ):
		"""
		Add element on coordinate system. Note that if you add an axis, it will remove a
		previous existing horizontal/vertical axis.
		"""
		assert element
		assert isinstance( element, CoordinateSystemElement )

		if isinstance( element, Axis ):
			if element.is_horizontal():
				self.x_axis = element
			else:
				self.y_axis = element
		else:
			element.reload_bounds()
			self.elements.append( element )
			self.reload_bounds()

	def reload_bounds( self ):
		if not self.resize_bounds:
			return

		if not self.elements:
			self.bounds.left = -1
			self.bounds.right = 1
			self.bounds.bottom = -1
			self.bounds.top = 1
			return

		for element in self.elements:
			self.bounds.update( element.bounds )

		assert self.bounds

	def __draw_elements( self, image, draw, hide_x_axis = False, hide_y_axis = False ):
		for element in self.elements:
			element.draw( image = image, draw = draw, bounds = self.bounds )

		if not hide_x_axis and self.x_axis:
			self.x_axis.draw( image = image, draw = draw, bounds = self.bounds )

		if not hide_y_axis and self.y_axis:
			self.y_axis.draw( image = image, draw = draw, bounds = self.bounds )

	def draw( self, width, height, axis_units_equal_length = True, hide_x_axis = False, hide_y_axis = False ):
		""" Returns a PIL image """

		self.bounds.image_width = width
		self.bounds.image_height = height

		if axis_units_equal_length:
			self.reload_bounds()

		image = mod_image.new( 'RGBA', ( width, height ), ( 255, 255, 255, 255 ) )
		draw = mod_imagedraw.Draw( image )

		if self.resize_bounds:
			self.bounds.update_to_image_size()

		self.__draw_elements( image = image, draw = draw, hide_x_axis = hide_x_axis, hide_y_axis = hide_y_axis )

		return image

class CoordinateSystemElement:
	""" Abstract class, every subclass should detect bounds and have the code to draw this item """

	bounds = None
	transparency_mask = None

	def __init__( self, transparency_mask = None ):
		self.bounds = Bounds()

		self.transparency_mask = transparency_mask if transparency_mask else 255

	def reload_bounds( self ):
		""" Will be called after the element is added to the coordinate system """
		raise Error( 'Not implemented in {0}'.format( self.__class__ ) )
	
	def process_image( self, image, draw, bounds ):
		""" Will be called after the element is added to the coordinate system """
		raise Error( 'Not implemented in {0}'.format( self.__class__ ) )

	def get_color_with_transparency( self, color ):
		""" Use this to get color with appropriate transparency taken from this element. """
		if not color:
			return None

		assert len( color ) >= 3

		return ( color[ 0 ], color[ 1 ], color[ 2 ], self.transparency_mask )

	def draw( self, image, draw, bounds ):
		if self.transparency_mask == 255:
			tmp_image, tmp_draw = image, draw
		else:
			tmp_image = mod_image.new( 'RGBA', ( bounds.image_width, bounds.image_height ) )
			tmp_draw = mod_imagedraw.Draw( tmp_image )

		self.process_image( tmp_image, tmp_draw, bounds )

		if tmp_image != image or tmp_draw != draw:
			image.paste( tmp_image, mask = tmp_image )

class Axis( CoordinateSystemElement ):

	horizontal = None
	color = None
	label_color = None

	# If set, draw label every:
	labels = None

	# If set, draw point every:
	points = None

	def __init__( self, horizontal, color = None, labels = None, label_color = None,
			label_position = None, points = None, transparency_mask = None ):
		CoordinateSystemElement.__init__( self, transparency_mask = transparency_mask )

		self.horizontal = horizontal
		self.color = color if color else DEFAULT_AXES_COLOR
		self.label_color = label_color if label_color else DEFAULT_LABEL_COLOR

		self.labels = float( labels ) if labels else None
		self.points = float( points ) if points else None

		if self.horizontal:
			self.label_position = label_position if label_position else LEFT_CENTER
		else:
			self.label_position = label_position if label_position else CENTER_DOWN

		assert len( self.label_position ) == 2

		#Bounds are not important for axes:
		#self.reload_bounds()
	
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

		return start, end

	def draw_dots( self, bounds, draw ):
		# TODO: Rename points!
		if not self.points:
			return

		if self.horizontal:
			dots_from, dots_to = self.get_start_end( self.points, bounds.bottom, bounds.top )
		else:
			dots_from, dots_to = self.get_start_end( self.points, bounds.left, bounds.right )

		i = dots_from
		while i <= dots_to:
			self.draw_dot( i, bounds, draw )
			i += self.points

	def draw_dot( self, i, bounds, draw ):
		if self.horizontal:
			x, y = cartesisus_to_image_coord( 0, i, bounds )
		else:
			x, y = cartesisus_to_image_coord( i, 0, bounds )

		draw.line( ( x - 2, y, x + 2, y ), DEFAULT_AXES_COLOR )
		draw.line( ( x, y + 2, x, y - 2 ), DEFAULT_AXES_COLOR )

	def draw_labels( self, bounds, draw ):
		# TODO: Rename labels!
		if not self.labels:
			return

		if self.horizontal:
			labels_from, labels_to = self.get_start_end( self.labels, bounds.bottom, bounds.top )
		else:
			labels_from, labels_to = self.get_start_end( self.labels, bounds.left, bounds.right )

		i = labels_from
		while i <= labels_to:
			self.draw_label( i, bounds, draw )
			i += self.labels

	def draw_label( self, i, bounds, draw ):
		if i == 0:
			return

		if i == int( i ):
			i = int( i )

		label = str( i )
		label_width, label_height = draw.textsize( label )

		x, y = self.get_point( i )
		x, y = cartesisus_to_image_coord( x, y, bounds )

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

		draw.text( ( x, y ), label, DEFAULT_LABEL_COLOR )

	def get_point( self, n ):
		if self.horizontal:
			return 0, n
		else:
			return n, 0

	def process_image( self, image, draw, bounds ):

		# TODO: Podijeliti na dio za crtanje točaka i dio za labele

		if self.horizontal:
			axe_from_point = cartesisus_to_image_coord( 0, bounds.bottom, bounds )
			axe_to_point = cartesisus_to_image_coord( 0, bounds.top, bounds )
		else:
			axe_from_point = cartesisus_to_image_coord( bounds.left, 0, bounds )
			axe_to_point = cartesisus_to_image_coord( bounds.right, 0, bounds )

		self.draw_dots( bounds, draw )
		self.draw_labels( bounds, draw )

		draw.line( ( axe_from_point[ 0 ], axe_from_point[ 1 ], axe_to_point[ 0 ], axe_to_point[ 1 ] ), self.color )

class Dot( CoordinateSystemElement ):

	# TODO

	pass

class Label( CoordinateSystemElement ):

	# TODO

	pass

class Grid( CoordinateSystemElement ):

	horizontal = None
	vertical = None
	color = None

	def __init__( self, horizontal, vertical, color = None, transparency_mask = None ):
		CoordinateSystemElement.__init__( self, transparency_mask = transparency_mask )

		assert horizontal or vertical, 'Grid must have horizontal or vertical distance.'

		self.horizontal = float( horizontal ) if horizontal else None
		self.vertical = float( vertical ) if vertical else None
		self.color = color if color else DEFAULT_GRID_COLOR

		#Bounds are not important for axes:
		#self.reload_bounds()
	
	def reload_bounds( self ):
		# not important
		pass

	def process_image( self, image, draw, bounds ):
		if self.vertical:
			axe_from_point = cartesisus_to_image_coord( 0, bounds.bottom, bounds )
			axe_to_point = cartesisus_to_image_coord( 0, bounds.top, bounds )
			i = mod_math.floor( bounds.left / self.vertical )
			while i < mod_math.ceil( bounds.right ):
				x, y = cartesisus_to_image_coord( i, 0, bounds )
				if i != 0 and i != bounds.left and i != bounds.right:
					draw.line( ( x, axe_from_point[ 1 ], x, axe_to_point[ 1 ] ), self.get_color_with_transparency( self.color ) )
				i += self.vertical

		if self.horizontal:
			axe_from_point = cartesisus_to_image_coord( bounds.left, 0, bounds )
			axe_to_point = cartesisus_to_image_coord( bounds.right, 0, bounds )
			i = mod_math.floor( bounds.bottom / self.horizontal )
			while i < mod_math.ceil( bounds.top ):
				x, y = cartesisus_to_image_coord( 0, i, bounds )
				if i != 0 and i != bounds.bottom and i != bounds.top:
					draw.line( ( axe_from_point[ 0 ], y, axe_to_point[ 0 ], y ), self.get_color_with_transparency( self.color ) )
				i += self.horizontal

class Line( CoordinateSystemElement ):

	start = None
	end = None
	color = None

	def __init__( self, start, end, color = None, transparency_mask = None ):
		CoordinateSystemElement.__init__( self, transparency_mask = transparency_mask )

		assert start
		assert len( start ) == 2
		assert end
		assert len( end ) == 2

		self.start = start
		self.end = end
		self.color = color if color else DEFAULT_ELEMENT_COLOR

		self.reload_bounds()
	
	def reload_bounds( self ):
		self.bounds.update( point = self.start )
		self.bounds.update( point = self.end )

	def process_image( self, image, draw, bounds ):
		x1, y1 = cartesisus_to_image_coord( x = self.start[ 0 ], y = self.start[ 1 ], bounds = bounds )
		x2, y2 = cartesisus_to_image_coord( x = self.end[ 0 ], y = self.end[ 1 ], bounds = bounds )
		draw.line( ( x1, y1, x2, y2 ), self.get_color_with_transparency( self.color ) )

class GraphFunction( CoordinateSystemElement ):

	function = None
	step = None
	start = None
	end = None
	points = None
	color = None
	fill_color = None

	def __init__( self, function, start = None, end = None, step = None, fill_color = False, color = None, transparency_mask = None ):
		CoordinateSystemElement.__init__( self, transparency_mask = transparency_mask )

		assert function

		self.function = function
		self.step = float( step if step else 0.1 )
		self.start = start if start != None else -1
		self.end = end if end != None else -1

		self.fill_color = fill_color
		self.color = color if color else DEFAULT_ELEMENT_COLOR

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

		zero_point = cartesisus_to_image_coord( 0, 0, bounds )
		for i, point in enumerate( self.points ):
			if i > 0:
				previous = self.points[ i - 1 ]
				x1, y1 = cartesisus_to_image_coord( previous[ 0 ], previous[ 1 ], bounds )
				x2, y2 = cartesisus_to_image_coord( point[ 0 ], point[ 1 ], bounds )
				if self.fill_color:
					draw.polygon(
						[ ( x1, zero_point[ 1 ] ), ( x1, y1 ), ( x2, y2 ), ( x2, zero_point[ 1 ] ) ], 
						fill = self.get_color_with_transparency( self.fill_color )
					)
					draw.line( ( x1, y1, x2, y2 ), self.get_color_with_transparency( self.color ) )
				else:
					draw.line( ( x1, y1, x2, y2 ), self.get_color_with_transparency( self.color ) )

class Circle( CoordinateSystemElement ):

	x = None
	y = None
	radius = None
	color = None
	fill_color = None

	def __init__( self, x, y, radius, color = None, fill_color = None, transparency_mask = None ):
		CoordinateSystemElement.__init__( self, transparency_mask = transparency_mask )

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
		x1, y1 = cartesisus_to_image_coord(
				x = self.x - self.radius / 2.,
				y = self.y + self.radius / 2.,
				bounds = bounds )
		x2, y2 = cartesisus_to_image_coord(
				x = self.x + self.radius / 2.,
				y = self.y - self.radius / 2.,
				bounds = bounds )

		draw.ellipse(
				( x1, y1, x2, y2 ),
				fill = self.get_color_with_transparency( self.fill_color ),
				outline = self.get_color_with_transparency( self.color ) )

class KeyValueGraph( CoordinateSystemElement ):

	color = None
	fill_color = None

	items = None

	def __init__( self, values, color = None, fill_color = False, transparency_mask = None ):
		CoordinateSystemElement.__init__( self, transparency_mask = transparency_mask )

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

		zero_point = cartesisus_to_image_coord( 0, 0, bounds )

		for i, point in enumerate( self.items ):
			if i > 0:
				previous = self.items[ i - 1 ]
				x1, y1 = cartesisus_to_image_coord( previous[ 0 ], previous[ 1 ], bounds )
				x2, y2 = cartesisus_to_image_coord( point[ 0 ], point[ 1 ], bounds )
				if self.fill_color:
					draw.polygon(
						[ ( x1, zero_point[ 1 ] ), ( x1, y1 ), ( x2, y2 ), ( x2, zero_point[ 1 ] ) ], 
						fill = self.get_color_with_transparency( self.fill_color )
					)
					draw.line( ( x1, y1, x2, y2 ), self.get_color_with_transparency( self.color ) )
				else:
					draw.line( ( x1, y1, x2, y2 ), self.get_color_with_transparency( self.color ) )

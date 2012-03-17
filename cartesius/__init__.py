# -*- coding: utf-8 -*-

import logging as mod_logging

import Image as mod_image
import ImageDraw as mod_imagedraw

def cartesisus_to_image_coord( x, y, bounds ):
	assert bounds.is_set()
	assert bounds.image_width
	assert bounds.image_height
	assert x != None
	assert y != None

	mod_logging.debug( 'x = {0}, y = {1}'.format( x, y ) )

	x = float( x )
	y = float( y )

	x_ratio = ( x - bounds.left ) / ( bounds.right - bounds.left )
	y_ratio = ( y - bounds.bottom ) / ( bounds.top - bounds.bottom )

	return ( x_ratio * bounds.image_width, bounds.image_height - y_ratio * bounds.image_height )

def min_max( *n ):
	mod_logging.debug( 'n = {0}'.format( n ) )
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

	def __init__( self ):
		self.elements = []

		# Set default bounds
		self.bounds = Bounds()

	def add( self, element ):
		assert element
		assert isinstance( element, CoordinateSystemElement )

		element.reload_bounds()
		self.elements.append( element )
		self.reload_bounds()

	def reload_bounds( self ):
		if not self.elements:
			self.bounds.left = -1
			self.bounds.right = 1
			self.bounds.bottom = -1
			self.bounds.top = 1
			return

		for element in self.elements:
			self.bounds.update( element.bounds )

		assert self.bounds

	def __draw_elements( self, draw ):
		for element in self.elements:
			element.draw( draw = draw, bounds = self.bounds )

	def __draw_axes( self, draw ):
		assert self.bounds

		x_axe_from_point = cartesisus_to_image_coord( 0, self.bounds.bottom, self.bounds )
		x_axe_to_point = cartesisus_to_image_coord( 0, self.bounds.top, self.bounds )
		y_axe_from_point = cartesisus_to_image_coord( self.bounds.left, 0, self.bounds )
		y_axe_to_point = cartesisus_to_image_coord( self.bounds.right, 0, self.bounds )

		mod_logging.debug( 'from {0},{1} to {2},{3}'.format( x_axe_from_point, x_axe_to_point, y_axe_from_point, y_axe_to_point ) )

		draw.line( ( x_axe_from_point[ 0 ], x_axe_from_point[ 1 ], x_axe_to_point[ 0 ], x_axe_to_point[ 1 ] ), ( 150, 150, 150, 255 ) )
		draw.line( ( y_axe_from_point[ 0 ], y_axe_from_point[ 1 ], y_axe_to_point[ 0 ], y_axe_to_point[ 1 ] ), ( 150, 150, 150, 255 ) )

		#draw.line( ( 200, 0, 200, 200 ), ( 2, 2, 2, 255 ) )

	def draw( self, width, height ):
		""" Returns a PIL image """

		self.bounds.image_width = width
		self.bounds.image_height = height

		self.reload_bounds()

		image = mod_image.new( 'RGBA', ( width, height ), ( 255, 255, 255, 255 ) )
		draw = mod_imagedraw.Draw( image )

		self.bounds.update_to_image_size()

		self.__draw_elements( draw )
		self.__draw_axes( draw )

		return image

class CoordinateSystemElement:
	""" Abstract class, every subclass should detect bounds and have the code to draw this item """

	bounds = None

	def __init__( self ):
		self.bounds = Bounds()

	def reload_bounds( self ):
		""" Will be called after the element is added to the coordinate system """
		raise Error( 'Not implemented in {0}'.format( self.__class__ ) )
	
	def draw( self, draw, bounds ):
		""" Note, bounds are coordinate system's bounds, not this element's bounds! """
		raise Error( 'Not implemented in {0}'.format( self.__class__ ) )

class Line( CoordinateSystemElement ):

	start = None
	end = None

	def __init__( self, start, end ):
		CoordinateSystemElement.__init__( self )

		assert start
		assert len( start ) == 2
		assert end
		assert len( end ) == 2

		self.start = start
		self.end = end

		self.reload_bounds()
	
	def reload_bounds( self ):
		self.bounds.update( point = self.start )
		self.bounds.update( point = self.end )

	def draw( self, draw, bounds ):
		x1, y1 = cartesisus_to_image_coord( x = self.start[ 0 ], y = self.start[ 1 ], bounds = bounds )
		x2, y2 = cartesisus_to_image_coord( x = self.end[ 0 ], y = self.end[ 1 ], bounds = bounds )
		draw.line( ( x1, y1, x2, y2 ), ( 0, 0, 255, 127 ) )

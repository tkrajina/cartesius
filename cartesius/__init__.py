# -*- coding: utf-8 -*-

import logging as mod_logging

import Image as mod_image
import ImageDraw as mod_imagedraw

def cartesisus_to_image_coord( x, y, bounds ):
	assert bounds
	assert bounds.image_width
	assert bounds.image_height
	assert x != None
	assert y != None

	mod_logging.debug( 'x = {0}, y = {1}'.format( x, y ) )

	x = float( x )
	y = float( y )

	x_ratio = ( x - bounds.left ) / ( bounds.right - bounds.left )
	y_ratio = ( y - bounds.bottom ) / ( bounds.top - bounds.bottom )

	return ( x_ratio * bounds.image_width, y_ratio * bounds.image_height )

def image_to_cartesisus_coord( x, y, bounds ):
	assert bounds
	assert bounds.image_width
	assert bounds.image_height
	assert x != None
	assert y != None

class Bounds:
	""" Bounds for coordinate system and image size. """

	image_width = None
	image_height = None

	left = None
	right = None
	bottom = None
	top = None

	def __init__( self ):
		self.reset()

	def reset( self ):
		self.left_bound, self.right_bound, self.lower_bound, self.upper_bound = None, None, None, None

	def update( self, bounds = None, left = None, right = None, top = None, bottom = None ):
		if self.left == None or ( left != None and left < self.left ):
			self.left = float( left )
		if self.right == None or ( right != None and right > self.right ):
			self.right = float( right )
		if self.bottom == None or ( bottom != None and bottom < self.bottom ):
			self.bottom = float( bottom )
		if self.top == None or ( top != None and top > self.top ):
			self.top = float( top )

		if bounds:
			self.update( left = bounds.left, right = bounds.right, bottom = bounds.bottom, top = bounds.top )

		assert self.bottom < self.top
		assert self.left < self.right

	def __bool__( self ):
		return self.left != None and self.right != None and self.bottom != None and self.top != None

	def __str__( self ):
		return '[bounds:{0},{1},{2},{3}, image:{4},{5}]'.format( self.bottom, self.top, self.left, self.right, self.image_width, self.image_height )

class CoordinateSystem:

	elements = None

	bounds = None

	def __init__( self ):
		self.elements = []

		# Set default bounds
		self.bounds = Bounds()

	def reload_bounds( self ):
		if not self.elements:
			self.bounds.left = -1
			self.bounds.right = 1
			self.bounds.bottom = -1
			self.bounds.top = 1
			return

		for element in self.elements:
			bounds.update( element.bounds )

		assert self.bounds

	def __draw_elements( self, draw ):
		pass

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

		self.__draw_elements( draw )
		self.__draw_axes( draw )

		return image

class CoordinateSystemElement:
	""" Abstract class, every subclass should detect bounds and have the code to draw this item """

	bounds = None

	def __init__( self ):
		self.bounds = Bounds()
	
	def draw():
		raise Error( 'Not implemented in {0}'.format( self.__class__ ) )

# -*- coding: utf-8 -*-

import logging as mod_logging
import cartesius as mod_cartesius
import math as mod_math

mod_logging.basicConfig( level = mod_logging.DEBUG, format = '%(asctime)s %(name)-12s %(levelname)-8s %(message)s' )


class Test:

	def test_001_lines( self ):
		"""Lines of different colors"""
		coordinate_system = mod_cartesius.CoordinateSystem()

		coordinate_system.add( mod_cartesius.Line( ( 0, 0 ), ( -.7, -.7 ) ) )
		coordinate_system.add( mod_cartesius.Line( ( .5, -.5 ), ( -.5, .5 ), color = ( 0, 255, 0 ) ) )
		coordinate_system.add( mod_cartesius.Line( ( 0, 0 ), ( 10, 1 ), color = ( 0, 0, 255 ) ) )

		return coordinate_system.draw( 600, 300, show_grid = True, show_labels = True )

	def test_002_function( self ):
		""" Function math.sin from -4 to 5"""
		coordinate_system = mod_cartesius.CoordinateSystem()

		f = lambda x : mod_math.sin( x ) * 2
		coordinate_system.add( mod_cartesius.GraphFunction( f, start = -4, end = 5, step = 0.02, color = ( 0, 0, 255 ) ) )

		return coordinate_system.draw( 600, 300, show_grid = False, show_labels = True )

	def test_003_filled_function( self ):
		""" Line function and normal function but with filled graph"""
		coordinate_system = mod_cartesius.CoordinateSystem()

		f = lambda x : mod_math.sin( x ) * 2
		coordinate_system.add( mod_cartesius.GraphFunction( f, start = -4, end = 5, step = 0.02, color = ( 0, 0, 255 ) ) )

		g = lambda x : mod_math.sin( x ) * 2
		coordinate_system.add( mod_cartesius.GraphFunction( g, start = 1, end = 4, step = 0.02, fill_color = ( 200, 255, 200 ) ) )

		return coordinate_system.draw( 600, 300, show_grid = False, show_labels = True )

	def test_004_filled_transparent_graphs( self ):
		coordinate_system = mod_cartesius.CoordinateSystem()

		coordinate_system.add(
				mod_cartesius.GraphFunction(
						mod_math.sin,
						start = -4,
						end = 5,
						step = 0.02,
						fill_color = ( 0, 0, 255 ),
						transparency_mask = 100 ) )

		coordinate_system.add(
				mod_cartesius.GraphFunction(
						mod_math.cos,
						start = -4,
						end = 5,
						step = 0.02,
						fill_color = ( 200, 255, 200 ),
						transparency_mask = 100 ) )

		return coordinate_system.draw( 600, 300, show_grid = True, show_labels = True )

	def test_005_key_value_graphs( self ):
		""" Key-value graphs"""
		coordinate_system = mod_cartesius.CoordinateSystem()

		# With dict:
		coordinate_system.add(
				mod_cartesius.KeyValueGraph(
						values = { -2: 1, 0: -1, 3: 1.2, 7: 1.2 },
						fill_color = ( 50, 50, 50 ),
						transparency_mask = 50 ) )
		# With pairs of tuples
		coordinate_system.add( 
				mod_cartesius.KeyValueGraph( 
						values = ( ( 0, 0 ), ( 1, -3 ), ( 10, 3 ) ),
						color = ( 255, 0, 0 ),
						transparency_mask = 150 ) )

		return coordinate_system.draw( 600, 300, show_grid = True, show_labels = True )

	def test_006_circles( self ):
		""" Key-value graphs"""
		coordinate_system = mod_cartesius.CoordinateSystem()

		coordinate_system.add(
			mod_cartesius.Circle(
				x = 4,
				y = -3,
				radius = 2,
				transparency_mask = 200,
				fill_color = ( 150, 150, 150 ),
				color = ( 0, 0, 0 ) ) )
		coordinate_system.add(
			mod_cartesius.Circle(
				x = 4,
				y = 3,
				radius = 2,
				transparency_mask = 200,
				color = ( 0, 0, 255 ) ) )

		return coordinate_system.draw( 600, 300, show_grid = True, show_labels = True )

	def test_007_circles_2( self ):
		""" Another example with circles """
		coordinate_system = mod_cartesius.CoordinateSystem()
		
		for i in range( 1, 20 ):
			x = i / 2.
			coordinate_system.add( mod_cartesius.Circle( x, y = mod_math.sin( x ), radius = mod_math.sqrt( x ), transparency_mask = 50, fill_color = ( i * 10, 2 * 10, i * 10 ), color = ( 0, 0, 0 ) ) )

		return coordinate_system.draw( 600, 300, show_grid = False, show_labels = True )

if __name__ == '__main__':
	html = """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
	<html>
	<head>

	<title>Cartesius examples</title>

	<style type="text/css"></style>

	</head>
	<body>"""

	test = Test()

	elements = dir( test )
	elements.sort()
	for method in elements:
		if method.startswith( 'test_' ):
			name = method.replace( 'test_', '' )

			method = getattr( test, method )
			description = method.__doc__
			image = method()
			image_name = '{0}.png'.format( name )
			image.save( image_name )

			html += '<h2>{0}:</h2>'.format( description )
			html += '<p><img src="{0}" /></p>'.format( image_name )

	html += '</body>'

	with open( 'index.html', 'w' ) as f:
		f.write( html )

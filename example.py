# -*- coding: utf-8 -*-

import logging as mod_logging
import cartesius as mod_cartesius
import math as mod_math
import os as mod_os
import sys as mod_sys

mod_logging.basicConfig( level = mod_logging.DEBUG, format = '%(asctime)s %(name)-12s %(levelname)-8s %(message)s' )

examples = []

def test_lines():
	"""Lines of different colors"""
	coordinate_system = mod_cartesius.CoordinateSystem()

	coordinate_system.add( mod_cartesius.Line( ( 0, 0 ), ( -.7, -.7 ) ) )
	coordinate_system.add( mod_cartesius.Line( ( .5, -.5 ), ( -.5, .5 ), color = ( 0, 255, 0 ) ) )
	coordinate_system.add( mod_cartesius.Line( ( 0, 0 ), ( 10, 1 ), color = ( 0, 0, 255 ) ) )

	return coordinate_system.draw( 600, 300 )

examples.append( test_lines )

def test_function():
	""" Function math.sin from -4 to 5"""
	coordinate_system = mod_cartesius.CoordinateSystem()

	f = lambda x : mod_math.sin( x ) * 2
	coordinate_system.add( mod_cartesius.GraphFunction( f, start = -4, end = 5, step = 0.02, color = ( 0, 0, 255 ) ) )

	return coordinate_system.draw( 600, 300 )

examples.append( test_function )

def test_function_with_custom_bounds():
	"""Same function, but with custom coordinate system bounds"""
	coordinate_system = mod_cartesius.CoordinateSystem( bounds = ( -32, 20, -3, 3 ))

	f = lambda x : mod_math.sin( x ) * 2
	coordinate_system.add( mod_cartesius.GraphFunction( f, start = -4, end = 5, step = 0.02, color = ( 0, 0, 255 ) ) )

	return coordinate_system.draw( 600, 300 )

examples.append( test_function_with_custom_bounds )

def test_filled_function():
	""" Line function and normal function but with filled graph"""
	coordinate_system = mod_cartesius.CoordinateSystem()

	f = lambda x : mod_math.sin( x ) * 2
	coordinate_system.add( mod_cartesius.GraphFunction( f, start = -4, end = 5, step = 0.02, color = ( 0, 0, 255 ) ) )

	g = lambda x : mod_math.sin( x ) * 2
	coordinate_system.add( mod_cartesius.GraphFunction( g, start = 1, end = 4, step = 0.02, fill_color = ( 200, 255, 200 ) ) )

	return coordinate_system.draw( 600, 300 )

examples.append( test_filled_function )

def test_filled_function():
	""" Previous example with grid behind graphs """
	coordinate_system = mod_cartesius.CoordinateSystem()

	# Grid:
	coordinate_system.add( mod_cartesius.Grid( 1, 1 ) )

	f = lambda x : mod_math.sin( x ) * 2
	coordinate_system.add( mod_cartesius.GraphFunction( f, start = -4, end = 5, step = 0.02, color = ( 0, 0, 255 ) ) )

	g = lambda x : mod_math.sin( x ) * 2
	coordinate_system.add( mod_cartesius.GraphFunction( g, start = 1, end = 4, step = 0.02, fill_color = ( 200, 255, 200 ) ) )

	return coordinate_system.draw( 600, 300 )

examples.append( test_filled_function )

def test_filled_transparent_graphs():
	""" Two functions """
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

	return coordinate_system.draw( 600, 300 )

examples.append( test_filled_transparent_graphs )

def test_filled_transparent_graphs_2():
	""" Two functions with transparend grid over it """
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

	coordinate_system.add( mod_cartesius.Grid( 1, 1, transparency_mask = 140 ) )

	return coordinate_system.draw( 600, 300 )

examples.append( test_filled_transparent_graphs_2 )

def test_key_value_graphs():
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

	return coordinate_system.draw( 600, 300 )

examples.append( test_key_value_graphs )

def test_circles():
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

	return coordinate_system.draw( 600, 300 )

examples.append( test_circles )

def test_circles_2():
	""" Another example with circles """
	coordinate_system = mod_cartesius.CoordinateSystem()
	
	for i in range( 1, 20 ):
		x = i / 2.
		coordinate_system.add( mod_cartesius.Circle( x, y = mod_math.sin( x ), radius = mod_math.sqrt( x ), transparency_mask = 50, fill_color = ( i * 10, 2 * 10, i * 10 ), color = ( 0, 0, 0 ) ) )

	return coordinate_system.draw( 600, 300 )

examples.append( test_circles_2 )

def test_circles_3():
	""" Circles with horizontal grid """
	coordinate_system = mod_cartesius.CoordinateSystem()
	
	coordinate_system.add( mod_cartesius.Grid( 1, None, transparency_mask = 200 ) )

	for i in range( 1, 20 ):
		x = i / 2.
		coordinate_system.add( mod_cartesius.Circle( x, y = mod_math.sin( x ), radius = mod_math.sqrt( x ), transparency_mask = 50, fill_color = ( i * 10, 2 * 10, i * 10 ), color = ( 0, 0, 0 ) ) )

	return coordinate_system.draw( 600, 300 )

examples.append( test_circles_3 )

def test_circles_4():
	""" Circles with horizontal grid every 2 """
	coordinate_system = mod_cartesius.CoordinateSystem()
	
	coordinate_system.add( mod_cartesius.Grid( 2, None, transparency_mask = 200 ) )

	for i in range( 1, 20 ):
		x = i / 2.
		coordinate_system.add( mod_cartesius.Circle( x, y = mod_math.sin( x ), radius = mod_math.sqrt( x ), transparency_mask = 50, fill_color = ( i * 10, 2 * 10, i * 10 ), color = ( 0, 0, 0 ) ) )

	return coordinate_system.draw( 600, 300 )

examples.append( test_circles_4 )

def test_circles_5():
	""" Circles with vertical grid every 0.5 """
	coordinate_system = mod_cartesius.CoordinateSystem()
	
	coordinate_system.add( mod_cartesius.Grid( None, 0.5, transparency_mask = 200 ) )

	for i in range( 1, 20 ):
		x = i / 2.
		coordinate_system.add( mod_cartesius.Circle( x, y = mod_math.sin( x ), radius = mod_math.sqrt( x ), transparency_mask = 50, fill_color = ( i * 10, 2 * 10, i * 10 ), color = ( 0, 0, 0 ) ) )

	return coordinate_system.draw( 600, 300 )

examples.append( test_circles_5 )

def test_axis_with_custom_labels():
	"""Axis with custom label positions, vertical axes has points every 0.25, horizontal every 1.0"""
	coordinate_system = mod_cartesius.CoordinateSystem()

	coordinate_system.add( mod_cartesius.Axis( horizontal = True, labels = 1, points = 0.25 ) )
	coordinate_system.add( mod_cartesius.Axis( horizontal = False, labels = 2, points = 1 ) )
	
	f = lambda x : mod_math.sin( x ) * 2
	coordinate_system.add( mod_cartesius.GraphFunction( f, start = -4, end = 5, step = 0.02, color = ( 0, 0, 255 ) ) )

	return coordinate_system.draw( 600, 300 )

examples.append( test_axis_with_custom_labels )

def test_with_two_horizontal_grids():
	"""Two horizontal grids"""
	coordinate_system = mod_cartesius.CoordinateSystem()

	coordinate_system.add( mod_cartesius.Grid( 0.25, None, color = ( 200, 200, 200 ) ) )
	coordinate_system.add( mod_cartesius.Grid( 1, None, color = ( 100, 100, 250 ) ) )

	f = lambda x : mod_math.sin( x ) * 2
	coordinate_system.add( mod_cartesius.GraphFunction( f, start = -4, end = 5, step = 0.02, color = ( 0, 0, 255 ) ) )

	return coordinate_system.draw( 600, 300 )

examples.append( test_with_two_horizontal_grids )

args = mod_sys.argv[ 1: ]

if args:
	filtered_examples = []
	for example in examples:
		if example.func_name in args and example.func_name not in filtered_examples:
			filtered_examples.append( example )
	examples = filtered_examples

html = """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>

<title>Cartesius examples</title>

<style type="text/css"></style>

</head>
<body>"""

try:
	mod_os.makedirs( 'examples' )
except:
	pass

for i, function in enumerate( examples ):
	description = function.__doc__.strip()
	image = function()
	image_name = 'graph-{0}.png'.format( i )
	image.save( 'examples/' + image_name )

	html += '<h2>{0}:</h2>'.format( description )
	html += '<p><img src="{0}" /></p>'.format( image_name )

	print 'written:', image_name

html += '</body>'

with open( 'examples/index.html', 'w' ) as f:
	f.write( html )

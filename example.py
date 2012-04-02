# -*- coding: utf-8 -*-

import logging as mod_logging
import inspect as mod_inspect
import math as mod_math
import random as mod_random
import os as mod_os
import sys as mod_sys

import cartesius as cartesius

mod_logging.basicConfig( level = mod_logging.DEBUG, format = '%(asctime)s %(name)-12s %(levelname)-8s %(message)s' )

examples = []

def test_lines():
	"""Lines of different colors"""
	coordinate_system = cartesius.CoordinateSystem()

	coordinate_system.add( cartesius.Line( ( 0, 0 ), ( -.7, -.7 ) ) )
	coordinate_system.add( cartesius.Line( ( .5, -.5 ), ( -.5, .5 ), color = ( 0, 255, 0 ) ) )
	coordinate_system.add( cartesius.Line( ( 0, 0 ), ( 10, 1 ), color = ( 0, 0, 255 ) ) )

	return coordinate_system.draw( 500, 250 )

examples.append( test_lines )

def test_function():
	""" Function math.sin from -4 to 5"""
	coordinate_system = cartesius.CoordinateSystem()

	f = lambda x : mod_math.sin( x ) * 2
	coordinate_system.add( cartesius.Function( f, start = -4, end = 5, step = 0.02, color = ( 0, 0, 255 ) ) )

	return coordinate_system.draw( 500, 250 )

examples.append( test_function )

def test_function_with_custom_bounds():
	"""Same function, but with custom coordinate system bounds"""
	coordinate_system = cartesius.CoordinateSystem( bounds = ( -32, 20, -3, 3 ))

	f = lambda x : mod_math.sin( x ) * 2
	coordinate_system.add( cartesius.Function( f, start = -4, end = 5, step = 0.02, color = ( 0, 0, 255 ) ) )

	return coordinate_system.draw( 500, 250 )

examples.append( test_function_with_custom_bounds )

def test_filled_function():
	""" Line function and normal function but with filled graph"""
	coordinate_system = cartesius.CoordinateSystem()

	f = lambda x : mod_math.sin( x ) * 2
	coordinate_system.add( cartesius.Function( f, start = -4, end = 5, step = 0.02, color = ( 0, 0, 255 ) ) )

	g = lambda x : mod_math.sin( x ) * 2
	coordinate_system.add( cartesius.Function( g, start = 1, end = 4, step = 0.02, fill_color = ( 200, 255, 200 ) ) )

	return coordinate_system.draw( 500, 250 )

examples.append( test_filled_function )

def test_filled_function():
	""" Previous example with grid behind graphs """
	coordinate_system = cartesius.CoordinateSystem()

	# Grid:
	coordinate_system.add( cartesius.Grid( 1, 1 ) )

	f = lambda x : mod_math.sin( x ) * 2
	coordinate_system.add( cartesius.Function( f, start = -4, end = 5, step = 0.02, color = ( 0, 0, 255 ) ) )

	g = lambda x : mod_math.sin( x ) * 2
	coordinate_system.add( cartesius.Function( g, start = 1, end = 4, step = 0.02, fill_color = ( 200, 255, 200 ) ) )

	return coordinate_system.draw( 500, 250 )

examples.append( test_filled_function )

def test_filled_transparent_graphs():
	""" Two functions """
	coordinate_system = cartesius.CoordinateSystem()

	coordinate_system.add(
			cartesius.Function(
					mod_math.sin,
					start = -4,
					end = 5,
					step = 0.02,
					fill_color = ( 0, 0, 255 ),
					transparency_mask = 100 ) )

	coordinate_system.add(
			cartesius.Function(
					mod_math.cos,
					start = -4,
					end = 5,
					step = 0.02,
					fill_color = ( 200, 255, 200 ),
					transparency_mask = 100 ) )

	return coordinate_system.draw( 500, 250 )

examples.append( test_filled_transparent_graphs )

def test_filled_transparent_graphs_2():
	""" Two functions with transparend grid over it """
	coordinate_system = cartesius.CoordinateSystem()

	coordinate_system.add(
			cartesius.Function(
					mod_math.sin,
					start = -4,
					end = 5,
					step = 0.02,
					fill_color = ( 0, 0, 255 ),
					transparency_mask = 100 ) )

	coordinate_system.add(
			cartesius.Function(
					mod_math.cos,
					start = -4,
					end = 5,
					step = 0.02,
					fill_color = ( 200, 255, 200 ),
					transparency_mask = 100 ) )

	coordinate_system.add( cartesius.Grid( 1, 1, transparency_mask = 140 ) )

	return coordinate_system.draw( 500, 250 )

examples.append( test_filled_transparent_graphs_2 )

def test_key_value_graphs():
	""" Key-value graphs"""
	coordinate_system = cartesius.CoordinateSystem()

	# With dict:
	coordinate_system.add(
			cartesius.KeyValueGraph(
					values = { -2: 1, 0: -1, 3: 1.2, 7: 1.2 },
					fill_color = ( 50, 50, 50 ),
					transparency_mask = 50 ) )

	# With pairs of tuples
	coordinate_system.add( 
			cartesius.KeyValueGraph( 
					values = ( ( 0, 0 ), ( 1, -3 ), ( 4, 3 ), ( 5, -2 ), ( 7, 0 ) ),
					color = ( 255, 0, 0 ),
					transparency_mask = 150 ) )

	return coordinate_system.draw( 500, 250 )

examples.append( test_key_value_graphs )

def test_circles():
	"""50 random circles"""
	coordinate_system = cartesius.CoordinateSystem()

	for i in range( 50 ):
		coordinate_system.add(
			cartesius.Circle(
				x = mod_random.randint( -20, 20 ),
				y = mod_random.randint( 0, 20 ),
				radius = mod_random.randint( 1, 5 ),
				transparency_mask = mod_random.randint( 0, 255 ),
				fill_color = ( mod_random.randint( 0, 255 ), mod_random.randint( 0, 255 ), mod_random.randint( 0, 255 ) ),
				color = ( mod_random.randint( 0, 255 ), mod_random.randint( 0, 255 ), mod_random.randint( 0, 255 ) ) ) )

	return coordinate_system.draw( 500, 250 )

examples.append( test_circles )

def test_circles_2():
	""" Another example with circles """
	coordinate_system = cartesius.CoordinateSystem()
	
	for i in range( 1, 20 ):
		x = i / 2.
		coordinate_system.add( cartesius.Circle( x, y = mod_math.sin( x ), radius = mod_math.sqrt( x ), transparency_mask = 50, fill_color = ( i * 10, 2 * 10, i * 10 ), color = ( 0, 0, 0 ) ) )

	return coordinate_system.draw( 500, 250 )

examples.append( test_circles_2 )

def test_circles_3():
	""" Circles with horizontal grid """
	coordinate_system = cartesius.CoordinateSystem()
	
	coordinate_system.add( cartesius.Grid( 1, None, transparency_mask = 200 ) )

	for i in range( 1, 20 ):
		x = i / 2.
		coordinate_system.add( cartesius.Circle( x, y = mod_math.sin( x ), radius = mod_math.sqrt( x ), transparency_mask = 50, fill_color = ( i * 10, 2 * 10, i * 10 ), color = ( 0, 0, 0 ) ) )

	return coordinate_system.draw( 500, 250 )

examples.append( test_circles_3 )

def test_circles_4():
	""" Circles with horizontal grid every 2 """
	coordinate_system = cartesius.CoordinateSystem()
	
	coordinate_system.add( cartesius.Grid( 2, None, transparency_mask = 200 ) )

	for i in range( 1, 20 ):
		x = i / 2.
		coordinate_system.add( cartesius.Circle( x, y = mod_math.sin( x ), radius = mod_math.sqrt( x ), transparency_mask = 50, fill_color = ( i * 10, 2 * 10, i * 10 ), color = ( 0, 0, 0 ) ) )

	return coordinate_system.draw( 500, 250 )

examples.append( test_circles_4 )

def test_circles_5():
	""" Circles with vertical grid every 0.5 """
	coordinate_system = cartesius.CoordinateSystem()
	
	coordinate_system.add( cartesius.Grid( None, 0.5, transparency_mask = 200 ) )

	for i in range( 1, 20 ):
		x = i / 2.
		coordinate_system.add( cartesius.Circle( x, y = mod_math.sin( x ), radius = mod_math.sqrt( x ), transparency_mask = 50, fill_color = ( i * 10, 2 * 10, i * 10 ), color = ( 0, 0, 0 ) ) )

	return coordinate_system.draw( 500, 250 )

examples.append( test_circles_5 )

def test_axis_with_custom_labels():
	"""Axis with custom label positions, vertical axes has points every 0.25, horizontal every 1.0"""
	coordinate_system = cartesius.CoordinateSystem()

	coordinate_system.add( cartesius.Axis( horizontal = True, labels = 1, points = 0.25 ) )
	coordinate_system.add( cartesius.Axis( horizontal = False, labels = 2, points = 1 ) )
	
	f = lambda x : mod_math.sin( x ) * 2
	coordinate_system.add( cartesius.Function( f, start = -4, end = 5, step = 0.02, color = ( 0, 0, 255 ) ) )

	return coordinate_system.draw( 500, 250 )

examples.append( test_axis_with_custom_labels )

def test_axis_custom_colors():
	"""Axis with custom colors"""
	coordinate_system = cartesius.CoordinateSystem()

	coordinate_system.add( cartesius.Axis( horizontal = True, color = ( 255, 0, 0 ), labels = 1, points = 0.25 ) )
	coordinate_system.add( cartesius.Axis( horizontal = False, color = ( 0, 255, 0 ), labels = 2, points = 1 ) )
	
	f = lambda x : x * mod_math.sin( x * x )
	coordinate_system.add( cartesius.Function( f, start = -4, end = 5, step = 0.02, color = ( 0, 0, 255 ) ) )

	return coordinate_system.draw( 500, 250 )

examples.append( test_axis_custom_colors )

def test_with_two_horizontal_grids():
	"""Two horizontal grids"""
	coordinate_system = cartesius.CoordinateSystem()

	coordinate_system.add( cartesius.Grid( 0.25, None, color = ( 200, 200, 200 ) ) )
	coordinate_system.add( cartesius.Grid( 1, None, color = ( 250, 50, 50 ) ) )

	f = lambda x : mod_math.sin( x ) * 2
	coordinate_system.add( cartesius.Function( f, start = -4, end = 5, step = 0.02, color = ( 0, 0, 255 ) ) )

	return coordinate_system.draw( 500, 250 )

examples.append( test_with_two_horizontal_grids )

def test_labels_positions():
	"""Labels on different positions"""
	result = []

	coordinate_system = cartesius.CoordinateSystem( bounds = ( -2.5, 2.5, -2.5, 2.5 ) )
	coordinate_system.add( cartesius.Axis( horizontal = True, points = 1, labels = 1, label_position = cartesius.LEFT_UP, ) )
	coordinate_system.add( cartesius.Axis( horizontal = False, points = 1, labels = 1, label_position = cartesius.LEFT_CENTER, ) )
	result.append( coordinate_system.draw( 150, 150 ) )

	coordinate_system = cartesius.CoordinateSystem( bounds = ( -2.5, 2.5, -2.5, 2.5 ) )
	coordinate_system.add( cartesius.Axis( horizontal = True, points = 1, labels = 1, label_position = cartesius.LEFT_DOWN, ) )
	coordinate_system.add( cartesius.Axis( horizontal = False, points = 1, labels = 1, label_position = cartesius.CENTER_UP, ) )
	result.append( coordinate_system.draw( 150, 150 ) )

	coordinate_system = cartesius.CoordinateSystem( bounds = ( -2.5, 2.5, -2.5, 2.5 ) )
	coordinate_system.add( cartesius.Axis( horizontal = True, points = 1, labels = 1, label_position = cartesius.CENTER, ) )
	coordinate_system.add( cartesius.Axis( horizontal = False, points = 1, labels = 1, label_position = cartesius.CENTER_DOWN, ) )
	result.append( coordinate_system.draw( 150, 150 ) )

	coordinate_system = cartesius.CoordinateSystem( bounds = ( -2.5, 2.5, -2.5, 2.5 ) )
	coordinate_system.add( cartesius.Axis( horizontal = True, points = 1, labels = 1, label_position = cartesius.RIGHT_UP, ) )
	coordinate_system.add( cartesius.Axis( horizontal = False, points = 1, labels = 1, label_position = cartesius.RIGHT_CENTER, ) )
	result.append( coordinate_system.draw( 150, 150 ) )

	coordinate_system = cartesius.CoordinateSystem( bounds = ( -2.5, 2.5, -2.5, 2.5 ) )
	coordinate_system.add( cartesius.Axis( horizontal = True, points = 1, labels = 1, label_position = cartesius.RIGHT_DOWN, ) )
	coordinate_system.add( cartesius.Axis( horizontal = False, points = 1, labels = 1, label_position = cartesius.RIGHT_DOWN, ) )
	result.append( coordinate_system.draw( 150, 150 ) )

	return result

examples.append( test_labels_positions )

def test_hide_axis():
	"""Test with hidden axis"""
	result = []

	coordinate_system = cartesius.CoordinateSystem( bounds = ( -2.5, 2.5, -2.5, 2.5 ) )
	f = lambda x : x * mod_math.sin( x * x )
	coordinate_system.add( cartesius.Function( f, start = -4, end = 5, step = 0.02, color = ( 0, 0, 255 ) ) )

	result.append( coordinate_system.draw( 150, 150, hide_y_axis = True ) )
	result.append( coordinate_system.draw( 150, 150, hide_x_axis = True ) )

	return result

examples.append( test_hide_axis )

def test_hide_axis_positive_or_negative_parts():
	"""Hide positive and/or negative parts of axes"""
	result = []

	coordinate_system = cartesius.CoordinateSystem( bounds = ( -2.5, 2.5, -2.5, 2.5 ) )
	coordinate_system.add( cartesius.Function( lambda x : x * mod_math.sin( x * x ), start = -4, end = 5, step = 0.02, color = ( 0, 0, 255 ) ) )
	coordinate_system.add( cartesius.Axis( horizontal = True, hide_positive = True ) )
	coordinate_system.add( cartesius.Axis( horizontal = False, hide_positive = True ) )
	result.append( coordinate_system.draw( 150, 150 ) )

	coordinate_system = cartesius.CoordinateSystem( bounds = ( -2.5, 2.5, -2.5, 2.5 ) )
	coordinate_system.add( cartesius.Function( lambda x : x * mod_math.sin( x * x ), start = -4, end = 5, step = 0.02, color = ( 0, 0, 255 ) ) )
	coordinate_system.add( cartesius.Axis( horizontal = True, hide_negative = True ) )
	coordinate_system.add( cartesius.Axis( horizontal = False, hide_negative = True ) )
	result.append( coordinate_system.draw( 150, 150 ) )

	return result

examples.append( test_hide_axis_positive_or_negative_parts )

def test_detached_axes():
	"""Detached axes"""
	coordinate_system = cartesius.CoordinateSystem( bounds = ( -2.5, 2.5, -2.5, 2.5 ) )

	coordinate_system.add( cartesius.Function( lambda x : x * mod_math.sin( x * x ), start = -4, end = 5, step = 0.02, color = ( 0, 0, 255 ) ) )
	coordinate_system.add( cartesius.Axis( horizontal = True ) )
	coordinate_system.add( cartesius.Axis( horizontal = False, hide = True ) )

	return coordinate_system.draw( 500, 250 )

examples.append( test_detached_axes )

if __name__ == '__main__':
	args = mod_sys.argv[ 1: ]

	if args:
		filtered_examples = []
		for example in examples:
			if example.func_name in args and example.func_name not in filtered_examples:
				filtered_examples.append( example )
		examples = filtered_examples

	def clean_source_lines( function ):
		source_lines = mod_inspect.getsourcelines( function )[ 0 ]
		source_started = False
		result = ''

		for line in source_lines:
			if line.strip().endswith( '"""' ):
				source_started = True
			elif source_started:
				if not line.strip().startswith( 'return' ):
					result += line[ 1: ]

		return result

	html = """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
	<html>
	<head>

	<title>Cartesius examples</title>

	<style type="text/css"></style>

	</head>
	<body>
	<h1>Cartesius</h1>
	<p>
	Cartesius is a small library for drawing 2d coordinate system images.
	More on <a href='http://github.com/tkrajina/cartesius'>http://github.com/tkrajina/cartesius</a>
	</p>"""

	for i, function in enumerate( examples ):
		description = function.__doc__.strip()
		images = function()

		if not isinstance( images, list ):
			images = [ images ]	

		html += '<h2>{0}:</h2>'.format( description )

		html += '<p>'
		for j, image in enumerate( images ):
			image_name = 'graph-{0}-{1}.png'.format( i, j )
			image.save( image_name )
			print 'written:', image_name
			html += '<img src="{0}" style="border: 1px solid #f0f0f0;padding:5px;margin:5px;" /> '.format( image_name )
		html += '</p>'

		html += '<p>Code:</p>'
		html += '<pre style="font-size:0.8em;border-style:solid;border-color:gray;border-width:0px 0px 0px 1px;margin:2px 2px 10px 2px;padding:2px 2px 2px 10px;">' + clean_source_lines( function ) + '</pre>'

	html += '</body>'

	with open( 'index.html', 'w' ) as f:
		f.write( html )

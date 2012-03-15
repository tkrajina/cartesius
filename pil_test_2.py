# -*- coding: utf-8 -*-

import math as mod_math
import Image as mod_image
import ImageDraw as mod_imagedraw

width = 800
height = 400

background = mod_image.new( 'RGBA', ( width, height ), ( 255, 255, 255, 255 ) )

draw = mod_imagedraw.Draw( background )

for i in range( width ):
	sin_value = 200 + 200 * mod_math.sin( i / 280. * mod_math.pi )
	draw.line( ( i, 0, i, sin_value ), ( 0, 0, 255, 127 ) )

"""
draw.polygon(
	[ ( 0, 0 ), ( 100, 100 ), ( 200, 100 ) ]
	, fill = ( 255, 0, 255, 127 )
#	, outline = ( 255, 255, 255, 255 )
)
"""

background.show()

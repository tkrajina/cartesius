# -*- coding: utf-8 -*-

import logging as mod_logging
import cartesius as mod_cartesius
import math as mod_math

mod_logging.basicConfig( level = mod_logging.DEBUG, format = '%(asctime)s %(name)-12s %(levelname)-8s %(message)s' )

coordinate_system = mod_cartesius.CoordinateSystem()

coordinate_system.add( mod_cartesius.Line( ( 0, 0 ), ( -.7, -.7 ) ) )
coordinate_system.add( mod_cartesius.Line( ( .5, -.5 ), ( -.5, .5 ) ) )
coordinate_system.add( mod_cartesius.Line( ( 0, 0 ), ( 10, 1 ), color = ( 0, 0, 255 ) ) )

f = lambda x : mod_math.sin( x ) * 2
coordinate_system.add( mod_cartesius.GraphFunction( f, start = 2, end = 12, step = 0.02, fill_color = ( 100, 100, 100 ), color = ( 0, 0, 0 ), transparency_mask = 255 ) )

g = lambda x : mod_math.cos( x ) * 1.5 
coordinate_system.add( mod_cartesius.GraphFunction( g, start = -1.5, end = 11, step = 0.02, fill_color = ( 0, 200, 0 ), color = ( 255, 0, 0, 125 ), transparency_mask = 100 ) )

h = lambda x : ( x - 3 ) ** 2 / 50 - 3
coordinate_system.add( mod_cartesius.GraphFunction( h, start = 1.5, end = 11, step = 0.02, fill_color = ( 0, 0, 200 ), color = ( 255, 0, 0, 125 ), transparency_mask = 100 ) )

"""
k = lambda x : mod_math.sin( x * 4. ) * 2
coordinate_system.add( mod_cartesius.GraphFunction( k, start = -1.5, end = 11, step = 0.02, fill_color = ( 200, 0, 0 ), color = ( 255, 0, 0, 125 ), transparency_mask = 100 ) )
"""

coordinate_system.add( mod_cartesius.Circle( x = 4, y = -3, radius = 2, transparency_mask = 50, color = ( 0, 0, 0 ) ) )

image = coordinate_system.draw( 1200, 500 )

image.show()

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
coordinate_system.add( mod_cartesius.GraphFunction( g, start = 1.5, end = 11, step = 0.02, fill_color = ( 0, 200, 0 ), color = ( 255, 0, 0, 125 ), transparency_mask = 100 ) )

image = coordinate_system.draw( 1200, 500 )

image.show()

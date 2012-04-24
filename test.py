# -*- coding: utf-8 -*-

# Copyright 2011 Tomo Krajina
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging as mod_logging
import unittest as mod_unittest
import cartesius as mod_cartesius

mod_logging.basicConfig( level = mod_logging.DEBUG, format = '%(asctime)s %(name)-12s %(levelname)-8s %(message)s' )

class Tests( mod_unittest.TestCase ):
    """ Tests only for simple functionalities, not the image creation """

    """ TODO
    def test_conversion( self ):
        bounds = mod_cartesius.Bounds( left = -1, right = 1, top = 1, bottom = -1, image_width = 100, image_height = 100 )
        x, y = mod_cartesius.cartesisus_to_image_coord( 0.5, 0.5, bounds )

        self.assertEquals( x, 75 )
        self.assertEquals( y, 75 )

        x, y = mod_cartesius.cartesisus_to_image_coord( -0.5, 0, bounds )

        self.assertEquals( x, 25 )
        self.assertEquals( y, 50 )
        """

    def test_min_max( self ):
        min_value, max_value = mod_cartesius.min_max( None, 3 )

        self.assertEquals( min_value, 3 )
        self.assertEquals( max_value, 3 )

        min_value, max_value = mod_cartesius.min_max( 1, None, 3 )

        self.assertEquals( min_value, 1 )
        self.assertEquals( max_value, 3 )

        min_value, max_value = mod_cartesius.min_max( None, 1, 1.5, 3 )

        self.assertEquals( min_value, 1 )
        self.assertEquals( max_value, 3 )

    def test_bounds_reset( self ):
        bounds = mod_cartesius.Bounds()

        self.assertFalse( bounds.is_set() )

        bounds.left = 1
        self.assertFalse( bounds.is_set() )

        bounds.right = 1
        self.assertFalse( bounds.is_set() )

        bounds.bottom = 1
        self.assertFalse( bounds.is_set() )

        bounds.top = 1
        self.assertTrue( bounds.is_set() )

    def test_bounds_width_point( self ):
        bounds = mod_cartesius.Bounds()

        self.assertFalse( bounds.is_set() )

        bounds.update( point = ( 2, 17 ) )
        self.assertEquals( bounds.left, 2 )
        self.assertEquals( bounds.right, 2 )
        self.assertEquals( bounds.bottom, 17 )
        self.assertEquals( bounds.top, 17 )

        bounds.update( point = ( -1, -1 ) )
        self.assertEquals( bounds.left, -1 )
        self.assertEquals( bounds.right, 2 )
        self.assertEquals( bounds.bottom, -1 )
        self.assertEquals( bounds.top, 17 )

    def test_bounds_width_xy( self ):
        bounds = mod_cartesius.Bounds()

        self.assertFalse( bounds.is_set() )

        bounds.update( x = 2 )
        self.assertEquals( bounds.left, 2 )
        self.assertEquals( bounds.right, 2 )

        bounds.update( x = -1 )
        self.assertEquals( bounds.left, -1 )
        self.assertEquals( bounds.right, 2 )

        bounds.update( x = 100 )
        self.assertEquals( bounds.left, -1 )
        self.assertEquals( bounds.right, 100 )

        bounds.update( y = 2 )
        self.assertEquals( bounds.bottom, 2 )
        self.assertEquals( bounds.top, 2 )

        bounds.update( y = -1 )
        self.assertEquals( bounds.bottom, -1 )
        self.assertEquals( bounds.top, 2 )

        bounds.update( y = 100 )
        self.assertEquals( bounds.bottom, -1 )
        self.assertEquals( bounds.top, 100 )

    def test_bounds_update_to_image_size_1( self ):
        bounds = mod_cartesius.Bounds( left = -1, right = 1, bottom = -2, top = 2, image_width = 100, image_height = 100 )

        bounds.update_to_image_size()

        self.assertEquals( bounds.left, -2 )
        self.assertEquals( bounds.right, 2 )
        self.assertEquals( bounds.bottom, -2 )
        self.assertEquals( bounds.top, 2 )

    def test_bounds_update_to_image_size_2( self ):
        bounds = mod_cartesius.Bounds( left = -1, right = 1, bottom = -1, top = 1, image_width = 400, image_height = 100 )

        bounds.update_to_image_size()

        self.assertEquals( bounds.left, -4 )
        self.assertEquals( bounds.right, 4 )
        self.assertEquals( bounds.bottom, -1 )
        self.assertEquals( bounds.top, 1 )

    def test_line_bounds( self ):
        line = mod_cartesius.Line( ( 1, 2 ), ( -5, 4 ) )

        self.assertTrue( line.bounds )
        self.assertEquals( line.bounds.left, -5 )
        self.assertEquals( line.bounds.right, 1 )
        self.assertEquals( line.bounds.bottom, 2 )
        self.assertEquals( line.bounds.top, 4 )

if __name__ == '__main__':
    mod_unittest.main()

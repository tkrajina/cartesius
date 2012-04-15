# -*- coding: utf-8 -*-

""" Charts are normal CoordinateSystemElements """

import main as mod_main

class MyElement:

	def __init__( self, data = None, transparency_mask = None ):
		mod_main.CoordinateSystemElement.__init__( self, transparency_mask = transparency_mask )

		assert data, 'Data must be set'

		self.reload_bounds()

	def reload_bounds( self ):
		pass
	
	def process_image( self, draw_handler ):
		pass

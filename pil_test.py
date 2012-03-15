import Image as mod_image
import ImageDraw as mod_imagedraw

background = mod_image.new( 'RGBA', ( 512,512 ), ( 255,0,0,0 ) )

poly = mod_image.new( 'RGBA', ( 512,512 ) )
poly_draw = mod_imagedraw.Draw( poly )
poly_draw.polygon(
	[ ( 128,128 ), ( 384, 384 ), ( 128, 384 ), ( 384, 128 ) ]
	, fill = ( 255,255,255,127 )
#	, outline = ( 255, 255, 255, 255 )
)
background.paste( poly, mask = poly )

poly = mod_image.new( 'RGBA', ( 512,512 ) )
poly_draw = mod_imagedraw.Draw( poly )
poly_draw.polygon(
	[ ( 100,100 ), ( 384, 384 ), ( 100, 384 ), ( 384, 100 ) ]
	, fill = ( 255,255,255,127 )
#	, outline = ( 255, 255, 255, 255 )
)
background.paste( poly, mask = poly )

background.show()

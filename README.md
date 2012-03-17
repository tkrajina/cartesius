Cartesius:
==========

Cartesius is an simple library for drawing things (graphs, histograms) in the cartesian coordinate system. It depends only on PIL.

    import cartesius
    
    coordinate_system = cartesius.CoordinateSystem()
    
    # Monocolor FilledGraph:
    filled_graph = cartesius.FilledGraph( color = ( 0, 0, 1 ) )
    filled_graph.add_point( ( 0, 2 ) )
    filled_graph.add_point( ( 1, 5 ) )
    filled_graph.add_point( ( 5.3, 3.7 ) )
    coordinate_system.add( filled_graph )
    
    # Multicolor filled graph:
    filled_graph = cartesius.FilledGraph()
    filled_graph.add_point( ( 0, 2 ), color = ( 1, 0, 0 ) )
    filled_graph.add_point( ( 1, 5 ), color = ( 0, 1, 0 ) )
    filled_graph.add_point( ( 5.3, 3.7 ), color = ( 0, 0, 1 ) )
    coordinate_system.add( filled_graph )
    
    # Circle:
    circle = cartesius.Circle( ( 2, 3.4 ), radius = 2 )
    coordinate_system.add( circle )
    
    # Icon:
    icon = cartesius.Icon( x = 3, image = 'icon.png', line_color = ( 0.3, 0.3, 0.3 ) )
    coordinate_system.add( icon )
    
    # Function graph
    def f( x ):return x ** 2 - 5
    graph_function = cartesius.GraphFunction( function = f, steps = 0.2, from = 2, to = 10 )
    coordinate_system.add( graph_function )
    
    # Line:
    line = cartesius.Line( ( 2, 3 ), ( 5, 5.3 ) )
    coordinate_system.add( line )
    
    # By default, the CoordinateSystem will detect the lower/upper/left/right bounds, but you can force yours with:
    coordinate_system.set_lower_bound( 0 )
    coordinate_system.set_left_bound( 0 )

	# Draw:
	coordinate_system.draw()

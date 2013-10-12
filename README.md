# Cartesius

Cartesius is a library for drawing 2d coordinate system images.

Note, all examples come in two versions: normal and antialiased. Antialiased can be created ba adding <tt>antialiasing = True</tt> in <tt>CoordinateSystem.draw()</tt> but are more CPU intensive to create.

## 50 random circles

![graph-0-0.png](http://tkrajina.github.io/cartesius/graph-0-0.png)&nbsp;![graph-0-1.png](http://tkrajina.github.io/cartesius/graph-0-1.png)&nbsp;

Code:

    import cartesius.main as cartesius
    import cartesius.elements as elements
    import cartesius.charts as charts

    coordinate_system = cartesius.CoordinateSystem()
    
    for i in range(50):
        center = (random.randint(-20, 20), random.randint(0, 20))
        coordinate_system.add(
            elements.Circle(
                center,
                radius = random.randint(1, 5),
                transparency_mask = random.randint(0, 255),
                fill_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
                color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))))
    
## PieChart with default colors

![graph-1-0.png](http://tkrajina.github.io/cartesius/graph-1-0.png)&nbsp;![graph-1-1.png](http://tkrajina.github.io/cartesius/graph-1-1.png)&nbsp;

Code:

    import cartesius.main as cartesius
    import cartesius.elements as elements
    import cartesius.charts as charts

    coordinate_system = cartesius.CoordinateSystem()
    
    # list or tuple of two-element tuples (value, label):
    piechart_data = (
        charts.data('abc', 1),
        charts.data('cde', 2),
        charts.data('efg', 4),
        charts.data('ijk', 1),
        charts.data('lmn', 5),
        charts.data('opq', 5),
        charts.data('xyz', 3),
    )
    piechart = charts.PieChart(data=piechart_data, color=(0, 0, 0))
    coordinate_system.add(piechart)
    
    # No need for axes:
    coordinate_system.add(elements.Axis(horizontal=True, hide=True))
    coordinate_system.add(elements.Axis(vertical=True, hide=True))
    
## PieChart with custom colors

![graph-2-0.png](http://tkrajina.github.io/cartesius/graph-2-0.png)&nbsp;![graph-2-1.png](http://tkrajina.github.io/cartesius/graph-2-1.png)&nbsp;

Code:

    import cartesius.main as cartesius
    import cartesius.elements as elements
    import cartesius.charts as charts

    coordinate_system = cartesius.CoordinateSystem()
    
    piechart_data = (
        charts.data('abc', 1, fill_color=(255, 200, 200)),
        charts.data('cde', 2, fill_color=(200, 255, 200)),
        charts.data('efg', 5, fill_color=(200, 200, 255)),
        charts.data('ijk', 3, fill_color=(255, 255, 255)),
    )
    piechart = charts.PieChart(data=piechart_data, color=(0, 0, 0))
    
    coordinate_system.add(piechart)
    
    # No need for axes:
    coordinate_system.add(elements.Axis(horizontal=True, hide=True))
    coordinate_system.add(elements.Axis(vertical=True, hide=True))
    
## Bar charts with same column width. One with default and the other with custom colors

![graph-3-0.png](http://tkrajina.github.io/cartesius/graph-3-0.png)&nbsp;![graph-3-1.png](http://tkrajina.github.io/cartesius/graph-3-1.png)&nbsp;

Code:

    import cartesius.main as cartesius
    import cartesius.elements as elements
    import cartesius.charts as charts

    coordinate_system = cartesius.CoordinateSystem()
    
    barchart_data_1 = (
            charts.data(-1, -.5),
            charts.data(0, .7),
            charts.data(1, 2),
            charts.data(2, 2.7),
            charts.data(3, 4),
            charts.data(4, 3.1),
            charts.data(5, 2.1),
            charts.data(6, 1),
            charts.data(7, -.3)
    )
    barchart_1 = charts.BarChart(vertical=True, data=barchart_data_1, width=0.95)
    coordinate_system.add(barchart_1)
    
    custom_color = (100, 100, 200)
    
    barchart_data_2 = (
            charts.data(-1, -.25, fill_color=custom_color),
            charts.data(0, .35, fill_color=custom_color),
            charts.data(1, 1, fill_color=custom_color),
            charts.data(2, 1.35, fill_color=custom_color),
            charts.data(3, 2, fill_color=custom_color),
            charts.data(4, 1.65, fill_color=custom_color),
            charts.data(5, 1, fill_color=custom_color),
            charts.data(6, .5, fill_color=custom_color),
            charts.data(7, -.6, fill_color=custom_color)
    )
    barchart_2 = charts.BarChart(vertical=True, data=barchart_data_2, width=0.75, color=(0, 0, 0))
    coordinate_system.add(barchart_2)
    
## BarChart with different column widths

![graph-4-0.png](http://tkrajina.github.io/cartesius/graph-4-0.png)&nbsp;![graph-4-1.png](http://tkrajina.github.io/cartesius/graph-4-1.png)&nbsp;

Code:

    import cartesius.main as cartesius
    import cartesius.elements as elements
    import cartesius.charts as charts

    coordinate_system = cartesius.CoordinateSystem()
    
    barchart_data = (
            charts.data(-5, -0, -.5, label='Negative value'),
            charts.data(0, 1, size=.7),
            charts.data(1, 3, size=2),
            charts.data(3, 4, size=4, label='#1'),
            charts.data(4, 5.5, size=3.1),
            charts.data(6, 7, size=2.1),
            charts.data(7, 9, size=1),
    )
    barchart = charts.BarChart(vertical=True, data=barchart_data, color=(0, 0, 0))
    coordinate_system.add(barchart)
    
## Horizontal bar charts

![graph-5-0.png](http://tkrajina.github.io/cartesius/graph-5-0.png)&nbsp;![graph-5-1.png](http://tkrajina.github.io/cartesius/graph-5-1.png)&nbsp;

Code:

    import cartesius.main as cartesius
    import cartesius.elements as elements
    import cartesius.charts as charts

    coordinate_system = cartesius.CoordinateSystem()
    
    barchart_data_1 = (
            charts.data(-1, -.5, label='a'),
            charts.data(0, .7, label='b'),
            charts.data(1, 2, label='c'),
            charts.data(2, 2.7, label='d'),
            charts.data(3, 4, label='Maximum value'),
            charts.data(4, 3.1, label='f'),
            charts.data(5, 2.1, label='g'),
            charts.data(6, 1, label='h'),
            charts.data(7, -.3, label='The end!')
    )
    barchart_1 = charts.BarChart(horizontal=True, data=barchart_data_1, width=0.95)
    coordinate_system.add(barchart_1)
    
    custom_color = (100, 100, 200)
    
    barchart_data_2 = (
            charts.data(-1, -.25, fill_color=custom_color),
            charts.data(0, .35, fill_color=custom_color),
            charts.data(1, 1, fill_color=custom_color),
            charts.data(2, 1.35, fill_color=custom_color),
            charts.data(3, 2, fill_color=custom_color),
            charts.data(4, 1.65, fill_color=custom_color),
            charts.data(5, 1, fill_color=custom_color),
            charts.data(6, .5, fill_color=custom_color),
            charts.data(7, -.6, fill_color=custom_color)
    )
    barchart_2 = charts.BarChart(horizontal=True, data=barchart_data_2, width=0.75, color=(0, 0, 0))
    coordinate_system.add(barchart_2)
    
## Bar charts with data given as generator function

![graph-6-0.png](http://tkrajina.github.io/cartesius/graph-6-0.png)&nbsp;![graph-6-1.png](http://tkrajina.github.io/cartesius/graph-6-1.png)&nbsp;

Code:

    import cartesius.main as cartesius
    import cartesius.elements as elements
    import cartesius.charts as charts

    import cartesius.colors as colors
    
    coordinate_system = cartesius.CoordinateSystem()
    
    bottom_collor = (0, 0, 255)
    top_color = (255, 255, 255)
    
    # In case you don't want to keep all your data in memory, you can give the data as a
    # generator function that will lazy-load your data. This works for all charts:
    def data_generator():
        for x in range(25):
            key = x / 2.
            value = 2 * math.sin(x/4.)
            color = colors.get_color_between(bottom_collor, top_color, (value + 2) / 4.)
            yield charts.data(key, value, fill_color=color)
    
    barchart_data_generator = data_generator
    barchart = charts.BarChart(data=barchart_data_generator, vertical=True, width=0.5)
    coordinate_system.add(barchart)
    
## Function math.sin from -4 to 5

![graph-7-0.png](http://tkrajina.github.io/cartesius/graph-7-0.png)&nbsp;![graph-7-1.png](http://tkrajina.github.io/cartesius/graph-7-1.png)&nbsp;

Code:

    import cartesius.main as cartesius
    import cartesius.elements as elements
    import cartesius.charts as charts

    coordinate_system = cartesius.CoordinateSystem()
    
    f = lambda x : math.sin(x) * 2
    coordinate_system.add(charts.Function(f, start=-4, end=5, step=0.02, color=0x0000ff))
    
## Same function, but with custom coordinate system bounds

![graph-8-0.png](http://tkrajina.github.io/cartesius/graph-8-0.png)&nbsp;![graph-8-1.png](http://tkrajina.github.io/cartesius/graph-8-1.png)&nbsp;

Code:

    import cartesius.main as cartesius
    import cartesius.elements as elements
    import cartesius.charts as charts

    coordinate_system = cartesius.CoordinateSystem(bounds=(-32, 20, -3, 3))
    
    f = lambda x : math.sin(x) * 2
    coordinate_system.add(charts.Function(f, start=-4, end=5, step=0.02, color=(0, 0, 255)))
    
## Line function and normal function but with filled graph

![graph-9-0.png](http://tkrajina.github.io/cartesius/graph-9-0.png)&nbsp;![graph-9-1.png](http://tkrajina.github.io/cartesius/graph-9-1.png)&nbsp;

Code:

    import cartesius.main as cartesius
    import cartesius.elements as elements
    import cartesius.charts as charts

    coordinate_system = cartesius.CoordinateSystem()
    
    f = lambda x : math.sin(x) * 2
    coordinate_system.add(charts.Function(f, start=-4, end=5, step=0.02, color=0x0000ff))
    
    g = lambda x : math.sin(x) * 2
    coordinate_system.add(charts.Function(g, start=1, end=4, step=0.02, fill_color=(200, 255, 200)))
    
## Previous example with grid behind graphs

![graph-10-0.png](http://tkrajina.github.io/cartesius/graph-10-0.png)&nbsp;![graph-10-1.png](http://tkrajina.github.io/cartesius/graph-10-1.png)&nbsp;

Code:

    import cartesius.main as cartesius
    import cartesius.elements as elements
    import cartesius.charts as charts

    coordinate_system = cartesius.CoordinateSystem()
    
    # Grid:
    coordinate_system.add(elements.Grid(1, 1))
    
    f = lambda x : math.sin(x) * 2
    coordinate_system.add(charts.Function(f, start=-4, end=5, step=0.02, color=(0, 0, 255)))
    
    g = lambda x : math.sin(x) * 2
    coordinate_system.add(charts.Function(g, start=1, end=4, step=0.02, fill_color=(200, 255, 200)))
    
## Two functions

![graph-11-0.png](http://tkrajina.github.io/cartesius/graph-11-0.png)&nbsp;![graph-11-1.png](http://tkrajina.github.io/cartesius/graph-11-1.png)&nbsp;

Code:

    import cartesius.main as cartesius
    import cartesius.elements as elements
    import cartesius.charts as charts

    coordinate_system = cartesius.CoordinateSystem()
    
    coordinate_system.add(
            charts.Function(
                    math.sin,
                    start = -4,
                    end = 5,
                    step = 0.02,
                    fill_color = (0, 0, 255),
                    transparency_mask = 100))
    
    coordinate_system.add(
            charts.Function(
                    math.cos,
                    start = -4,
                    end = 5,
                    step = 0.02,
                    fill_color = (200, 255, 200),
                    transparency_mask = 100))
    
## Two functions with transparend grid over them

![graph-12-0.png](http://tkrajina.github.io/cartesius/graph-12-0.png)&nbsp;![graph-12-1.png](http://tkrajina.github.io/cartesius/graph-12-1.png)&nbsp;

Code:

    import cartesius.main as cartesius
    import cartesius.elements as elements
    import cartesius.charts as charts

    coordinate_system = cartesius.CoordinateSystem()
    
    coordinate_system.add(
            charts.Function(
                    math.sin,
                    start = -4,
                    end = 5,
                    step = 0.02,
                    fill_color = (0, 0, 255),
                    transparency_mask = 100))
    
    coordinate_system.add(
            charts.Function(
                    math.cos,
                    start = -4,
                    end = 5,
                    step = 0.02,
                    fill_color = (200, 255, 200),
                    transparency_mask = 100))
    
    coordinate_system.add(elements.Grid(1, 1, transparency_mask=140))
    
## Line charts

![graph-13-0.png](http://tkrajina.github.io/cartesius/graph-13-0.png)&nbsp;![graph-13-1.png](http://tkrajina.github.io/cartesius/graph-13-1.png)&nbsp;

Code:

    import cartesius.main as cartesius
    import cartesius.elements as elements
    import cartesius.charts as charts

    import cartesius.colors as colors
    
    coordinate_system = cartesius.CoordinateSystem()
    
    # linechart (that mimic function chart) with generator and colors computed on the fly:
    def f():
        from_color = (255, 255, 0)
        to_color = (100, 100, 255)
        i = -2
        while i < 6:
            value = 2 * math.sin(i)
            color = colors.get_color_between(from_color, to_color, (value + 2)/4.)
            yield charts.data(i, value, fill_color=color, color=(0, 0, 0))
            i += .05
    
    coordinate_system.add(
            charts.LineChart(
                    data = f,
                    transparency_mask = 0))
    
    # filled line chart with labels
    coordinate_system.add(
            charts.LineChart(
                    data = (charts.data(-2, 1, label='aaa'), 
                            charts.data(0, -1, label='bbb'), 
                            charts.data(3, 1.2), 
                            charts.data(7, 1.2)),
                    fill_color = (50, 50, 50),
                    transparency_mask = 50))
    
    # normal line chart with labels:
    coordinate_system.add(
            charts.LineChart(
                    data = (charts.data(0, 0), 
                            charts.data(1, -3), 
                            charts.data(4, 3, label='aaa', label_position=cartesius.CENTER_DOWN), 
                            charts.data(5, -2, label='custom label', label_position=cartesius.RIGHT_CENTER), 
                            charts.data(7, 0)),
                    color = (255, 0, 0),
                    transparency_mask = 150))
    
## Another example with circles

![graph-14-0.png](http://tkrajina.github.io/cartesius/graph-14-0.png)&nbsp;![graph-14-1.png](http://tkrajina.github.io/cartesius/graph-14-1.png)&nbsp;

Code:

    import cartesius.main as cartesius
    import cartesius.elements as elements
    import cartesius.charts as charts

    
    # The colors package contain e few utility functions for colors:
    import cartesius.colors as colors
    
    coordinate_system = cartesius.CoordinateSystem()
    
    from_color = (255, 0, 255)
    to_color = (0, 255, 0)
    
    iterations = 20
    for i in range(1, iterations):
        x = i / 2.
        y = math.sin(x)
        center = (i / 1, math.sin(x))
        color = colors.get_color_between(from_color, to_color, i/float(iterations))
        coordinate_system.add(elements.Circle(center, radius=math.sqrt(x),
                transparency_mask=50, fill_color=color, color=(0, 0, 0)))
    
## Circles with horizontal grid

![graph-15-0.png](http://tkrajina.github.io/cartesius/graph-15-0.png)&nbsp;![graph-15-1.png](http://tkrajina.github.io/cartesius/graph-15-1.png)&nbsp;

Code:

    import cartesius.main as cartesius
    import cartesius.elements as elements
    import cartesius.charts as charts

    coordinate_system = cartesius.CoordinateSystem()
    
    coordinate_system.add(elements.Grid(1, None, transparency_mask=200))
    
    for i in range(1, 20):
        x = i / 2.
        y = math.sin(x)
        center = (i / 1, math.sin(x))
        coordinate_system.add(elements.Circle(center, radius=math.sqrt(x),
                transparency_mask = 50, fill_color = (i * 10, 2 * 10, i * 10), color=(0, 0, 0)))
    
## Circles with horizontal grid every 2

![graph-16-0.png](http://tkrajina.github.io/cartesius/graph-16-0.png)&nbsp;![graph-16-1.png](http://tkrajina.github.io/cartesius/graph-16-1.png)&nbsp;

Code:

    import cartesius.main as cartesius
    import cartesius.elements as elements
    import cartesius.charts as charts

    coordinate_system = cartesius.CoordinateSystem()
    
    coordinate_system.add(elements.Grid(2, None, transparency_mask=200))
    
    for i in range(1, 20):
        x = i / 2.
        y = math.sin(x)
        center = (i / 1, math.sin(x))
        coordinate_system.add(elements.Circle(center, radius=math.sqrt(x),
                transparency_mask=50, fill_color=(i * 10, 2 * 10, i * 10), color=(0, 0, 0)))
    
## Circles with vertical grid every 0.5

![graph-17-0.png](http://tkrajina.github.io/cartesius/graph-17-0.png)&nbsp;![graph-17-1.png](http://tkrajina.github.io/cartesius/graph-17-1.png)&nbsp;

Code:

    import cartesius.main as cartesius
    import cartesius.elements as elements
    import cartesius.charts as charts

    coordinate_system = cartesius.CoordinateSystem()
    
    coordinate_system.add(elements.Grid(None, 0.5, transparency_mask=200))
    
    for i in range(1, 20):
        x = i / 2.
        y = math.sin(x)
        center = (i / 1, math.sin(x))
        coordinate_system.add(elements.Circle(center, radius=math.sqrt(x),
                transparency_mask=50, fill_color=(i * 10, 2 * 10, i * 10), color=(0, 0, 0)))
    
## Axis with custom label positions and decorations:

![graph-18-0.png](http://tkrajina.github.io/cartesius/graph-18-0.png)&nbsp;![graph-18-1.png](http://tkrajina.github.io/cartesius/graph-18-1.png)&nbsp;

Code:

    import cartesius.main as cartesius
    import cartesius.elements as elements
    import cartesius.charts as charts

    coordinate_system = cartesius.CoordinateSystem()
    
    coordinate_system.add(elements.Axis(horizontal=True, labels=1, points=0.25))
    coordinate_system.add(elements.Axis(vertical=True, labels=2, labels_decorator=lambda x:'speed=%sm/s' % x, points=1))
    
    f = lambda x : math.sin(x) * 2
    coordinate_system.add(charts.Function(f, start=-4, end=5, step=0.02, color=(0, 0, 255)))
    
## Axis with custom labels II

![graph-19-0.png](http://tkrajina.github.io/cartesius/graph-19-0.png)&nbsp;![graph-19-1.png](http://tkrajina.github.io/cartesius/graph-19-1.png)&nbsp;

Code:

    import cartesius.main as cartesius
    import cartesius.elements as elements
    import cartesius.charts as charts

    coordinate_system = cartesius.CoordinateSystem(bounds=(-1500, 1500, -1500, 1500))
    
    # Labels with suffixes 'm':
    coordinate_system.add(elements.Axis(horizontal=True, labels='500m', points=100))
    
    # Custom labels on custom positions:
    coordinate_system.add(elements.Axis(vertical=True, labels={1000: 'one km', 500: 'half km'},
            points = 100))
    
## Axis with custom colors

![graph-20-0.png](http://tkrajina.github.io/cartesius/graph-20-0.png)&nbsp;![graph-20-1.png](http://tkrajina.github.io/cartesius/graph-20-1.png)&nbsp;

Code:

    import cartesius.main as cartesius
    import cartesius.elements as elements
    import cartesius.charts as charts

    coordinate_system = cartesius.CoordinateSystem()
    
    coordinate_system.add(elements.Axis(horizontal=True, color=(255, 0, 0), labels=1, points=0.25))
    coordinate_system.add(elements.Axis(vertical=True, color=(0, 255, 0), labels=2, points=1))
    
    f = lambda x : x * math.sin(x * x)
    coordinate_system.add(charts.Function(f, start=-4, end=5, step=0.02, color=(0, 0, 255)))
    
## Two horizontal grids

![graph-21-0.png](http://tkrajina.github.io/cartesius/graph-21-0.png)&nbsp;![graph-21-1.png](http://tkrajina.github.io/cartesius/graph-21-1.png)&nbsp;

Code:

    import cartesius.main as cartesius
    import cartesius.elements as elements
    import cartesius.charts as charts

    coordinate_system = cartesius.CoordinateSystem()
    
    coordinate_system.add(elements.Grid(0.25, None, color=(200, 200, 200)))
    coordinate_system.add(elements.Grid(1, None, color=(250, 50, 50)))
    
    f = lambda x : math.sin(x) * 2
    coordinate_system.add(charts.Function(f, start=-4, end=5, step=0.02, color=(0, 0, 255)))
    
## Labels on different positions

![graph-22-0.png](http://tkrajina.github.io/cartesius/graph-22-0.png)&nbsp;![graph-22-1.png](http://tkrajina.github.io/cartesius/graph-22-1.png)&nbsp;![graph-22-2.png](http://tkrajina.github.io/cartesius/graph-22-2.png)&nbsp;![graph-22-3.png](http://tkrajina.github.io/cartesius/graph-22-3.png)&nbsp;![graph-22-4.png](http://tkrajina.github.io/cartesius/graph-22-4.png)&nbsp;

Code:

    import cartesius.main as cartesius
    import cartesius.elements as elements
    import cartesius.charts as charts

    cs_1 = cartesius.CoordinateSystem(bounds=(-2.5, 2.5, -2.5, 2.5))
    cs_1.add(elements.Axis(horizontal=True, points=1, labels=1, label_position=cartesius.LEFT_UP,))
    cs_1.add(elements.Axis(vertical=True, points=1, labels=1, label_position=cartesius.LEFT_CENTER,))
    
    cs_2 = cartesius.CoordinateSystem(bounds=(-2.5, 2.5, -2.5, 2.5))
    cs_2.add(elements.Axis(horizontal=True, points=1, labels=1, label_position=cartesius.LEFT_DOWN,))
    cs_2.add(elements.Axis(vertical=True, points=1, labels=1, label_position=cartesius.CENTER_UP,))
    
    cs_3 = cartesius.CoordinateSystem(bounds=(-2.5, 2.5, -2.5, 2.5))
    cs_3.add(elements.Axis(horizontal=True, points=1, labels=1, label_position=cartesius.CENTER,))
    cs_3.add(elements.Axis(vertical=True, points=1, labels=1, label_position=cartesius.CENTER_DOWN,))
    
    cs_4 = cartesius.CoordinateSystem(bounds=(-2.5, 2.5, -2.5, 2.5))
    cs_4.add(elements.Axis(horizontal=True, points=1, labels=1, label_position=cartesius.RIGHT_UP,))
    cs_4.add(elements.Axis(vertical=True, points=1, labels=1, label_position=cartesius.RIGHT_CENTER,))
    
    cs_5 = cartesius.CoordinateSystem(bounds=(-2.5, 2.5, -2.5, 2.5))
    cs_5.add(elements.Axis(horizontal=True, points=1, labels=1, label_position=cartesius.RIGHT_DOWN,))
    cs_5.add(elements.Axis(vertical=True, points=1, labels=1, label_position=cartesius.RIGHT_DOWN,))
    
## Test with hidden axis

![graph-23-0.png](http://tkrajina.github.io/cartesius/graph-23-0.png)&nbsp;![graph-23-1.png](http://tkrajina.github.io/cartesius/graph-23-1.png)&nbsp;![graph-23-2.png](http://tkrajina.github.io/cartesius/graph-23-2.png)&nbsp;![graph-23-3.png](http://tkrajina.github.io/cartesius/graph-23-3.png)&nbsp;

Code:

    import cartesius.main as cartesius
    import cartesius.elements as elements
    import cartesius.charts as charts

    
    cs_1 = cartesius.CoordinateSystem(bounds=(-2.5, 2.5, -2.5, 2.5))
    cs_1.add(elements.Axis(horizontal=True, hide=True))
    cs_1.add(elements.Axis(vertical=True))
    cs_1.add(charts.Function(
            lambda x : x * math.sin(x * x),
            start = -4,
            end = 5,
            step = 0.02,
            color = (0, 0, 255)))
    
    cs_2 = cartesius.CoordinateSystem(bounds=(-2.5, 2.5, -2.5, 2.5))
    cs_2.add(elements.Axis(horizontal=True))
    cs_2.add(elements.Axis(vertical=True, hide=True))
    cs_2.add(charts.Function(
            lambda x : x * math.sin(x * x),
            start = -4,
            end = 5,
            step = 0.02,
            color = (0, 0, 255)))
    
## Hide positive and/or negative parts of axes

![graph-24-0.png](http://tkrajina.github.io/cartesius/graph-24-0.png)&nbsp;![graph-24-1.png](http://tkrajina.github.io/cartesius/graph-24-1.png)&nbsp;![graph-24-2.png](http://tkrajina.github.io/cartesius/graph-24-2.png)&nbsp;![graph-24-3.png](http://tkrajina.github.io/cartesius/graph-24-3.png)&nbsp;

Code:

    import cartesius.main as cartesius
    import cartesius.elements as elements
    import cartesius.charts as charts

    cs_1 = cartesius.CoordinateSystem(bounds=(-2.5, 2.5, -2.5, 2.5))
    cs_1.add(charts.Function(lambda x : x * math.sin(x * x), start=-4, end=5, step=0.02, color=(0, 0, 255)))
    cs_1.add(elements.Axis(horizontal=True, hide_positive=True))
    cs_1.add(elements.Axis(vertical=True, hide_positive=True))
    
    cs_2 = cartesius.CoordinateSystem(bounds=(-2.5, 2.5, -2.5, 2.5))
    cs_2.add(charts.Function(lambda x : x * math.sin(x * x), start=-4, end=5, step=0.02, color=(0, 0, 255)))
    cs_2.add(elements.Axis(horizontal=True, hide_negative=True))
    cs_2.add(elements.Axis(vertical=True, hide_negative=True))
    
## Detached axes

![graph-25-0.png](http://tkrajina.github.io/cartesius/graph-25-0.png)&nbsp;![graph-25-1.png](http://tkrajina.github.io/cartesius/graph-25-1.png)&nbsp;

Code:

    import cartesius.main as cartesius
    import cartesius.elements as elements
    import cartesius.charts as charts

    coordinate_system = cartesius.CoordinateSystem(bounds=(-10, 10, -10, 10))
    
    coordinate_system.add(charts.Function(lambda x : x * math.sin(x * x),
            start = -4, end = 5, step = 0.02, color = (0, 0, 255)))
    
    # Standard axes:
    coordinate_system.add(elements.Axis(horizontal=True, points=2))
    coordinate_system.add(elements.Axis(vertical=True, labels=2))
    
    # You can have only one horizontal and one vertical standard axis and, if you add
    # more -- the newer will overwrite the older.
    
    # But, you can make as many as you want *detached axes*. These are just like normal
    # ones, but their center is not (0,0).
    
    # Detached:
    detached_axes_center = (-5, 4)
    
    coordinate_system.add(elements.Axis(horizontal=True, points=2, labels=2,
            detached_center=detached_axes_center, color=(255, 0, 0)))
    coordinate_system.add(elements.Axis(vertical=True, points=2, labels=2,
            detached_center=detached_axes_center, color=(0, 0, 255)))
    
    # Another pair of detached axes with hidden negative/positive halfs:
    detached_axes_center = (4, -5)
    coordinate_system.add(elements.Axis(horizontal=True, points=2, labels=2,
            detached_center=detached_axes_center, hide_negative=True))
    coordinate_system.add(elements.Axis(vertical=True, points=2, labels=2,
            detached_center=detached_axes_center, hide_positive=True))
    
## Lines different colors

![graph-26-0.png](http://tkrajina.github.io/cartesius/graph-26-0.png)&nbsp;![graph-26-1.png](http://tkrajina.github.io/cartesius/graph-26-1.png)&nbsp;

Code:

    import cartesius.main as cartesius
    import cartesius.elements as elements
    import cartesius.charts as charts

    coordinate_system = cartesius.CoordinateSystem()
    
    coordinate_system.add(elements.Line((0, 0), (-.7, -.7)))
    coordinate_system.add(elements.Line((.5, -.5), (-.5, .5), color=(0, 255, 0)))
    coordinate_system.add(elements.Line((0, 0), (7, 3), color=(0, 0, 255)))
    
## Test points of different styles with/without label and different label positions

![graph-27-0.png](http://tkrajina.github.io/cartesius/graph-27-0.png)&nbsp;![graph-27-1.png](http://tkrajina.github.io/cartesius/graph-27-1.png)&nbsp;

Code:

    import cartesius.main as cartesius
    import cartesius.elements as elements
    import cartesius.charts as charts

    coordinate_system = cartesius.CoordinateSystem(bounds=(-.5, 5, -.5, 5))
    
    # Without labels:
    coordinate_system.add(elements.Point((1, 4), style='.'))
    coordinate_system.add(elements.Point((2, 4), style='+'))
    coordinate_system.add(elements.Point((3, 4), style='x'))
    coordinate_system.add(elements.Point((4, 4), style='o'))
    
    # With labels:
    coordinate_system.add(elements.Point((1, 3), style='.', label='A'))
    coordinate_system.add(elements.Point((2, 3), style='+', label='B'))
    coordinate_system.add(elements.Point((3, 3), style='x', label='C'))
    coordinate_system.add(elements.Point((4, 3), style='o', label='D'))
    
    # With labels and custom colors:
    coordinate_system.add(elements.Point((1, 2), style='.', label='A',
            color=(255, 0, 0)))
    coordinate_system.add(elements.Point((2, 2), style='+', label='B',
            color=(0, 255, 0)))
    coordinate_system.add(elements.Point((3, 2), style='x', label='C',
            color=(0, 0, 255)))
    coordinate_system.add(elements.Point((4, 2), style='o', label='D',
            color=(150, 150, 150)))
    
    # With labels on custom positions:
    coordinate_system.add(elements.Point((1, 1), style='.', label='A',
            label_position=cartesius.RIGHT_CENTER))
    coordinate_system.add(elements.Point((2, 1), style='+', label='B',
            label_position=cartesius.LEFT_CENTER))
    coordinate_system.add(elements.Point((3, 1), style='x', label='C',
            label_position=cartesius.CENTER_UP))
    coordinate_system.add(elements.Point((4, 1), style='o', label='D',
            label_position=cartesius.CENTER_DOWN))
    

## License

Geoelevations.rb is licensed under the [Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0)

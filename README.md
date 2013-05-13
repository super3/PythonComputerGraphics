Computer Graphics
=========
Practicing the fundamentals of computer graphics by building a 2D/3D graphic engine. Emphasis is placed on simplicing and code-reuse, rather than preformance. The finished results are outputted as [PPM files](http://netpbm.sourceforge.net/doc/ppm.html). 

***

Primitives
---
Contains the bare essentials for the engine to run. These include:

* Color (`class`) - Object to contain RGB color info for pixels. Might use a 3 item tuple instead.
* Shape (`class`) - Base class for all geometric primitives.
* Image (`class`) - Object that contains all the pixel data for an image.

Geometric Primitives
---
"Contains" all the geometric primitives for the 2D part of the engine. All the geometric primitives are based on the abtract class Shape. Included geometric primitives, and their constructors:
 
* Line(x1, x2, y1, y2)
* Ellipse(x1, y1, x2, y2, color)
* Circle(x, y, radius, color)
* Polygon(point_list, color)

***

Abtract Class: Shape
---
Base class for all geometric primitives. If you are going to understand how this works you will need to read this first. 

#### Constructor and Magics
* \_\_init\_\_ - Initializes vars.
* \_\_str\_\_ (return `String`) - Prints out all draw points for the shape. Primarily for debugging.

#### Vars
* border_color (type `color Class`) - Contains the RGB draw color for the shape's border.
* inside_color (type `color Class`) - Contains the RGB draw color for the shape's inside (or fill).
* border (type `2-tuples List`) - Contains all the draw points for the shape's border.
* inside (type `2-tuples List`) - Contains all the draw points for the shape's inside (or fill).

#### Draw Methods
* draw() - Calculates all draw points for the shape, and stores in class data.
* draw_border() - Calculates a shape's border points. Implemented by child class.
* draw_inside() - Calculates a shapes's inside points (or fill). Implemented by child class.
* fill(color) - Fills the shape with a color. If no color is passed, then the border color will be used.
* remove_duplicates () - Removes all duplicate points for a passed list.

#### Transformation Methods
* move(x, y) - Translates a shape. Should be used instead of translate to avoid redrawing.
* translate(x, y) - Translates a shape. 
* rotate(x, y, angle) - Rotates a shape. 
* scale(x, y, factor_x, factor_y) - Scales a shape. 

Class: Image
---
Contains all pixel data for in image.

#### Constructor
* \_\_init\_\_ - Initializes vars. Fills background with white.

#### Vars
* x (type `int`) - X size of image.
* y (type `int`) - Y size of image.
* inten (type `int`) - Intensity of pixels. (Default is 255). 
* img - Array of pixels.

#### Methods
* fill(color) - Fill the image with a passed background color. Default white.
* getIndex(x,y) - Get pixel index from (x,y).
* blit(shapeObj) - Draw a shape onto the image.
* save(path) - Saves a PPM file to the specified path. 

***

Sample Code
---
Assuming the proper classes have been imported. 

### Line Example
	# Imports
	import Class.GeoPrimitives

    # Create a Blank Image
	img = Image(320, 240)
	# Fill Image with Color
	img.fill( Color(245, 245, 245) )
	# Create Line Objects
	line1 = Line( 60, 120, 160, 120, Color(255, 0, 0) )
	line2 = Line( 160, 120, 160, 220, Color(0, 255, 0) )
	# Rotate Lines
	line1.rotate( 160, 120, 45 )
	line2.rotate( 160, 120, 45 )
	# Scale Lines
	line1.scale( 160, 120, .5, .5 )
	line2.scale( 160, 120, .5, .5 )
	# Translate Lines
	line1.translate( 50, 50 )
	line2.translate( 50, 50 )
	# Draw Lines on Image
	img.blit( line1 )
	img.blit( line2 )
    # Create/Write Image
	img.save('test.ppm')
    
Output: 
![Line Example Output](/Images/line.jpg "Line Example Output")

### Polygon Example

    # Create Blank Image
    img = Image(320, 240)
	# Fill Image with Color
	img.fill( Color(245, 245, 245) )
	# Create Polygon
	point_list = [ (60,120), (110, 200), (110, 150), (200, 220), (160, 120) ]
	polygon1 = Polygon( point_list, Color(255,0,0) )
	# Translate Polygon
	polygon1.translate( 30, -30 )
	# Scale Polygon
	polygon1.scale( 160, 120, 1.5, 1.5 )
	# Rotate Polygon
	polygon1.rotate( 160, 120, -40 )
	# Blit and Create/Write Image
	img.blit( polygon1.fill() )
	img.save('test.ppm')
    
Output: 
![Polygon Example Output](/Images/polygon.jpg "Polygon Example Output")
#!/usr/bin/env python
# Filename: Primitives.py
# Project Github: http://github.com/super3/ClassDev
# Author: Shawn Wilkinson <me@super3.org>
# Author Website: http://super3.org/
# License: GPLv3 <http://gplv3.fsf.org/>

# Pixel Class
class Color:
	"""Contains RGB color info for pixels. Might use a 3 item tuple instead."""
	def __init__(self, r, g, b):
		self.r = r
		self.g = g
		self.b = b
	def __str__(self):
		return "%s %s %s " % (str(self.r), str(self.g), str(self.b))

# Shape Class
class Shape(object):
	"""Base class for Geometric Primitives."""
	# Magic Functions
	def __init__(self, color=Color(0,0,0)):
		self.border_color = color
		self.inside_color = color
		self.border = []
		self.inside = []
		self.do_fill = False
	def __str__(self):
		"""Returns a string containing all the points in the shape."""
		output = ""
		for a_point in self.points:
			output += str(a_point) + ", "
		return output

	# Drawing Functions
	def draw(self):
		"""Calculates a shape's points, and stores it."""
		self.border = self.draw_border()
		if self.do_fill: self.inside = self.draw_inside()
	def draw_border(self):
		"""Calculates a shape's border points."""
		raise NotImplementedError
	def draw_inside(self):
		"""Calculates a shapes's inside points (or fill)."""
		raise NotImplementedError
	def fill(self, color = None):
		"""Fills the shape with a color. If no color is passed, then the border color will be used."""
		self.do_fill = True
		if color == None: self.inside_color = self.border_color
		else: self.inside_color = color
		return self

	# Cleanup Function
	def remove_duplicates(self, points):
		"""Removes duplicates from a list by converting it to a set then back to a list."""
		return list(set(points))
	
	# Transformations
	def move(self, x, y):
		"""Translate any shape."""

		# Temp Vars
		tmp_border = []
		tmp_inside = []

		# Translate
		for point in self.border:
			tmp_border.append( (point[0]+x, point[1]+y) )
		for point in self.inside:
			tmp_border.append( (point[0]+x, point[1]+y) )	

		# Save Translated Data
		self.border = tmp_border
		self.inside = tmp_inside

	def translate(self, x, y):
		raise NotImplementedError
	def rotate(self, x, y, angle):
		raise NotImplementedError
	def scale(self, x, y, factor_x, factor_y):
		raise NotImplementedError
	def scale_eq(self, x, y, factor):
		self.scale(x, y, factor, factor)

# Image Class
class Image:
	"""Contains all pixel data for in image."""
	def __init__(self, size_x, size_y, inten = 255):
		"""Initialize vars, and fill image with white."""
		self.x = size_x
		self.y = size_y
		self.inten = inten
		self.img = []
		self.fill()
	def fill(self, color=Color(255,255,255)):
		"""Fill the image with a passed background color. Default white."""
		for y in range(self.y):
			for x in range(self.x):
				self.img.append( color )
	def getIndex(self, x, y):
		"""Get pixel index from (x,y)."""
		# I = x + xd(yd − y − 1) + 1
		return x + self.x * ( self.y - y - 1 ) - 1
	def blit(self, shapeObj):
		"""Draw a shape onto the image."""
		# Calculate Object's Points
		shapeObj.draw()
		# Draw Object on Image
		for point in shapeObj.inside:
			self.img[ self.getIndex(point[0], point[1]) ] = shapeObj.inside_color
		for point in shapeObj.border:
			self.img[ self.getIndex(point[0], point[1]) ] = shapeObj.border_color
	def save(self, path):
		"""Saves a PPM file to the specified path."""
		# Header
		head = "P3\n"
		head += "# Created by Shawn Wilkinson\n"
		head += str(self.x) + " " + str(self.y) + "\n"
		head += str(self.inten) + "\n"
		# Write to File
		f = open(path, 'w+')
		f.write(head)
		for pix in self.img:
			f.write(str(pix))
		f.close()
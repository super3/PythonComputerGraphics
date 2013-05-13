#!/usr/bin/env python
# Filename: GeoPrimitives.py
# Project Github: http://github.com/super3/ClassDev
# Author: Shawn Wilkinson <me@super3.org>
# Author Website: http://super3.org/
# License: GPLv3 <http://gplv3.fsf.org/>

# Imports
import math
import operator
from Primitives import *

# Line Class
class Line(Shape):
	# Constructor
	def __init__(self, x1, y1, x2, y2, color=Color(0,0,0)):
		# Private Vars
		self.x1 = x1
		self.x2 = x2
		self.y1 = y1
		self.y2 = y2
		# Color and Points
		super(Line, self).__init__(color)
	def __str__(self):
		return "(%s, %s) to (%s, %s)" % (str(self.x1), str(self.y1), str(self.x2), str(self.y2))

	# Equations
	def getSlopeLong(self):
		try:
			return (self.y2 - self.y1) / (self.x2 - self.x1)
		except ZeroDivisionError:
			print("ZeroDivisionError! " + str(self))
			return 0

	def getSlopeTall(self):
		try:
			return (self.x2 - self.x1) / (self.y2 - self.y1)
		except ZeroDivisionError:
			print("ZeroDivisionError! " + str(self))
			return 0

	def getIntercept(self):
		return ( -(self.getSlopeLong()) )*self.x1 + self.y1

	# More Equations
	def eq37(self, x, y, angle):
		return ( x * math.cos(math.radians(angle)) ) - ( y * math.sin(math.radians(angle)) )
	def eq38(self, x, y, angle):
		return ( y * math.cos(math.radians(angle)) ) + ( x * math.sin(math.radians(angle)) )
	def get_center(self):
		xc = (self.x1 + self.x2) / 2
		yx = (self.y1 + self.y2) / 2
		return (xc,yx)
	def get_points(self):
		return [(self.x1, self.y1), (self.x2, self.y2)]

	# Draw Functions
	def draw_border(self):
		solution = []

		# Find the x length |x1 − x2| and the y length |y1 − y2|
		x_len = abs(self.x1 - self.x2)
		y_len = abs(self.y1 - self.y2)

		if x_len > y_len:
			x_vals = []
			# Find all the integer values from x1 to x2: [x1...x2]
			for x in range(min(self.x1,self.x2+1), max(self.x1,self.x2+1)):
				x_vals.append(x)
			# Solve for the corresponding y values using Equation 2.1: [y1...y2]
			for x in x_vals:
				y = (self.getSlopeLong() * x) + self.getIntercept()
				solution.append( (x, round(y)) )
		else:
			y_vals = []
			# Find all the integer values from y1 to y2: [y1...y2]
			for y in range(min(self.y1,self.y2+1), max(self.y1,self.y2+1)):
				y_vals.append(y)
			# Solve for the corresponding x values using Equation 2.4: [x1...x2]
			for y in y_vals:
				x = self.getSlopeTall()*y - self.getSlopeTall()*self.y1 + self.x1
				solution.append( (round(x), y) )

		return solution

	def draw_inside(self):
		return []

	def draw(self):
		self.border = self.draw_border()
		return self.border

	# Transformations 
	def translate(self, x, y):
		"""
		A simple translate algorithm to translate a line drawing by xt and yt
		is outlined in the following steps:

		"""
		self.x1 += x
		self.x2 += x
		self.y1 += y
		self.y2 += y

	def rotate(self, x, y, angle):
		"""
		A simple rotation algorithm to rotate a line drawing about a point (xr, yr)
		by β-degrees is outlined in the following steps:

		"""
		# Translate the end and start points by xt = −xr and yt = −yr
		self.translate(-x,-y)
		x1 = self.x1
		x2 = self.x2
		y1 = self.y1
		y2 = self.y2

		# Rotate the translated x-values β-degrees using Equation 3.7
		self.x1 = round(self.eq37(x1, y1, angle))
		self.x2 = round(self.eq37(x2, y2, angle))
		# Rotate the translated y-values β-degrees using Equation 3.8
		self.y1 = round(self.eq38(x1, y1, angle))
		self.y2 = round(self.eq38(x2, y2, angle))

		# Translate resulting points by xt = xr and yt = yr
		self.translate(x,y)

	def scale(self, x, y, factor_x, factor_y):
		"""
		A simple scale algorithm to scale a line drawing by Sx and Sy for a fixed
		point (xf, yf) is outlined in the following steps:

		"""
		# Translate the end and start points by xt = −xf and yt = −yf
		self.translate(-x,-y)

		# Scale the translated x-values by Sx using Equation 3.9
		self.x1 = round(self.x1*factor_x)
		self.x2 = round(self.x2*factor_x)
		# Scale the translated y-values by Sy using Equation 3.10
		self.y1 = round(self.y1*factor_y)
		self.y2 = round(self.y2*factor_y)

		# Translate resulting points by xt = xf and yt = yf
		self.translate(x,y)

	# Hacks
	def minX(self):
		return min(self.x1,self.x2)
	def maxX(self):
		return max(self.x1,self.x2)
	def minY(self):
		return min(self.y1,self.y2)
	def maxY(self):
		return max(self.y1,self.y2)





# Ellipse Class
class Ellipse(Shape):
	# Constructor
	def __init__(self, x, y, a, b, color=Color(0,0,0)):
		# Private Vars
		self.x = x
		self.y = y
		self.a = a # major
		self.b = b # minor
		# Color and Points
		super(Ellipse, self).__init__(color)

	# Ellipse Functions
	def sym(self, points):
		"""Uses symmetry to find the other parts of the ellipse."""
		new_points = []
		for point in points:
			new_points.append( ( point[0], point[1])  )
			new_points.append( (-point[0], point[1])  )
			new_points.append( ( point[0], -point[1]) )
			new_points.append( (-point[0], -point[1]) )
		return new_points

	def center(self, points):
		"""Positions found points around the ellipse center."""
		new_points = []
		for point in points:
			new_points.append( (point[0]+self.x, point[1]+self.y) )
		return new_points

	# Draw Functions
	def draw_border(self):
		solution = []

		# Initialize starting point to (a, 0): x = a and y = 0
		x = self.a
		y = 0
		solution.append( (x,y) )

		# If a2(y + 1) < b2(x − .5), (In region 2)
		while (math.pow(self.a,2) * (y + 1)) < (math.pow(self.b,2) * (x - 0.5)):
			# Compute the next y location for region 2: y + 1
			y += 1
			# Compute the x value (xa) for y + 1 using Equation 2.8
			x = round(math.sqrt(math.pow(self.a,2) * (1-(1/math.pow(self.b,2))*math.pow(y,2))))
			solution.append( (x,y) )
		# Now in region 1
		while(x > 0):
			# Compute the next x location for region 1: x − 1
			x -= 1
			# Compute the y location (ya) for x − 1 using Equation 2.9
			y = round(math.sqrt(math.pow(self.b,2) * (1-(1/math.pow(self.a,2))*math.pow(x,2))))
			solution.append( (x, y) )
			
		# From the discovered points in the first quadrant, find the other points by symmetry
		solution = self.sym(solution)
		# Add the center point (xc, yc) to all discovered points
		solution = self.center(solution)
		# Remove duplicates to be safe
		solution = self.remove_duplicates(solution)
		
		return solution

	def draw_inside(self):
		solution = []

		# Find the absolute boundaries of the primitive
		self.border = self.draw_border()
		min_y = min(y[1] for y in self.border)
		max_y = max(y[1] for y in self.border)
		# For each row of the primitive, find the boundary pixels
		for row in range( min_y, max_y ):
			bound_min = min((y for y in self.border if y[1]==row), key=operator.itemgetter(0))
			bound_max = max((y for y in self.border if y[1]==row), key=operator.itemgetter(0))
			# For each row, fill in the pixels between boundary pixels
			solution.extend( Line(bound_min[0], bound_min[1], bound_max[0], bound_max[1]).draw() )

		return solution

	# Transformations
	def translate(self, x, y):
		self.x += x
		self.y += y

	def rotate(self, x, y, angle):
		# One possible way this could work is forming a line from the center of the ellipse
		# to one of the border points. Then you apply your standard line rotation with the
		# center point being the rotation point. Unfortunately, you literally have to do this
		# for every single border point. 
		raise NotImplementedError

	def scale(self, x, y, factor_x, factor_y):
		# This only scales on the center point.
		self.a *= factor_x
		self.b *= factor_y






# Circle Class
class Circle(Ellipse):
	def __init__(self, x, y, r, color=Color(0,0,0)):
		super(Circle, self).__init__(x,y,r,r,color)





# Polygon Class
class Polygon(Shape):
	# Constructor
	def __init__(self, point_list, color=Color(0,0,0)):
		# Private Vars
		self.point_list = point_list
		# Color and Points
		super(Polygon, self).__init__(color)

	# Equations
	def getSlope(self, x1, y1, x2, y2):
		return (x2 - x1) / (y2 - y1)
	def eq24(self, x1, y1, x2, y2, y):
		return self.getSlope(x1, y1, x2, y2)*y - self.getSlope(x1, y1, x2, y2)*y1 + x1

	# Draw Functions
	def draw_border(self):
		# A simple polygon algorithm is outlined in the following steps for n vertex
		# points [(x1, y1), (x2, y2), ..., (xn, yn)], listed in the order to be connected:
		solution = []
		# 1. Use the line algorithm in section 2.1 to draw a line between adjacent points in the order listed
		for i in range(len(self.point_list)-1):
			x1 = self.point_list[i][0]
			y1 = self.point_list[i][1]
			x2 = self.point_list[i+1][0]
			y2 = self.point_list[i+1][1]
			solution.extend( Line(x1, y1, x2, y2).draw() )
		# 2. Use the line algorithm in section 2.1 to draw a line between the last point in the list and the first point
		x1 = self.point_list[0][0]
		y1 = self.point_list[0][1]
		x2 = self.point_list[len(self.point_list)-1][0]
		y2 = self.point_list[len(self.point_list)-1][1]
		solution.extend( Line(x1, y1, x2, y2).draw() )
		solution = self.remove_duplicates(solution)
		return solution

	def scan_line(self, a):
		"""
		A simple scan-line intersection algorithm to compute the intersection
	 	of a scan line y = a and an edge – with vertex points (x1, y1) and (x2, y2)
	 	from the polygon's list of vertex points.

		"""
		solution = []

		for i in range(len(self.point_list)):

			# Two vertex points to local vars
			x1 = self.point_list[i][0]
			y1 = self.point_list[i][1]
			x2 = self.point_list[(i+1)%len(self.point_list)][0]
			y2 = self.point_list[(i+1)%len(self.point_list)][1]
			
			# This is a horizontal line, so there is not an intersection
			if y2 - y1 == 0: continue
			else:
				# The scan line is outside of the edge, so there is not an intersection
				if not (min(y1,y2) <= a and max(y1,y2) >= a): continue 
				
				# Find the y-value of the maximal vertex point
				y_max = max(y1,y2)
				
				# The scan line intersects a maximal vertex-point, so there is not an intersection
				if a == y_max: continue
				else:
					# Find the x-value of the intersect for y = a using Equation 2.4
					x_val = round(self.eq24(x1, y1, x2, y2, a))
					solution.append( (x_val, a) )

		return solution

	def draw_inside(self):
		point_pairs = []
		solution = []

		# Find the min y-value (ymin) and the max y-value (ymax)
		min_y = min(y[1] for y in self.point_list)
		max_y = max(y[1] for y in self.point_list)

		# Use the scan-line intersection algorithm to find intersections
		for a in range(min_y+1, max_y): # min_y+1 to get throw away single bottom point, range throws away max_y
			tmp = self.scan_line(a)
			# sort intersections from minimal to maximal value based on the x values
			tmp.sort( key=operator.itemgetter(0) ) 
			if len(tmp) > 0: point_pairs.extend( tmp ) 

		# If there are intersections
		if len(point_pairs) > 0:
			# Fill in pixels between adjacent pairs of intersection points
			for i in range(0, len(point_pairs)-1, 2):
				solution.extend( Line(point_pairs[i][0], point_pairs[i][1], point_pairs[i+1][0], point_pairs[i+1][1]).draw() )	

		return solution

	# Transformations
	def translate(self, x, y):
		tmp_list = []
		for point in self.point_list:
			tmp_list.append( (point[0]+x, point[1]+y) )
		self.point_list = tmp_list
	
	def rotate(self, x, y, angle):
		tmp_point_list = []
		for i in range(len(self.point_list)):

			# Two vertex points to local vars
			x1 = self.point_list[i][0]
			y1 = self.point_list[i][1]
			x2 = self.point_list[(i+1)%len(self.point_list)][0]
			y2 = self.point_list[(i+1)%len(self.point_list)][1]

			# Preform rotation on temporary line 
			tmp_line = Line(x1, y1, x2, y2)
			tmp_line.rotate(x, y, angle)

			# Rotated points back to point list
			tmp_point_list.append((tmp_line.x1, tmp_line.y1))
		self.point_list = tmp_point_list

	
	def scale(self, x, y, factor_x, factor_y):
		tmp_point_list = []
		for i in range(len(self.point_list)):
			# Two vertex points to local vars
			x1 = self.point_list[i][0]
			y1 = self.point_list[i][1]
			x2 = self.point_list[(i+1)%len(self.point_list)][0]
			y2 = self.point_list[(i+1)%len(self.point_list)][1]

			# Preform rotation on temporary line 
			tmp_line = Line(x1, y1, x2, y2)
			tmp_line.scale(x, y, factor_x, factor_y)

			# Rotated points back to point list
			tmp_point_list.append((tmp_line.x1, tmp_line.y1))
		self.point_list = tmp_point_list

	def scale_eq(self, x, y, factor):
		self.scale(x, y, factor, factor)
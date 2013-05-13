#!/usr/bin/env python
# Filename: Line3D.py
# Project Github: http://github.com/super3/ClassDev
# Author: Shawn Wilkinson <me@super3.org>
# Author Website: http://super3.org/
# License: GPLv3 <http://gplv3.fsf.org/>

# Imports 
import math
from GeoPrimitives import Image
from GeoPrimitives import Line

# Point 3D
class Point3D:
	# Constructor
	def __init__(self, point):
		self.point = point # 3-tuple

	# Equations
	def eq(self, xya, za, d):
		"""Works for Equation 4.1 and 4.2."""
		return (xya/za) * d

	# Method
	def get_2D_point(self, d):
		"""Returns a 2-tuple 2D point from a passed d."""
		x = self.eq(self.point[0], self.point[2], d)
		y = self.eq(self.point[1], self.point[2], d)
		return x,y

# Line 3D
class Line3D:
	# Constructor
	def __init__(self, start_pt, end_pt):
		# Private Vars
		self.start_pt = Point3D(start_pt)
		self.end_pt = Point3D(end_pt)

	# Equations
	def project(self, d):
		"""
		A simple projection algorithm to project the vertex points of a 3D line
		segment onto a view plane located at z = d, for a center of projection at the
		origin (0,0,0), is outlined in the following steps:

		"""

		# Project the x and y values of the start and end points to the view plane using
		x1, y1 = self.start_pt.get_2D_point(d)
		x2, y2 = self.end_pt.get_2D_point(d)
		
		# Return a 2D line object
		return Line(x1, y1, x2, y2)

# World 3D
class World3D:
	# Constructor
	def __init__(self):
		self.object_list = []
	def add(self, an_object):
		self.object_list.append( an_object )

	def get_center(self, lines):
		min_x = min(x.minX() for x in lines)
		max_x = max(x.maxX() for x in lines)
		min_y = min(y.minY() for y in lines)
		max_y = max(y.maxY() for y in lines)
		xc = (max_x + min_x) / 2
		yc = (max_y + min_y) / 2
		return (xc, yc)

	def display(self, d, translate, scale):
		"""
		For a translation location at (xL, yL) and a scale factor of sf, a simple
		display algorithm to display points projected onto a view plane (as describe
		in section 4.2) as 2D lines is as follows:

		"""
		
		# 3D to 2D Lines
		tmp_lines = []
		for line_3D in self.object_list:
			tmp_lines.append( line_3D.project(d) )
		# 1. Find the center of the 2D points using Equations 4.3 and 4.4.
		xc, yc = self.get_center(tmp_lines)
		# 2. Translate the start and end points of each line using the translation algorithm in
		# section 3.1, where xt and yt are found from Equations 4.5 and 4.6
		for line in tmp_lines: 
			line.translate(translate[0]-xc, translate[1]-yc)
		# 3. Scale the translated start and end points from Step 2 by Sx = sf and Sy = sf for a fix point of (xL, yL) 
		# using the scale algorithm in section 3.3.
		for line in tmp_lines: 
			line.scale_eq(translate[0], translate[1], scale)
		# 4. Find the points between each start and end point using the line algorithm in section 2.1
		for line in tmp_lines:
			print(line)
		return tmp_lines

# Arbitrary 3D View
class Arbit3D:
	# Constructor
	def __init__(self, a, b):
		self.a = a
		self.b = b

	# Equations
	def eq(self, vector, b):
		"""
		u'1 = u1							(4.19)
		u'2	= u2 * cos(β) − u3 * sin(β) 	(4.20)
		u'3	= u3 * cos(β) + u2 * sin(β)	    (4.21)
		
		"""
		vector1 = vector[0]
		vector2 = (vector[1] * math.cos(math.radians(b))) - (vector[2] * math.sin(math.radians(b)))
		vector3 = (vector[2] * math.cos(math.radians(b))) + (vector[1] * math.sin(math.radians(b)))
		return (round(vector1,4), round(vector2,4), round(vector3,4))
	def eq2(self, vector, a):
		"""
		u'1 = u1 * cos(α) + u3 * sin(α) 	(4.10)
		u'2	= u2 							(4.11)
		u'3	= u	3 * cos(α) − u1	* sin(α)    (4.12)

		"""
		vector1 = (vector[0] * math.cos(math.radians(a))) + (vector[2] * math.sin(math.radians(a)))
		vector2 = vector[1]
		vector3 = (vector[2] * math.cos(math.radians(a))) - (vector[0] * math.sin(math.radians(a)))
		return (round(vector1,4), round(vector2,4), round(vector3,4))

	def view(self):
		"""
		A simple 3D view algorithm to define a view for a 3D environment given
		α and β is outlined in the following steps:

		"""

		# 1. Initialize ~u to (1, 0, 0), ~v to (0, 1, 0), and ~n to (0, 0, 1)
		u = (1, 0, 0)
		v = (0, 1, 0)
		n = (0, 0, 1)

		# 2. Rotate ~u by β using Equations 4.19, 4.20, and 4.21
		u = self.eq(u, self.b)
		# 3. Rotate ~v by β using Equations 4.22, 4.23, and 4.24
		v = self.eq(v, self.b)
		# 4. Rotate ~n by β using Equations 4.25, 4.26, and 4.27
		n = self.eq(n, self.b)

		# 5. Rotate the result of step 2 by α using Equations 4.10, 4.11, and 4.12
		u = self.eq2(u, self.a)
		# 6. Rotate the result of step 3 by α using Equations 4.13, 4.14, and 4.15
		v = self.eq2(v, self.a)
		# 7. Rotate the result of step 4 by α using Equations 4.16, 4.17, and 4.18
		n = self.eq2(n, self.a)
		
		print(u)
		print(v)
		print(n) 
		#return u,v,n

# Arbit 3D View Alignment
	# Constructor
	def __init__(self, vertex_list):
		pass

	# Equations
		def eq(self, vrp):
			"""4.28 to 4.30"""
			for vertex in vertex_list:
				x = vertex[0] - vrp[0]
				y = vertex[1] - vrp[1]
				z = vertex[2] - vrp[2]
				vertex = (x, y, z)
		def eq2(self)
			pass

	def align(self, vrp, cop):	
		"""
		A simple 3D view-alignment algorithm to align the view reference coordinate system
		with the world coordinate-system, for a VRP = (xvrp, yvrp, zvrp), CoP = (0, 0, dn),
		and view reference coordinate system = [~u,~v, ~n], is as follows:

		"""

		# 1. For each vertex point
		for vertex in vertex_list:
			# (a) Translate the x-values by -xvrp	using Equation 4.28
			# (b) Translate the y-values by -yvrp	using Equation 4.29
			# (c) Translate the z-values by -zvrp	using Equation 4.30
			self.eq(vrp)
			# (d) Rotate the new x-values from step (a) by ~u using Equation 4.31
			# (e) Rotate the new y-values from step (b) by ~v using Equation 4.32
			# (f) Rotate the new z-values from step (c) by ~n using Equation 4.33
			# (g) Translate the new z-values from step (f) by −dn	using Equation 4.36
			pass


# Unit Tests
if __name__ == "__main__":
	world1 = World3D()
	world1.add( Line3D( (35,40,70), (20,30,50) ) )
	#world1.align()
	# VRP = (20, 20, 75), CoP = (0, 0, 20), ~u = (0.7071, 0.7071, 0), ~v = (0, 0, 1), ~n = (0.7071, −0.7071, 0)
	# Output: Aligned Start-Point = (24.7487, −5, −23.5355), Aligned End-Point = (7.0711, −25, −27.0711)
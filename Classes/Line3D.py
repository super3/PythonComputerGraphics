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
		#for line in tmp_lines:
		#	print(line)
		return tmp_lines

	def finish(self):
		# 1. Find the view reference coordinate system = [~u,~v, ~n] for α and β using the 3D view algorithm in
		#    section 4.4

		# 2. Align the 3D environment to the standard view for the VRP, CoP, and [~u,~v, ~n] using the 3D
		#    view-alignment algorithm in section 4.5.

		# 3. Project the vertex points to the view plane at z = −dn using the projection algorithm in section 4.2.

		# 4. Use the display algorithm from section 4.3 to display the projected	vertex points as 2D lines.
		pass

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
		
		#print(u)
		#print(v)
		#print(n) 
		return u,v,n

# Arbit 3D View Alignment
class ArbitAlign:
	# Constructor
	def __init__(self, vertex_list):
		self.vertex_list = vertex_list

	# Equations
	def eq(self, vertex, vrp):
		"""4.28 to 4.30"""
		x = vertex[0] - vrp[0]
		y = vertex[1] - vrp[1]
		z = vertex[2] - vrp[2]
		return (x, y, z)
	def eq2(self, vertex, u, v, n):
		"""4.31-4.33"""
		x = vertex[0] * u[0] + vertex[1] * u[1] + vertex[2] * u[2]
		y = vertex[0] * v[0] + vertex[1] * v[1] + vertex[2] * v[2]  
		z = vertex[0] * n[0] + vertex[1] * n[1] + vertex[2] * n[2]
		return (x, y, z)

	def align(self, vrp, cop, u, v, n):	
		"""
		A simple 3D view-alignment algorithm to align the view reference coordinate system
		with the world coordinate-system, for a VRP = (xvrp, yvrp, zvrp), CoP = (0, 0, dn),
		and view reference coordinate system = [~u,~v, ~n], is as follows:

		"""
		new_list = []

		# 1. For each vertex point
		for vertex in self.vertex_list:
			# (a) Translate the x-values by -xvrp	using Equation 4.28
			# (b) Translate the y-values by -yvrp	using Equation 4.29
			# (c) Translate the z-values by -zvrp	using Equation 4.30
			vertex = self.eq(vertex, vrp)

			# (d) Rotate the new x-values from step (a) by ~u using Equation 4.31
			# (e) Rotate the new y-values from step (b) by ~v using Equation 4.32
			# (f) Rotate the new z-values from step (c) by ~n using Equation 4.33
			
			vertex = self.eq2(vertex, u, v, n)
			

			# (g) Translate the new z-values from step (f) by −dn	using Equation 4.36
			vertex = vertex[0], vertex[1], vertex[2] - cop[2]

			new_list.append(vertex)
		return new_list

class DView:
	def __init__(self, a, b, vrp, cop, point_list, trans, scale):
		self.a = a
		self.b = b
		self.vrp = vrp
		self.cop = cop
		self.point_list = point_list
		self.trans = trans
		self.scale = scale
	def run(self):
		# 1. Find the view reference coordinate system = [~u,~v, ~n] for α and β using the 3D view algorithm in
		#    section 4.4
		u, v, n = Arbit3D(self.a, self.b).view()

		# 2. Align the 3D environment to the standard view for the VRP, CoP, and [~u,~v, ~n] using the 3D
		#    view-alignment algorithm in section 4.5.
		arbit = ArbitAlign(self.point_list)
		out = arbit.align(self.vrp, self.cop, u, v, n)

		# 3. Project the vertex points to the view plane at z = −dn using the projection algorithm in section 4.2.

		# 4. Use the display algorithm from section 4.3 to display the projected vertex points as 2D lines.
		myworld = World3D()
		myworld.add(Line3D(out[0], out[1]))
		finish = myworld.display(self.cop[2], self.trans, self.scale)
		return finish

		

# Unit Tests
def float_eq(a, b, epsilon=0.01):
	return abs(a - b) < epsilon

def unit_test1():
	"""Testing 4.7 Unit Tests #1"""
	# Input: Wire-frame environment with one 3D line, Start Point = (35, 40, 70),
	# End Point = (20, 30, 50), project onto a view plane located at d = 20
	# Output: Projected Start-Point = (10, 11.43), Projected End-Point = (8, 12)
	assert(Line3D((35,40,70),(20,30,50)).project(20).x1 == 10)
	assert(float_eq(Line3D((35,40,70),(20,30,50)).project(20).y1, 11.43))
	assert(Line3D((35,40,70),(20,30,50)).project(20).x2 == 8)
	assert(Line3D((35,40,70),(20,30,50)).project(20).y2 == 12)

	# Input: Wire-frame environment with one 3D line, Start Point =(35, 40, 70),
	# End Point = (20, 30, 50), project onto a view plane located at d = −20
	# Output: Projected Start-Point = (−10, −11.43), Projected End-Point = (−8, −12)
	assert(Line3D((35,40,70),(20,30,50)).project(-20).x1 == -10)
	assert(float_eq(Line3D((35,40,70),(20,30,50)).project(-20).y1, -11.43))
	assert(Line3D((35,40,70),(20,30,50)).project(-20).x2 == -8)
	assert(Line3D((35,40,70),(20,30,50)).project(-20).y2 == -12)

def unit_test2():
	"""Testing 4.7 Unit Tests #2"""
	# Input: Wire-frame environment with one 3D line, Start Point = (35, 40, 70),
	# End Point = (20, 30, 50), projected onto a view plane located at d = 20
	# (using the projection algorithm in section 4.2) – translate to location 
	# (160, 120), and scale by sf = 10
	# Output: Displayed Start-Point = (170, 117), Displayed End-Point = (150, 123)
	myworld = World3D()
	myworld.add(Line3D((35,40,70), (20,30,50)))
	assert(myworld.display(20, (160,120), 10)[0].x1 == 170)
	assert(myworld.display(20, (160,120), 10)[0].y1 == 117)
	assert(myworld.display(20, (160,120), 10)[0].x2 == 150)
	assert(myworld.display(20, (160,120), 10)[0].y2 == 123)
	

	# Input: Wire-frame environment with two 3D line, Line 1 – Start
	# Point = (35, 40, 70), and End Point = (20, 30, 50); Line 2 – Start
	# Point = (55, 40, 20), and End Point = (30, 50, 10); projected onto a
	# view plane located at d = 20 (using the projection algorithm
	# in section 4.2) – translate to location (500, 500), and scale by
	# sf = 10
	# Output: Line 1 –Displayed Start-Point = (260, 57), and 
	# Displayed End-Point = (240, 63); Line 2 – Displayed Start-Point = (710, 343),
	# and Displayed End-Point = (760, 943)
	
	myworld1 = World3D()
	myworld1.add(Line3D((35,40,70),(20,30,50)))
	myworld1.add(Line3D((55,40,20),(30,50,10)))

	assert(myworld1.display(20, (500,500), 10)[0].x1 == 260)
	assert(myworld1.display(20, (500,500), 10)[0].y1 == 57)
	assert(myworld1.display(20, (500,500), 10)[0].x2 == 240)
	assert(myworld1.display(20, (500,500), 10)[0].y2 == 63)

	assert(myworld1.display(20, (500,500), 10)[1].x1 == 710)
	assert(myworld1.display(20, (500,500), 10)[1].y1 == 343)
	assert(myworld1.display(20, (500,500), 10)[1].x2 == 760)
	assert(myworld1.display(20, (500,500), 10)[1].y2 == 943)

def unit_test3():
	"""Testing 4.7 Unit Tests #3"""
	arbit = Arbit3D(45, 90)
	result = arbit.view()
	assert(str(result) == "((0.7071, 0.0, -0.7071), (0.7071, 0.0, 0.7071), (0.0, -1.0, 0.0))")

def unit_test4():
	"""Testing 4.7 Unit Tests #4"""
	#world = World3D()
	#world.add( Line3D( (35,40,70), (20,30,50) ) )
	#world.align()

	vrp = (20, 20, 75)
	cop = (0, 0, 20)
	u = (0.7071, 0.7071, 0)
	v = (0, 0, 1)
	n = (0.7071, -0.7071, 0)

	arbit = ArbitAlign([(35,40,70), (20,30,50)])
	out = arbit.align(vrp, cop, u, v, n)

	# VRP = (20, 20, 75), CoP = (0, 0, 20), ~u = (0.7071, 0.7071, 0), ~v = (0, 0, 1), ~n = (0.7071, −0.7071, 0)
	# Output: Aligned Start-Point = (24.7487, −5, −23.5355), Aligned End-Point = (7.0711, −25, −27.0711)
	assert(str(out) == "[(24.7485, -5, -23.5355), (7.071, -25, -27.070999999999998)]")

def unit_test5():
	"""Testing 4.7 Unit Test #5"""
	#world = World3D()
	#world.add( Line3D( (35,40,70), (20,30,50) ) )
	#world.finish()

	# – Input: Wire-frame environment with one 3D line, Start Point =
	# (35, 40, 70), End Point = (20, 30, 50). VRP = (20, 20, 75), CoP =
	# (0, 0, 20), α = 45, and β = 90. Translate to location (160, 120),
	# and scale by sf = 10
	# – Output: Displayed Start-Point = (136, 197), Displayed End-Point
	# = (184, 43)

	DView(45, 90, (20, 20, 75), (0, 0, 20), [(35, 40, 70), (20, 30, 50)], (160,120), 10).run()

	# – Input: Wire-frame environment with one 3D line, Start Point =
	# (35, 40, 70), End Point = (20, 30, 50). VRP = (0, 0, 20), CoP =
	# (0, 0, −20), α = 0, and β = 0. Translate to location (160, 120),
	# and scale by sf = 10
	# 4.8. REVIEW QUESTIONS 65
	# – Output: Displayed Start-Point = (170, 117), Displayed End-Point
	# = (150, 123)

	test = DView(0, 0, (0, 0, 20), (0, 0, -20), [(35, 40, 70), (20, 30, 50)], (160,120), 10).run()
	#print(test[0])

def ex1():
	points = [(35, 40, 70), (20, 30, 50)]
	outlines = DView(45, 90, (20, 20, 75), (0, 0, 20), points, (160,120), 80).run()
	print(outlines[0])

# Main 
if __name__ == "__main__":
	unit_test1()
	unit_test2()
	unit_test3()
	unit_test4()
	unit_test5()

	ex1()
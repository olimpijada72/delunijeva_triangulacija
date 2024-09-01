import sys, os, math
import random
import sys
import pygame

#Funkcija za odredjivanje opisane kruznice bilo koje tri tacke
def circumcircle(tri):
	try:
		D = ( (tri[0][0] - tri[2][0]) * (tri[1][1] - tri[2][1]) - (tri[1][0] -  tri[2][0]) * (tri[0][1] - tri[2][1]) )
		
		center_x = (((tri[0][0] - tri[2][0]) * (tri[0][0] + tri[2][0]) + (tri[0][1] - tri[2][1]) * (tri[0][1] + tri[2][1])) / 2 * (tri[1][1] - tri[2][1]) - ((tri[1][0] - tri[2][0]) * (tri[1][0] + tri[2][0]) + (tri[1][1] - tri[2][1]) * (tri[1][1] + tri[2][1])) / 2 * (tri[0][1] - tri[2][1])) / D
		
		center_y = (((tri[1][0] - tri[2][0]) * (tri[1][0] + tri[2][0]) + (tri[1][1] - tri[2][1]) * (tri[1][1] + tri[2][1])) / 2 * (tri[0][0] - tri[2][0]) - ((tri[0][0] - tri[2][0]) * (tri[0][0] + tri[2][0]) + (tri[0][1] - tri[2][1]) * (tri[0][1] + tri[2][1])) / 2 * (tri[1][0] - tri[2][0])) / D
		
		radius = math.sqrt ((tri[2][0] - center_x)**2 + (tri[2][1] - center_y)**2 )
		
		return [[center_x, center_y], radius]
	except:
		print("Divide By Zero error")
		# print(tri)

# Proverava da li se tacka nalazi unutar kruznice
def pointInCircle(point, circle):
	#This is pretty simple; just find the distance between the point and the center. If it's less than or equal to the radius, the point is inside the circle
	
	d = math.sqrt( math.pow(point[0] - circle[0][0], 2) + math.pow(point[1] - circle[0][1],2) )
	if d < circle[1]:
		return True
	else:
		return False
	
# Obicna Point (tacka) klasa
class Point():
	def __init__(self, x, y):
		self._x = x
		self._y = y
	
	#Position of the point
	def pos(self):
		return [self._x, self._y]
			
	#Determines if two points are equivalent
	def isEqual(self, other_point):
		if(self._x == other_point._x and self._y == other_point._y): return True
		else: return False
	
	#Convert the point into a string (for debugging purposes)
	def pointToStr(self):
		return str(self.pos())

# Obicna Edge(duz) klasa
class Edge():
	def __init__(self, a, b):
		if a is not b:
			self._a = a
			self._b = b
	
	# Provera da li su dve duzi iste
	def isEqual(self, other_edge):
		if (self._a.isEqual(other_edge._a) or self._b.isEqual(other_edge._a)) and (self._a.isEqual(other_edge._b) or self._b.isEqual(other_edge._b)):
			return True
		elif self == other_edge:
			return True
		else:
			return False
	
	#Konvertuje duz u string (za debugging)
	def edgeToStr(self):
		return str([self._a.pos(), self._b.pos()])
	
	#Racuna duzinu duzi
	def length(self):
		return math.sqrt( math.pow(self._b.pos()[0] - self._a.pos()[0],2) + math.pow(self._b.pos()[1] - self._a.pos()[1],2))
	
	#Proverava da li se dve duzi presecaju
	def edgeIntersection(self, other_edge):

		if self.isEqual(other_edge):
			return False
		else:
			try:
				x1 = self._a.pos()[0]
				x2 = self._b.pos()[0]
				x3 = other_edge._a.pos()[0]
				x4 = other_edge._b.pos()[0]
				y1 = self._a.pos()[1]
				y2 = self._b.pos()[1]
				y3 = other_edge._a.pos()[1]
				y4 = other_edge._b.pos()[1]
				t = (((x1 - x3)*(y3 - y4)) - ((y1 - y3)*(x3 - x4))) / (((x1 - x2)*(y3 - y4)) - ((y1 - y2)*(x3 - x4)))
				u = (((x2 - x1)*(y1 - y3)) - ((y2 - y1)*(x1 - x3))) / (((x1 - x2)*(y3 - y4)) - ((y1 - y2)*(x3 - x4)))
				
				#If 0 <= t <= 1 or 0 <= u <= 1, onda postoji presek. 
				if (t >= 0 and t <= 1) and (u >= 0 and u <= 1):
					int_x = int(x1 + t*(x2 - x1))
					int_y = int(y1 + t*(y2 - y1))
					int_point = Point(int_x, int_y)
					
					#Ako se tacka preseka nalazi na jednom od temena, onda se date duzi ne seku
					if self._a.isEqual(int_point) or self._b.isEqual(int_point) or other_edge._a.isEqual(int_point) or other_edge._b.isEqual(int_point):
						return False
					
					#Ako nema tacke, onda se ne seku
					else:
						return True
					
				else:
					return False
			except:
				#Divide-by-zero error se tumaci kao da se duzi ne seku
				return False

#Obicna Triangle (trougao) klasa
class Triangle():
	
	#Ne moze da se napravi trougao ako su bilo koje dve tacke iste
	def __init__(self, a, b, c):
		if a is not b and a is not c:
			self._a = a
		if b is not a and b is not c:
			self._b = b
		if c is not a and c is not b:
			self._c = c
	
	#Provera da li su dva trougla ista (da li su im sva 3 temena ista)
	def isEqual(self, other_tri):
		if (self._a is other_tri._a or self._a is other_tri._b or self._a is other_tri._c) and (self._b is other_tri._a or self._b is other_tri._b or self._b is other_tri._c) and (self._c is other_tri._a or self._c is other_tri._b or self._c is other_tri._c): return True
		else: return False
	
	#Ispisivanje trougla (za debugging)
	def printTriangle(self):
		print("A: " + self._a.pointToStr() + " B: " + self._b.pointToStr() + " C: " + self._c.pointToStr())

#Graph class
class Graph():
	def __init__(self):
		
		#Lista svih tacaka
		self._points = []
		
		#Lista svih trouglova
		self._triangles = []
		
		#Lista svih duzi
		self._edges = []
		
		#Maksimumi tacaka (za sortiranje)
		self._point_min_x = 0
		self._point_max_x = 0
		
	def addPoint(self, point):
	
		#Provera da li postoji vec ta tacka
		for x in self._points:
			if x.isEqual(point): 
				return False
			
		# Ako tacka ima X vrednost nizu od bilo koje druge tacke
		if self._point_min_x > point.pos()[0] or self._point_min_x == 0:
			self._points.insert(0,point)
			self._point_min_x = point.pos()[0]
			return True
		
		# Ako tacka ima X vrednost visu od bilo koje druge tacke
		elif self._point_max_x < point.pos()[0]:
			self._points.append(point)
			self._point_max_x = point.pos()[0]
			return True
		
		# Ako tacka ima X vrednost negde u sredini
		else:
			same_x = []
			for x in self._points:
				if x.pos()[0] == point.pos()[0]:
					same_x.append(x)
			
			# Ako ni jedna tacka nema istu X vrednost kao nova tacka,
			# nadji prvu tacku koju ima visu X vrednost i ubaci novu tacku pre te
			if len(same_x) == 0:
				first_greater = 0
				for x in self._points:
					if x.pos()[0] > point.pos()[0]:
						first_greater = self._points.index(x)
						break
				self._points.insert(first_greater, point)
				return True
			
			# Ako postoji samo jedna tacka sa istom X vrednoscu,
			# uporedi Y vrednosti da utvrdis gde da je ubacis
			elif len(same_x) == 1:
				index = self._points.index(same_x[0])
				if same_x[0].pos()[1] > point.pos()[1]:
					self._points.insert(index - 1, point)
					return True
				else:
					self._points.insert(index + 1, point)
					return True
			
			# Ako vise tacaka imaju istu X vrednost, na osnovu Y vrednosti odredi
			# gde nova tacka treba da bude
			else:
				first_greater_y = 0
				for x in same_x:
					if x.pos()[1] > point.pos()[1]:
						first_greater_y = self._points.index(x)
						break
				if(first_greater_y != 0):
					self._points.insert(first_greater_y, point)
					return True
				else:
					self._points.insert(self._points.index(same_x[len(same_x) - 1]), point)
					return True
		
	def addEdge(self, edge):
		
		#Proveri da li vec postoji takva duz, ako nema, dodaj
		for x in self._edges:
			if x.isEqual(edge):
				return False
		self._edges.append(edge)
		return True
		
	#Doda trougao u listu trouglova i vrati true ako uspe.
	#Ako postoji isti trouga, vraca false
	def addTriangle(self, triangle):
		
		#Proveri da li postoji isti trougao
		for x in self._triangles:
			if x.isEqual(triangle): return False
		
		#Ako nema, dodaj
		self._triangles.append(triangle)
		tri = [ triangle._a.pos(), triangle._b.pos(), triangle._c.pos() ]
		return True
		
	# Proveri da li je trougao Delunej
	# (tj. da li u opisanoj kruznici nema drugihtacaka )	
	def triangleIsDelaunay(self, triangle):
		tri = [ triangle._a.pos(), triangle._b.pos(), triangle._c.pos() ]
		cc = circumcircle(tri)
		for x in self._points:
			#print(x.pos())
			#Ako dobijemo divide-by-zero error,	pretpostavljamo da trougao nije Delaunay
			if not (x.isEqual(triangle._a) and x.isEqual(triangle._b) and x.isEqual(triangle._c)):
				try:
					if pointInCircle(x.pos(), cc):
						return False
				except:
					return False
		#self._circles.append(cc)
		return True
	
	#Generesi Delunijevu mrezu tako sto ce se svaki moguci trougao testirati da li zadovoljava Delunijev uslov,
	#pa ce se zatim proveriti koje duzi se presecaju, i naposletku otkloniti duzu od dve duzi 
	def generateDelaunayMesh(self):
	
		#Napravi svaki moguci trougao i proveri Delunijev uslov
		for p1 in self._points:
			for p2 in self._points:
				for p3 in self._points:
					if not p1.isEqual(p2) and not p2.isEqual(p3) and not p3.isEqual(p1):
						test_tri = Triangle(p1,p2,p3)
						if self.triangleIsDelaunay(test_tri):
							self.addTriangle(test_tri)
		
		#Dodavanje duzi trouglova u graf
		for t in self._triangles:
			if not self.triangleIsDelaunay(t):
				self._triangles.remove(t)
			else:
				self.addEdge(Edge(t._a, t._b))
				self.addEdge(Edge(t._b, t._c))
				self.addEdge(Edge(t._c, t._a))
				
		#Provera da li ima duzi koji se seku
		bad_edges = []
		for e1 in self._edges:
			for e2 in self._edges:
				if not e1.isEqual(e2):
					if e1.edgeIntersection(e2):
						len_e1 = e1.length()
						len_e2 = e2.length()
						if len_e1 >= len_e2:
							bad_edges.append(e1)
							
						else:
							bad_edges.append(e2)
		
		#Izbacivanje iz grafa duzi koji se seku
		for x in bad_edges:
			for y in self._edges:
				if x.isEqual(y):
					self._edges.remove(y)
					continue




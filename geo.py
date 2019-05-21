import numpy as np

from stl import mesh

def sorted_tuple(a, b):
	return (a,b) if a < b else (b,a)

def sorted_tuple_3(a, b, c):
	return (a, b, c) if a < c and b < c and a <= b else (
		(b, a, c) if a < c and b < c and b < a else (
			(a, c, b) if a < b and c < b and a <= c else (
				(c, a, b) if a < b and c < b and c < a else (
					(b, c, a) if b < a and c < a and b <= c else (c, b, a)
				)
			)
		)
	)

class GEO:
	"""docstring for GEO"""
	def __init__(self):
		self.points = {}
		self.edges = set()
		self.faces = set()

	def _add_points(self, point = (0, 0, 0)):
		if point not in self.points.keys():
			self.points[point] = len(self.points)
		return self.points[point]

	def quad(self, v1, v2):
		if len(v1) != len(v2): return
		if len(v1) == 1:
			p1 = self._add_points(v1[0])
			p2 = self._add_points(v2[0])
			self.edges.add(sorted_tuple(v1[0], v2[0]))
		else:
			for i in range(1, len(v1)):
				i0 = self._add_points(v1[i-1])
				i1 = self._add_points(v2[i-1])
				i2 = self._add_points(v1[i])
				i3 = self._add_points(v2[i])

				# self.edges.add(sorted_tuple(i0, i1))
				# self.edges.add(sorted_tuple(i0, i2))
				# self.edges.add(sorted_tuple(i0, i3))
				# self.edges.add(sorted_tuple(i1, i2))
				# self.edges.add(sorted_tuple(i1, i3))
				# self.edges.add(sorted_tuple(i2, i3))

				self.faces.add(sorted_tuple_3(i0, i1, i2))
				# self.faces.add(sorted_tuple_3(i0, i1, i3))
				# self.faces.add(sorted_tuple_3(i0, i2, i3))
				self.faces.add(sorted_tuple_3(i1, i2, i3))

	def save_stl(self, filename = 'geo.stl'):
		# Create the mesh
		faces = np.array(list(self.faces))
		output = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
		points = {}
		for k in self.points.keys():
			t = self.points[k]
			points[t] = np.array(list(k))

		for i, f in enumerate(faces):
			for j in range(3):
				output.vectors[i][j] = points[f[j]]

		# Write the mesh to file "cube.stl"
		output.save(filename)


	def __str__(self):
		return "points size: {}, edges size: {}, faces size: {}".format(len(self.points), len(self.edges), len(self.faces))
		
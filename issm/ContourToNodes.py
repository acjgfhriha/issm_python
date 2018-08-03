from ContourToNodes_python import ContourToNodes_python

def ContourToNodes(x,y,contourname,edgevalue):
	"""
	CONTOURTONODES - flags vertices inside contour

		Usage:
			flags = ContourToNodes(x,y,contourname,edgevalue);

		x,y: list of nodes
		contourname: name of .exp file containing the contours, or resulting structure from call to expread
		edgevalue: integer (0, 1 or 2) defining the value associated to the nodes on the edges of the polygons
		flags: vector of flags (0 or 1), of size nodes
	"""

	#Call mex module
	flags = ContourToNodes_python(x,y,contourname,edgevalue)

	#return
	return flags

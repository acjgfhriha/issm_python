from BamgTriangulate_python import BamgTriangulate_python

def BamgTriangulate(x,y):
	"""
	BAMGTRIANGULATE

	Usage:
		index = BamgTriangulate(x,y)

	index: index of the triangulation
	x,y: coordinates of the nodes
	"""

	# Call mex module
	index = BamgTriangulate_python(x,y)
	# return
	return index

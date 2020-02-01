import bpy
from primitive.primitive import CreatePrimitive, PrimitiveCurveClass
from bsmax.actions import delete_objects

def GetRectangleShapes(width, length, corner):
	Shapes = []
	w, l = width / 2, length / 2
	r, c = corner, corner - (corner * 0.551786)
	if corner == 0:
		p1, p2, p3, p4 = (-w, -l, 0), (-w,  l, 0), ( w,  l, 0), ( w, -l, 0)
		pt1 = (p1, p1, 'VECTOR', p1, 'VECTOR')
		pt2 = (p2, p2, 'VECTOR', p2, 'VECTOR')
		pt3 = (p3, p3, 'VECTOR', p3, 'VECTOR')
		pt4 = (p4, p4, 'VECTOR', p4, 'VECTOR')
		Shapes.append([pt1, pt2, pt3, pt4])
	else:
		pc1, pl1, pr1 = (-w + r, -l, 0), (-w + c, -l, 0), (-w + r, -l, 0)
		pc2, pl2, pr2 = ( w - r, -l, 0), ( w - r, -l, 0), ( w - c, -l, 0)
		pc3, pl3, pr3 = ( w, -l + r, 0), ( w, -l + c, 0), ( w, -l + r, 0)
		pc4, pl4, pr4 = ( w, l - r, 0), ( w, l - r, 0), ( w, l - c, 0)
		pc5, pl5, pr5 = (  w - r, l, 0), (  w - c, l, 0), (  w - r, l, 0) 
		pc6, pl6, pr6 = ( -w + r, l, 0), ( -w + r, l, 0), ( -w + c, l, 0)
		pc7, pl7, pr7 = ( -w, l - r, 0), ( -w, l - c, 0), ( -w, l - r, 0)
		pc8, pl8, pr8 = ( -w, -l + r, 0), ( -w, -l + r, 0), ( -w, -l + c, 0)
		pt1 = (pc1, pl1, 'FREE', pr1, 'VECTOR')
		pt2 = (pc2, pl2, 'VECTOR', pr2, 'FREE')
		pt3 = (pc3, pl3, 'FREE', pr3, 'VECTOR')
		pt4 = (pc4, pl4, 'VECTOR', pr4, 'FREE')
		pt5 = (pc5, pl5, 'FREE', pr5, 'VECTOR')
		pt6 = (pc6, pl6, 'VECTOR', pr6, 'FREE')
		pt7 = (pc7, pl7, 'FREE', pr7, 'VECTOR')
		pt8 = (pc8, pl8, 'VECTOR', pr8, 'FREE')
		Shapes.append([pt1, pt2, pt3, pt4, pt5, pt6, pt7, pt8])
	return Shapes

class Rectangle(PrimitiveCurveClass):
	def __init__(self):
		self.classname = "Rectangle"
		self.finishon = 2
		self.owner = None
		self.data = None
		self.close = True
	def reset(self):
		self.__init__()
	def create(self, ctx):
		shapes = GetRectangleShapes(0, 0, 0)
		self.create_curve(ctx, shapes, self.classname)
		pd = self.data.primitivedata
		pd.classname = self.classname
	def update(self, ctx):
		pd = self.data.primitivedata
		shapes = GetRectangleShapes(pd.width, pd.length, pd.chamfer1)
		self.update_curve(ctx, shapes)
	def abort(self):
		delete_objects([self.owner])

class BsMax_OT_CreateRectangle(CreatePrimitive):
	bl_idname = "bsmax.createrectangle"
	bl_label = "Rectangle (Create)"
	subclass = Rectangle()

	def create(self, ctx, clickpoint):
		self.subclass.create(ctx)
		self.params = self.subclass.owner.data.primitivedata
		self.subclass.owner.location = clickpoint.view
		self.subclass.owner.rotation_euler = clickpoint.orient
	def update(self, ctx, clickcount, dimantion):
		if clickcount == 1:
			self.params.width = dimantion.width
			self.params.length = dimantion.length
			self.subclass.owner.location = dimantion.center
		if clickcount > 0:
			self.subclass.update(ctx)
	def finish(self):
		pass

def rectangle_cls(register):
	c = BsMax_OT_CreateRectangle
	if register: bpy.utils.register_class(c)
	else: bpy.utils.unregister_class(c)

if __name__ == '__main__':
	rectangle_cls(True)

__all__ = ["rectangle_cls", "Rectangle"]
############################################################################
#	This program is free software: you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation, either version 3 of the License, or
#	(at your option) any later version.
#
#	This program is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with this program.  If not, see <https://www.gnu.org/licenses/>.
############################################################################

import bpy
from mathutils import Vector, Matrix
from bpy.types import Menu, Operator

from bsmax.actions import set_origen



class Object_OT_Modify_Pivot(Operator):
	bl_idname = "object.modify_pivotpoint"
	bl_label = "Modify Pivot Point"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(self, ctx):
		return ctx.active_object

	def execute(self, ctx):
		state = ctx.scene.tool_settings.use_transform_data_origin
		ctx.scene.tool_settings.use_transform_data_origin = not state
		return {"FINISHED"}




# TODO add this for mesh objects too
class Object_OT_Pivot_To_First_Point(Operator):
	bl_idname = "object.pivot_to_first_point"
	bl_label = "Pivot to First point"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(self, ctx):
		if len(ctx.selected_objects) > 0:
			for obj in ctx.selected_objects:
				if obj.type != 'CURVE':
					return False
			return True
		else:
			return False
	
	def execute(self,ctx):
		for obj in ctx.selected_objects:
			if len(obj.data.splines)>0:
				if len(obj.data.splines[0].bezier_points)>0:
					old_origin = obj.matrix_world @ obj.data.splines[0].bezier_points[0].co
					delta_origin = obj.data.splines[0].bezier_points[0].co.copy()
					obj.data.transform(Matrix.Translation(-delta_origin))
					obj.matrix_world.translation = old_origin
		return {"FINISHED"}



class Object_OT_Pivot_To_Buttom_Center(Operator):
	bl_idname = "object.pivot_to_buttom_center"
	bl_label = "Pivot to Buttom Center"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(self, ctx):
		return len(ctx.selected_objects) > 0
		
	def pivot_to_buttom_center(self, ctx, obj):
		""" TODO bound_box return value in local coordinate """
		""" need a fast method to get bound box in world space """
		b = [obj.matrix_world @ Vector(v) for v in obj.bound_box]
		min_x = min(b[0][0], b[1][0], b[2][0], b[3][0], b[4][0], b[5][0], b[6][0])
		max_x = max(b[0][0], b[1][0], b[2][0], b[3][0], b[4][0], b[5][0], b[6][0])
		min_y = min(b[0][1], b[1][1], b[2][1], b[3][1], b[4][1], b[5][1], b[6][1])
		max_y = max(b[0][1], b[1][1], b[2][1], b[3][1], b[4][1], b[5][1], b[6][1])
		min_z = min(b[0][2], b[1][2], b[2][2], b[3][2], b[4][2], b[5][2], b[6][2])
		center_x = (min_x + max_x)/2
		center_y = (min_y + max_y)/2
		location = Vector((center_x, center_y, min_z))
		set_origen(ctx, obj, location)

	def execute(self,ctx):
		for obj in ctx.selected_objects:
			self.pivot_to_buttom_center(ctx, obj)
		return {"FINISHED"}



class OBJECT_MT_Set_Pivot_Point(Menu):
	bl_idname = "OBJECT_MT_Set_Pivot_Point"
	bl_label = "Set Pivot Point"

	def draw(self, ctx):
		layout = self.layout
		layout.operator("object.origin_set",
						text="Object to Pivot").type='GEOMETRY_ORIGIN'

		layout.operator("object.origin_set",
						text="Pivot to Object").type='ORIGIN_GEOMETRY'

		layout.operator("object.origin_set",
						text="Pivot to 3D Cursor").type='ORIGIN_CURSOR'

		layout.operator("object.origin_set",
						text="Pivot to Center").type='ORIGIN_CENTER_OF_VOLUME'

		layout.operator("object.origin_set",
						text="Pivot to Geometry").type='ORIGIN_CENTER_OF_MASS'

		layout.operator("object.pivot_to_buttom_center",
						text="Pivot to Buttom Center")

		layout.operator("object.pivot_to_first_point",
						text="Pivot to First BezierPoint")

		layout.separator()

		layout.operator("view3d.snap_cursor_to_selected",
						text="Cursur to Selected")

		layout.operator("view3d.snap_cursor_to_center",
						text="Cursor to World Origin")

		layout.operator("view3d.snap_cursor_to_grid",
						text="Cursor to Grid")

		layout.operator("view3d.snap_cursor_to_active",
						text="Cursor to Active")

		layout.separator()

		layout.operator("view3d.snap_selected_to_grid",
						text="Selection to Gride")

		layout.operator("view3d.snap_selected_to_cursor",
						text="Selection to Cursor (keep offset)"
						).use_offset=False

		layout.operator("view3d.snap_selected_to_cursor",
						text="Selection to Cursor"
						).use_offset=True

		layout.operator("view3d.snap_selected_to_active",
						text="Selection to Active")



def snap_menu(self, ctx):
	layout = self.layout
	layout.separator()
	layout.operator("object.pivot_to_first_point")

classes = [Object_OT_Pivot_To_First_Point,
	Object_OT_Modify_Pivot,
	Object_OT_Pivot_To_Buttom_Center,
	OBJECT_MT_Set_Pivot_Point]

def register_pivot_point():
	for c in classes:
		bpy.utils.register_class(c)
	bpy.types.VIEW3D_MT_snap.append(snap_menu)

def unregister_pivot_point():
	bpy.types.VIEW3D_MT_snap.remove(snap_menu)
	for c in classes:
		bpy.utils.unregister_class(c)

if __name__ == "__main__":
	register_pivot_point()
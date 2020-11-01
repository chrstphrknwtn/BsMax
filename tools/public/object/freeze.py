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
from bpy.types import Operator
from bpy.props import EnumProperty, BoolProperty, StringProperty
from bsmax.actions import set_as_active_object



class Object_TO_Select_By_Name(Operator):
	""" Select """
	bl_idname = "object.select_by_name"
	bl_label = "select object by name"
	name: bpy.props.StringProperty(default="")
	
	@classmethod
	def poll(self, ctx):
		return ctx.mode == 'OBJECT'
	
	def execute(self,ctx):
		bpy.ops.object.select_all(action='DESELECT')
		if self.name != "":
			set_as_active_object(ctx,bpy.data.objects[self.name])
		return{"FINISHED"}



class Object_OT_Freeze(Operator):
	""" Freeze/Unfreeze Objects """
	bl_idname = "object.freeze"
	bl_label = "Freeze/Unfreeze"
	# bl_description = ""

	mode: EnumProperty(default='selection',
		items=[('selection','Freeze Selection',''),
			('unselected','Freeze Unselected',''),
			('clear','Unfreezee All','')])

	def execute(self, ctx):
		if self.mode == 'selection':
			for obj in ctx.selected_objects:
				obj.hide_select = True
		elif self.mode == 'unselected':
			for obj in bpy.data.objects:
				if not obj.select_get():
					obj.hide_select = True
		elif self.mode == 'clear':
			for obj in bpy.data.objects:
				obj.hide_select = False
		self.report({'INFO'},'bpy.ops.object.freeze()')
		return{"FINISHED"}



class Object_OT_Hide(Operator):
	""" Hide/Unhide Objects """
	bl_idname = "object.hide"
	bl_label = "Hide/Unhide"
	# bl_description = ""

	mode: EnumProperty(default='selection',
		items=[('selection','Hide Selection',''),
			('unselected','Hide Unselected',''),
			('clear','Unhide All','')])
	collection: BoolProperty(default=False)

	def execute(self, ctx):
		if self.mode == 'selection':
			for obj in ctx.selected_objects:
				obj.hide_render = True
				obj.hide_viewport = True
		elif self.mode == 'unselected':
			for obj in bpy.data.objects:
				if not obj.select_get():
					obj.hide_render = True
					obj.hide_viewport = True
		elif self.mode == 'clear':
			if self.collection:
				for collection in bpy.data.collections:
					collection.hide_render = False
					collection.hide_viewport = False
			for obj in bpy.data.objects:
				obj.hide_render = False
				obj.hide_viewport = False
			bpy.ops.object.hide_view_clear('INVOKE_DEFAULT')
		self.report({'INFO'},'bpy.ops.object.hide()')
		return{"FINISHED"}




classes = [Object_OT_Freeze, Object_OT_Hide, Object_TO_Select_By_Name]

def register_freeze():
	[bpy.utils.register_class(c) for c in classes]

def unregister_freeze():
	[bpy.utils.unregister_class(c) for c in classes]

if __name__ == "__main__":
	register_freeze()
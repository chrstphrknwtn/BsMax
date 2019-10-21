import bpy

# def active_object_is_ready(ctx):
# 	if ctx.area.type == 'VIEW_3D':
# 		return ctx.active_object != None
# 	return False

# def selection_is_ready(ctx):
# 	if ctx.area.type == 'VIEW_3D':
# 		return True
# 	return False

def is_active_object(ctx, types):
	if ctx.area.type == 'VIEW_3D':
		#if len(ctx.scene.objects) > 0:
		if ctx.active_object != None:
			if ctx.active_object.type in types:
				return True
	return False

def is_active_primitive(ctx):
	active_obj = ctx.active_object
	if active_obj != None:
		if active_obj.type in ['MESH','CURVE']:
			if active_obj.data.primitivedata.classname != "":
				return True
	return False

def is_objects_selected(ctx):
	if ctx.area.type == 'VIEW_3D':
		return len(ctx.selected_objects) > 0

def is_object_mode(ctx):
	if ctx.area.type == 'VIEW_3D':
		if len(ctx.scene.objects) > 0:
			if ctx.object != None:
				if ctx.object.mode == 'OBJECT':
					return True
			else:
				return True
		else:
			return True
	return False

def has_constraint(obj, constrainttype):
	for c in obj.constraints:
		if c.type == constrainttype:
			return True
	return False

def get_active_type(ctx):
	active_obj = ctx.active_object
	return None if active_obj == None else active_obj.type

def get_pref(ctx):
	#print("-->", __name__)
	# to do get addon name from __name__
	return ctx.preferences.addons['BsMax_2_80'].preferences

__all__ = ["is_active_object",
		"is_active_primitive",
		"is_objects_selected",
		"is_object_mode",
		"has_constraint",
		"get_active_type",
		"get_pref"]

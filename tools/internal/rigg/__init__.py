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

from .attach import register_attach, unregister_attach
from .bendy_bone import register_bendy_bone, unregister_bendy_bone
# from .eyetarget import register_eyetarget, unregister_eyetarget
from .joystick import register_joystic, unregister_joystic
from .menu import register_menu, unregister_menu
from .shapekey import register_shapekey, unregister_shapekey
from .wire_parameter import register_wire_parameter, unregister_wire_parameter

def register_rigg():
	register_attach()
	register_bendy_bone()
	# register_eyetarget()
	register_joystic()
	register_shapekey()
	register_wire_parameter()
	register_menu()

def unregister_rigg():
	unregister_attach()
	unregister_bendy_bone()
	# unregister_eyetarget()
	unregister_joystic()
	unregister_shapekey()
	unregister_wire_parameter()
	unregister_menu()
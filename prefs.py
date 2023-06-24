# ##### BEGIN GPL LICENSE BLOCK #####
#
#  <User Interface and Blender Addon for Pidgeon Render Farm>
#    Copyright (C) <2022>  <Crafto1337>
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 3
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

import bpy
from bpy.types import (
    AddonPreferences,
    Context
)
from bpy.props import (
    StringProperty
)


class SRF_APT_Preferences(AddonPreferences):
    bl_idname = __package__

    script_location: StringProperty(
        subtype="FILE_PATH", name="Script Location", description="Executable of Pidgeon Render Farm")

    def draw(self, context: Context):
        layout = self.layout

        layout.prop(self, "script_location")


classes = (
    SRF_APT_Preferences,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

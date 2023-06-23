# ##### BEGIN GPL LICENSE BLOCK #####
#
#  <User Interface and Blender Addon for Red Render Farm>
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
    Panel
)


class SRF_PT_panel(Panel):
    bl_label = "Super Render Farm"
    bl_idname = "SRF_PT_panel"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "render"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        row = layout.row()
        row.prop(scene, "batch_size")

        row = layout.row()
        row.prop(scene, "test_render_time")

        if not scene.test_render_time:
            row = layout.row()
            row.prop(scene, "render_time")

        if bpy.context.scene.render.image_settings.file_format in ["AVI_JPEG", "AVI_RAW", "FFMPEG"]:
            row = layout.row()
            row.prop(scene, "file_format")

        #row = layout.row()
        #row.prop(scene, "video")

        if scene.video:
            row = layout.row()
            row.prop(scene, "fps")

            row = layout.row()
            row.prop(scene, "vrc")

            row = layout.row()
            row.prop(scene, "vrc_value")

            row = layout.row()
            row.prop(scene, "resize")

            if scene.resize:
                row = layout.row()
                row.prop(scene, "res_x")
                #row = layout.row()
                row.prop(scene, "res_y")

        row = layout.row()
        row.prop(scene, "use_sfr")
        row = layout.row()
        row.prop(scene, "use_sid_temporal")

        row = layout.row()
        row.prop(scene, "exit_blender")

        row = layout.row()
        row = layout.row()
        row = layout.row()
        row.operator("superrenderfarm.render", icon="RENDER_RESULT")  # , text="Overwrite")

classes = (
    SRF_PT_panel,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

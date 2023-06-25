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

        layout.label(text="Consecutive Frames per Client:")
        layout.prop(scene, "batch_size", text="")

        if bpy.context.scene.render.image_settings.file_format in ["AVI_JPEG", "AVI_RAW", "FFMPEG"]:
            layout.label(text="File Format")
            layout.prop(scene, "file_format", text="")

        # layout.separator()
        # layout.label(text="Video Settings")

        # row = layout.row()
        # row.prop(scene, "video")

        if scene.video or False:
            # todo: Delete this prop
            # row = layout.row()
            # row.prop(scene, "fps")

            layout.label(text="Encoding Priority")
            row = layout.row()
            row.prop(scene, "vrc", text="")

            row = layout.row()
            row.prop(scene, "vrc_value")  # TODO: Proper label

            row = layout.row()
            row.prop(scene, "resize")

            if scene.resize:
                grid = layout.grid_flow(columns=1, align=True)

                grid.prop(scene, "res_x", text="Resolution X")
                grid.prop(scene, "res_y", text="Resolution Y")

        layout.separator()

        layout.label(text="Other Pidgeon Tools Addons")

        row = layout.row()
        row.prop(scene, "use_sfr")

        # if bpy.app.version >= (3,5):
        #     row = layout.row()
        #     row.prop(scene, "use_sid_temporal")

        layout.separator()

        row = layout.row()
        row.prop(scene, "test_render_time")

        # # # if not scene.test_render_time:
        # # #     row = layout.row()
        # # #     row.prop(scene, "render_time")

        # row = layout.row()
        # row.prop(scene, "exit_blender", text="Exit Blender while rendering")

        row = layout.row()
        # , text="Overwrite")
        row.operator("superrenderfarm.render", icon="RENDER_RESULT")


classes = (
    SRF_PT_panel,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

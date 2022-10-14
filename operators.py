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
    Context,
    Operator,
)

import sys

import subprocess
from subprocess import CREATE_NEW_CONSOLE

import json


import time


class SRF_OT_render_button(Operator):
    bl_idname = "superrenderfarm.render"
    bl_label = "Render with SRF"

    @classmethod
    def poll(cls, context: Context):
        return context.active_object is not None

    def execute(self, context: Context):
        scene = context.scene

        jO = {
            "VER": bpy.app.version_string,
            "FS": scene.frame_start,
            "FE": scene.frame_end,
            "RE": scene.render.engine,
            "FF": scene.render.image_settings.file_format,
            "RT": scene.render_time
        }

        if scene.test_render_time:
            startTime = time.time()
            bpy.ops.render.render()
            jO["RT"] = time.time() - startTime

        if jO["FF"] in ["AVI_JPEG", "AVI_RAW", "FFMPEG"]:
            jO["FF"] = scene.file_format

        jO["V"] = scene.video

        if jO["V"]:
            jO["FPS"] = scene.render.fps  # scene.fps
            jO["VRC"] = scene.vrc
            jO["VRCV"] = scene.vrc_value

            jO["R"] = scene.resize

            if jO["R"]:
                jO["RESX"] = scene.res_x
                jO["RESY"] = scene.res_y

        jS = json.dumps(jO)

        subprocess.call([sys.executable, context.preferences.addons[__package__]
                         .preferences.script_location, "--", jS], creationflags=CREATE_NEW_CONSOLE)

        if scene.exit_blender:
            bpy.ops.wm.quit_blender()

        return {'FINISHED'}


classes = (
    SRF_OT_render_button,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

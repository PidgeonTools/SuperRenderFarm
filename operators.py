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
    bl_label = "Render with PRF"

    @classmethod
    def poll(cls, context: Context):
        return context.active_object is not None

    def execute(self, context: Context):
        scene = context.scene

        jO = {
            "blender_version": bpy.app.version_string,
            "first_frame": scene.frame_start,
            "last_frame": scene.frame_end,
            "frames_total": (scene.frame_end - (scene.frame_start - 1)),
            "render_engine": scene.render.engine,
            "output_file_format": scene.render.image_settings.file_format,
            "time_per_frame": scene.render_time,
            "chunks": scene.chunk_size,
            "frame_step": bpy.context.scene.frame_step,
            #"use_zip": scene.use_zip,
        }

        if scene.use_sfr:
            # Try to call SFR
            try:
                bpy.ops.render.superfastrender_benchmark()
                # Save the new settings
                bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
            except AttributeError:
                print("SuperFastRender is NOT installed!")

        if scene.test_render_time:
            startTime = time.time()
            bpy.ops.render.render()
            jO["time_per_frame"] = time.time() - startTime

        if jO["output_file_format"] in ["AVI_JPEG", "AVI_RAW", "FFMPEG"]:
            jO["output_file_format"] = scene.file_format

        jO["video_generate"] = scene.video

        if jO["video_generate"]:
            jO["video_fps"] = scene.render.fps  # scene.fps
            jO["video_rate_control"] = scene.vrc
            jO["video_rate_control_value"] = scene.vrc_value

            jO["video_resize"] = scene.resize

            if jO["video_resize"]:
                jO["video_x"] = scene.res_x
                jO["video_y"] = scene.res_y

        jS = json.dumps(jO).replace(" ", "")
        jS = jS.replace("False", "false")
        jS = jS.replace("True", "true")

        print(jS)

        subprocess.Popen([context.preferences.addons[__package__]
                         .preferences.script_location, jS], creationflags=CREATE_NEW_CONSOLE)

        if scene.exit_blender:
            bpy.ops.wm.quit_blender()

        return {'FINISHED'}

classes = (
    SRF_OT_render_button,
)

def draw(self, context):
        layout = self.layout
        layout.operator("superrenderfarm.render", icon="RENDER_RESULT")

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.TOPBAR_MT_render.prepend(draw)

def unregister():

    bpy.types.TOPBAR_MT_render.remove(draw)
    
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

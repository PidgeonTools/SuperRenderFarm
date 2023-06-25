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
    Context,
    Operator,
    OperatorProperties,
)

import sys
from os import path

import subprocess
from subprocess import CREATE_NEW_CONSOLE

import json


import time


class SRF_OT_render_button(Operator):
    """Render the current Blender file with Pidgeon Render Farm"""
    bl_idname = "superrenderfarm.render"
    bl_label = "Render with PRF"

    @classmethod
    def poll(cls, context: 'Context'):
        prefs = context.preferences.addons[__package__].preferences

        return path.isfile(prefs.script_location)

    @classmethod
    def description(cls, context: 'Context', properties: 'OperatorProperties') -> str:
        if cls.poll(context):
            return "Render the current Blender file with Pidgeon Render Farm"

        return "Render the current Blender file with Pidgeon Render Farm. \
This requires setting the path to the PRF executable in the addon settings"

    def execute(self, context: Context):
        scene = context.scene

        jO = {
            "blender_version": bpy.app.version_string,
            "full_path_blend": bpy.data.filepath,
            "first_frame": scene.frame_start,
            "last_frame": scene.frame_end,
            "frames_total": (scene.frame_end - (scene.frame_start - 1)),
            "render_engine": scene.render.engine,
            "output_file_format": scene.render.image_settings.file_format,
            "time_per_frame": scene.render_time,
            "batch_size": scene.batch_size,
            "frame_step": bpy.context.scene.frame_step,
            # "use_sid_temporal": scene.use_sid_temporal,
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
            bpy.context.scene.render.filepath = path.join(path.dirname(context.preferences.addons[__package__]
                                                                       .preferences.script_location), "frame_####")
            bpy.context.scene.frame_current = bpy.context.scene.frame_start
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

        # if scene.exit_blender:
        #     bpy.ops.wm.quit_blender()

        # context.window_manager.modal_handler_add(self)

        return {"FINISHED"}

    def modal(self, context, event):
        scene = context.scene
        bpy.ops.object.empty_add(type='PLAIN_AXES')
        empty = bpy.context.view_layer.objects.active
        bpy.context.scene.frame_current = scene.frame_start-1

        for f in range(scene.frame_start, scene.frame_end+1):
            empty.keyframe_insert(data_path='location', frame=f)

        fcurves = empty.animation_data.action.fcurves
        for fcurve in fcurves:
            for keyframe in fcurve.keyframe_points:
                keyframe.type = "EXTREME"

        import threading

        x = threading.Thread(target=thread, args=(context,))
        x.start()

        # return {"PASS_THROUGH"}
        return {"FINISHED"}


def thread(con):
    scene = con.scene
    empty = bpy.context.view_layer.objects.active
    fcurves = empty.animation_data.action.fcurves

    import socket

    srf_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srf_socket.connect(("192.168.1.37", 19186))
    srf_socket.send("SRF".encode())

    frames: int = 0

    while True:
        update: str = srf_socket.recv(1024).decode()
        srf_socket.send("drop".encode())

        parts = update.split('|')

        if parts[1] == "done":
            for fcurve in fcurves:
                fcurve.keyframe_points[int(parts[0])-1].type = "JITTER"
            frames += 1
        elif parts[1] == "rendering":
            for fcurve in fcurves:
                fcurve.keyframe_points[int(parts[0])-1].type = "KEYFRAME"
        else:
            for fcurve in fcurves:
                fcurve.keyframe_points[int(parts[0])-1].type = "EXTREME"

        bpy.context.scene.frame_current = scene.frame_start-1
        for keyframe in fcurves[0].keyframe_points:
            if keyframe.type == "JITTER":
                bpy.context.scene.frame_current = bpy.context.scene.frame_current+1
            else:
                break

        if frames >= (scene.frame_end - (scene.frame_start - 1)):
            break

    srf_socket.close()


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

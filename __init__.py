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
from bpy.props import (
    StringProperty,
    BoolProperty,
    IntProperty,
    FloatProperty,
    EnumProperty
)
from bpy.types import (
    PropertyGroup,
    Panel,
    AddonPreferences,
    Operator
)


bl_info = {
    "name": "Super Render Farm",
    "author": "Crafto1337, Pidgeon Tools, Blender Defender",
    "version": (0, 0, 1),
    "blender": (2, 93, 0),
    # TODO: Maybe find a shorter description. This description is very long.
    "description": "Setup the render farm directy from Blender without having to start and setting it up manually",
    "location": "Properties > Render > Super Render Farm",
    "warning": "",
    "tracker_url": "https://www.github.com/PidgeonTools/SuperRenderFarm/issues",
    "wiki_url": "https://www.github.com/PidgeonTools/SuperRenderFarm",
    "endpoint_url": "https://raw.githubusercontent.com/PidgeonTools/SAM-Endpoints/main/SuperRenderFarm.json",
    "category": "Render",
}

# class properties(PropertyGroup):
#     string: StringProperty(
#         name = "String",
#         description = "Test",
#         default = ""
#     )
    
#     bool: BoolProperty(
#         name = "Bool",
#         description = "Test",
#         default = False
#     )

#     int: IntProperty(
#         name = "Int",
#         description = "Test",
#         default = 0,
#         min = 0,
#         max = 10
#     )

#     float: FloatProperty(
#         name = "Float",
#         description = "Test",
#         default = 0.0,
#         min = 0.0,
#         max = 10.0
#     )
    
#     enum: EnumProperty(
#         name = "Enum",
#         description = "",
#         items = [
#                 ('OP1', "Test", "")
#         ],
#         #update=LoadPreset
#     )

def register_properties():
    s = bpy.types.Scene
    #-----  -----#
    
    s.test_render_time = BoolProperty(
        name = "Test Render Time",
        description = "Render one test frame to approximate the render time per frame",
        default = False
    )

    s.render_time = IntProperty(
        name = "Render Time",
        description = "",
        default = 0,
        min = 0,
        #max = 10
    )

    s.file_format = EnumProperty(
        name = "File Format",
        description = "Because you have a video format selected, you now have the option to change that.",
        items = [
                ('PNG', "PNG", ""),
                ('BMP', "BMP", ""),
                #('IRIZ', "IRIZ", ""),
                ('IRIS', "Iris", ""),
                ('JPEG', "JPEG", ""),
                ('RAWTGA', "Targa RAW", ""),
                ('TGA', "Targa", ""),

                ('WEBP', "WebP", "Experimental!"),
                ('JP2', "JPEG 2000", "Experimental!"),
                #('DDS', "DDS", "Experimental!"),
                ('DPX', "DPX", "Experimental!"),
                ('CINEON', "Cineon", "Experimental!"),
                ('OPEN_EXR_MULTILAYER', "OpenEXR Multilayer", "Experimental!"),
                ('OPEN_EXR', "OpenEXR", "Experimental!"),
                ('TIFF', "TIFF", "Experimental!"),
                ('HDR', "Radiance HDR", "Experimental!"),
        ],

        #         
        #update=LoadPreset
    )
    
    s.video = BoolProperty(
        name = "Generate Video",
        description = "",
        default = False
    )
    
    s.fps = IntProperty(
        name = "Video FPS",
        description = "",
        default = 24,
        min = 1,
        #max = 10
    )
    
    s.vrc = EnumProperty(
        name = "Video Rate Control",
        description = "",
        items = [
                ('CBR', "CBR", "Constant Bitrate"),
                ('CRF', "CRF", "Constant Quality")
        ],
        #update=LoadPreset
    )
    
    s.vrc_value = IntProperty(
        name = "Video Rate Control Value",
        description = "Test",
        default = 0,
        min = 0,
        #max = 10
    )
    
    s.resize = BoolProperty(
        name = "Resize the video",
        description = "",
        default = False
    )
    
    s.res_x = IntProperty(
        name = "New video width",
        description = "Test",
        default = 1920,
        min = 1,
        #max = 10
    )
    
    s.res_y = IntProperty(
        name = "New video height",
        description = "Test",
        default = 1080,
        min = 1,
        #max = 10
    )

    s.exit_blender = BoolProperty(
        name = "Exit Blender",
        description = "",
        default = False
    )

class SRF_OT_render_button(Operator):
    bl_idname = "superrenderfarm.render"
    bl_label = "Render with SRF"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        render_srf(context)

        return {'FINISHED'}

def render_srf(context):
    scene = context.scene
    
    import json
    import sys
    import os
    import time
    import subprocess
    from subprocess import CREATE_NEW_CONSOLE

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
        jO["FPS"] = scene.render.fps #scene.fps
        jO["VRC"] = scene.vrc
        jO["VRCV"] = scene.vrc_value

        jO["R"] = scene.resize

        if jO["R"]:
            jO["RESX"] = scene.res_x
            jO["RESY"] = scene.res_y

    jS = json.dumps(jO)

    subprocess.call([sys.executable, context.preferences.addons[__package__].preferences.script_location, "--", jS], creationflags=CREATE_NEW_CONSOLE)

    if scene.exit_blender:
        bpy.ops.wm.quit_blender()
 
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
        row.prop(scene, "test_render_time")

        if not scene.test_render_time:
            row = layout.row()
            row.prop(scene, "render_time")

        if bpy.context.scene.render.image_settings.file_format in ["AVI_JPEG", "AVI_RAW", "FFMPEG"]:
            row = layout.row()
            row.prop(scene, "file_format")
        
        row = layout.row()
        row.prop(scene, "video")
        
        if scene.video:
            #row = layout.row()
            #row.prop(scene, "fps")
            
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
            row.prop(scene, "exit_blender")

        row = layout.row()
        row = layout.row()
        row = layout.row()
        row.operator("superrenderfarm.render")#, text="Overwrite")

class SRF_APT_Preferences(AddonPreferences):
    bl_idname = __package__

    script_location: StringProperty(subtype="DIR_PATH")

    def draw(self, context: bpy.types.Context):
        layout = self.layout

        layout.prop(self, "script_location")

classes = (
    # properties,
    SRF_OT_render_button,
    SRF_PT_panel,
    SRF_APT_Preferences
)

def register():
    register_properties()

    for cls in classes:
        bpy.utils.register_class(cls)

    
    # bpy.types.Scene.properties = bpy.props.PointerProperty(type = properties)


def unregister():
    for cls in reversed(classes):
        bpy.utils.register_class(cls)
    
    # del bpy.types.Scene.properties


if __name__ == "__main__":
    register()

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
    "author": "Crafto1337, Pidgeon Tools",
    "version": (0, 1),
    "blender": (2, 93, 0),
    "description": "Setup the render farm directy from Blender without having to start and setting it up manually",
    "warning": "",
    "tracker_url": "https://www.github.com/PidgeonTools/SuperRenderFarm/issues",
    "wiki_url": "https://www.github.com/PidgeonTools/SuperRenderFarm",
    "category": "Render",
}

class properties(PropertyGroup):
    string: StringProperty(
        name = "String",
        description = "Test",
        default = ""
    )
    
    bool: BoolProperty(
        name = "Bool",
        description = "Test",
        default = False
    )

    int: IntProperty(
        name = "Int",
        description = "Test",
        default = 0,
        min = 0,
        max = 10
    )

    float: FloatProperty(
        name = "Float",
        description = "Test",
        default = 0.0,
        min = 0.0,
        max = 10.0
    )
    
    enum: EnumProperty(
        name = "Enum",
        description = "",
        items = [
                ('OP1', "Test", "")
        ],
        #update=LoadPreset
    )
    
    #-----  -----#
    
    test_render_time: BoolProperty(
        name = "Test Render Time",
        description = "Render one test frame to approximate the render time per frame",
        default = False
    )

    render_time: IntProperty(
        name = "Render Time",
        description = "",
        default = 0,
        min = 0,
        #max = 10
    )

    file_format: EnumProperty(
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
    
    video: BoolProperty(
        name = "Generate Video",
        description = "",
        default = False
    )
    
    fps: IntProperty(
        name = "Video FPS",
        description = "",
        default = 24,
        min = 1,
        #max = 10
    )
    
    vrc: EnumProperty(
        name = "Video Rate Control",
        description = "",
        items = [
                ('CBR', "CBR", "Constant Bitrate"),
                ('CRF', "CRF", "Constant Quality")
        ],
        #update=LoadPreset
    )
    
    vrc_value: IntProperty(
        name = "Video Rate Control Value",
        description = "Test",
        default = 0,
        min = 0,
        #max = 10
    )
    
    resize: BoolProperty(
        name = "Resize the video",
        description = "",
        default = False
    )
    
    res_x: IntProperty(
        name = "New video width",
        description = "Test",
        default = 1920,
        min = 1,
        #max = 10
    )
    
    res_y: IntProperty(
        name = "New video height",
        description = "Test",
        default = 1080,
        min = 1,
        #max = 10
    )

    exit_blender: BoolProperty(
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
    props = scene.properties
    
    import json
    import sys
    import os
    import time
    import subprocess
    from subprocess import CREATE_NEW_CONSOLE

    jO = {
    "VER": bpy.app.version_string,
    "FS": bpy.context.scene.frame_start,
    "FE": bpy.context.scene.frame_end,
    "RE": bpy.context.scene.render.engine,
    "FF": bpy.context.scene.render.image_settings.file_format,
    "RT": props.render_time
    }

    if props.render_time_test:
        startTime = time.time()
        bpy.ops.render.render()
        jO["RT"] = time.time() - startTime

    if jO["FF"] in ["AVI_JPEG", "AVI_RAW", "FFMPEG"]:
        jO["FF"] = props.file_format

    jO["V"] = props.video

    if jO["V"]:
        jO["FPS"] = bpy.context.scene.render.fps#props.fps
        jO["VRC"] = props.vrc
        jO["VRCV"] = props.vrc_value

        jO["R"] = props.resize

        if jO["R"]:
            jO["RESX"] = props.res_x
            jO["RESY"] = props.res_y

    jS = json.dumps(jO)

    subprocess.call([sys.executable, context.preferences.addons["Super Render Farm"].preferences.script_location, "--", jS], creationflags=CREATE_NEW_CONSOLE)

    if props.exit_blender:
        bpy.ops.wm.quit_blender()
 
class SRF_PT_panel(Panel):
    bl_label = "Super Render Farm"
    bl_idname = "OBJECT_SRF_PANEL"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "render"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        props = scene.properties

        row = layout.row()
        row.prop(props, "test_render_time")

        if not props.test_render_time:
            row = layout.row()
            row.prop(props, "render_time")

        if bpy.context.scene.render.image_settings.file_format in ["AVI_JPEG", "AVI_RAW", "FFMPEG"]:
            row = layout.row()
            row.prop(props, "file_format")
        
        row = layout.row()
        row.prop(props, "video")
        
        if props.video:
            #row = layout.row()
            #row.prop(props, "fps")
            
            row = layout.row()
            row.prop(props, "vrc")
            
            row = layout.row()
            row.prop(props, "vrc_value")
            
            row = layout.row()
            row.prop(props, "resize")
            
            if props.resize:
                row = layout.row()
                row.prop(props, "res_x")
                #row = layout.row()
                row.prop(props, "res_y")

            row = layout.row()
            row.prop(props, "exit_blender")

        row = layout.row()
        row = layout.row()
        row = layout.row()
        row.operator("superrenderfarm.render")#, text="Overwrite")

class SRF_APT_Preferences(AddonPreferences):
    bl_idname = __package__

    script_location:StringProperty(subtype="DIR_PATH")

    def draw(self, context: bpy.types.Context):
        layout = self.layout

        layout.prop(self, "script_location")

classes = (
    properties,
    SRF_OT_render_button,
    SRF_PT_panel,
    SRF_APT_Preferences
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
    bpy.types.Scene.properties = bpy.props.PointerProperty(type = properties)


def unregister():
    for cls in reversed(classes):
        bpy.utils.register_class(cls)
    
    del bpy.types.Scene.properties


if __name__ == "__main__":
    register()

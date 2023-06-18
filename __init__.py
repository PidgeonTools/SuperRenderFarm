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
    BoolProperty,
    IntProperty,
    EnumProperty
)

from . import (
    operators,
    panels,
    prefs
)


bl_info = {
    "name": "Super Render Farm",
    "author": "Pidgeon Tools: Crafto1337, Blender Defender",
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


def register_properties():
    s = bpy.types.Scene
    #-----  -----#

    s.chunk_size = IntProperty(
        name="Chunk size",
        description="Specify the chunk size (recommended to use with ZIP)",
        default=1,
        min=1
    )

    s.use_zip = BoolProperty(
        name="Use zip",
        description="Use zip to save some bandwitdh",
        default=False
    )

    s.test_render_time = BoolProperty(
        name="Test Render Time",
        description="Render one test frame to approximate the render time per frame",
        default=False
    )

    s.render_time = IntProperty(
        name="Render Time",
        description="",
        default=0,
        min=0,
        #max = 10
    )

    s.file_format = EnumProperty(
        name="File Format",
        description="Because you have a video format selected, you now have the option to change that.",
        items=[
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
        # update=LoadPreset
    )

    s.video = BoolProperty(
        name="Generate Video",
        description="",
        default=False
    )

    s.fps = IntProperty(
        name="Video FPS",
        description="",
        default=24,
        min=1,
        #max = 10
    )

    s.vrc = EnumProperty(
        name="Video Rate Control",
        description="",
        items=[
            ('CBR', "CBR", "Constant Bitrate"),
            ('CRF', "CRF", "Constant Quality")
        ],
        # update=LoadPreset
    )

    s.vrc_value = IntProperty(
        name="Video Rate Control Value",
        description="Test",
        default=0,
        min=0,
        #max = 10
    )

    s.resize = BoolProperty(
        name="Resize the video",
        description="",
        default=False
    )

    s.res_x = IntProperty(
        name="New video width",
        description="Test",
        default=1920,
        min=1,
        #max = 10
    )

    s.res_y = IntProperty(
        name="New video height",
        description="Test",
        default=1080,
        min=1,
        #max = 10
    )

    s.use_sfr = BoolProperty(
        name="Opimize with SFR",
        description="Use SuperFastRender to find ideal render settings (sampples in relation to time).",
        default=False
    )

    s.exit_blender = BoolProperty(
        name="Exit Blender",
        description="Exit Blender while rendering.",
        default=False
    )


modules = (
    operators,
    panels,
    prefs
)


def register():
    register_properties()

    for mod in modules:
        mod.register()


def unregister():
    for mod in reversed(modules):
        mod.unregister()


# if __name__ == "__main__":
#     register()

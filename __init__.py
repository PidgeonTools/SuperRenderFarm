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
    "name": "Super Render Farm (SRF)",
    "author": "Pidgeon Tools: Crafto1337, Blender Defender",
    "version": (0, 0, 1),
    "blender": (2, 93, 0),
    "description": "Blender Addon for Pidgeon Render Farm",
    "location": "Properties > Render > Super Render Farm",
    "warning": "",
    "tracker_url": "https://www.github.com/PidgeonTools/SuperRenderFarm/issues",
    "wiki_url": "https://www.github.com/PidgeonTools/SuperRenderFarm",
    "endpoint_url": "https://raw.githubusercontent.com/PidgeonTools/SAM-Endpoints/main/SuperRenderFarm.json",
    "category": "Render",
}


def register_properties():
    s = bpy.types.Scene

    s.batch_size = IntProperty(
        name="Batch size",
        description="How many frames a Client renders before sending them back",
        default=1,
        min=1
    )

    s.test_render_time = BoolProperty(
        name="Approximate Render Time",
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
        description="Rendering videos is currently not possible with Pidgeon Render Farm, please specify an alternative file format to use for rendering",
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
        name="Encoding Priority",
        description="Whether the encoder should prioritize constant quality or constant file size",
        items=[
            ('CBR', "File Size", "Constant Bitrate/File Size"),
            ('CRF', "Quality", "Constant Quality")
        ],
        default="CRF"
        # update=LoadPreset
    )

    s.vrc_value = IntProperty(
        name="Encoding Priority Value",
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
        subtype="PIXEL"
        #max = 10
    )

    s.res_y = IntProperty(
        name="New video height",
        description="Test",
        default=1080,
        min=1,
        subtype="PIXEL"
        #max = 10
    )

    s.use_sfr = BoolProperty(
        name="Opimize with SFR",
        description="Use SuperFastRender to find ideal render settings (samples in relation to time)",
        default=False
    )

    s.use_sid_temporal = BoolProperty(
        name="Denoise with SID Temporal",
        description="Use SuperImageDenoiser Temporal for denoising",
        default=False
    )

    s.exit_blender = BoolProperty(
        name="Exit Blender",
        description="Exit Blender while rendering",
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

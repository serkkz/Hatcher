# -*- coding: utf-8 -*-
import bpy
from bpy.props import *
from bpy.types import (PropertyGroup)

class Edit_UV(bpy.types.Operator):
    bl_idname = "mesh.edit_uv"
    bl_label = "Generator"

    def invoke(self, context, event):

        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.screen.userpref_show('INVOKE_DEFAULT')
        bpy.context.area.type = 'IMAGE_EDITOR'
        bpy.context.area.ui_type = 'UV'

        return {'FINISHED'}
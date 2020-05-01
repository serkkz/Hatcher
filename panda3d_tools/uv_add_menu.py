# -*- coding: utf-8 -*-
import bpy
from bpy.props import *
from bpy.types import (PropertyGroup)

class Unwrap_menu(bpy.types.Menu):

    bl_idname = "UNWRAP_MENU_MT_menu"
    bl_label = "UV Mapping"

    def draw(self, context):
        layout = self.layout

        layout.operator("uv.reset")
        
        layout.separator()
        
        layout.operator_context = 'INVOKE_REGION_WIN'
        layout.operator("uv.project_from_view").scale_to_bounds = False
        layout.operator("uv.project_from_view", text="Project from View (Bounds)").scale_to_bounds = True
        
        layout.separator()  
        
        layout.operator_context = 'EXEC_REGION_WIN'
        layout.operator("uv.cube_project")
        layout.operator("uv.cylinder_project")
        layout.operator("uv.sphere_project") 
        
        layout.separator()      
        
        layout.operator_context = 'INVOKE_DEFAULT'
        layout.operator("uv.smart_project")
        layout.operator("uv.lightmap_pack")
        layout.operator("uv.follow_active_quads")
        layout.operator("uv.unwrap")
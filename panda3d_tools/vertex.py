# -*- coding: utf-8 -*-
import bpy
from bpy.props import *
from bpy.types import (PropertyGroup)

class Vertexs(bpy.types.Panel):
    bl_idname = "VERTEX_PT_Panel"
    bl_label = "Vertex"
    bl_category = "Hather"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return bpy.context.tool_settings.mesh_select_mode[0] == True

    def draw(self, context):
        layout = self.layout
        
        me = bpy.context.object.data

        # Проверка есть ли активный объект
        if bpy.context.active_object != None:
        
            if bpy.context.active_object.type == "MESH":

                # Общий фрейм для атрибутов с обводкой
                frameUV = layout.box()
                
                # Проверка есть ли текстурные координаты у объекта
                if bpy.context.object.data.uv_layers.active != None:

                    frameUV.label(text="UV coordinates: Yes")   
                    
                    frameUV_edit = frameUV.row()
                    
                    frameUV_edit.template_list("MESH_UL_uvmaps", "uvmaps", me, "uv_layers", me.uv_layers, "active_index", rows=2)

                    col = frameUV_edit.column(align=True)
                    
                    # Добавить слой UV
                    col.operator("mesh.uv_texture_add", icon='ADD', text="")  

                    # Удалить слой UV
                    col.operator("mesh.uv_texture_remove", icon='REMOVE', text="")
                    
                    # Кнопка редактирования UV
                    frameUV.operator("mesh.edit_uv", text="Edit map UV")

                else:
                    frameUV.label(text="UV coordinates: No") 
                    
                    # Добавить слой UV
                    frameUV.operator("mesh.uv_texture_add", text="Add map")
                    
            else:
                layout.label(text='Select the type of mesh object')
        else:
            layout.label(text='active object is not selected')

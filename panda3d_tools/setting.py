# -*- coding: utf-8 -*-
import bpy
import os
from bpy.props import *
from bpy.types import (PropertyGroup)

class Setting(bpy.types.Panel):

    bl_idname = "SETTING_PT_Panel"
    bl_label = "Setting export"
    bl_category = "Hatcher"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    
    def draw(self, context):
        #Общий слой для элементов.
        layout = self.layout
        
        # Выбор директории где установленна панда.
        layout.prop(context.scene.hatcher, 'dir_Panda3D_Bin', text='Directory folder bin')
        
        # Выбор директории проекта.
        layout.prop(context.scene.hatcher, 'dir_path_project', text='Directory project')

        if bpy.context.active_object != None:
            if bpy.context.active_object.type == "MESH":

                # Выбор директории для сохранения файла.
                layout.prop(context.object.hatcher, 'catalog_model', text='Relative catalog model')
                
                # Поле для задания имени файла.
                layout.prop(context.object, "name", text='Name file')

                # Проверяем указан ли путь экспорта у объекта.
                if context.scene.hatcher.dir_path_project != '':
                
                    # Вывод листа с осями верха для модели.
                    layout.prop(bpy.context.active_object.hatcher, "coordinatesystem", text="Coordinate system")
                
                    row = layout.row()
                    sub = row.row(align=True)
                    # Кнопка экспорта модели.
                    sub.operator("mesh.generate_egg", text="Export model")
                    # Кнопка экспорта сцены.
                    sub = row.row(align=True)
                    sub.operator("mesh.pass_operator", text="Export animation")
                    sub.enabled = False
                    sub = row.row(align=True)
                    sub.operator("mesh.pass_operator", text="Export level")
                    sub.enabled = False
                    sub = row.row(align=True)
                    sub.operator("mesh.pass_operator", text="Export a curve")
                    sub.enabled = False

                    # Проверяем указан ли путь установленой панды.
                    if bpy.context.scene.hatcher.dir_Panda3D_Bin != '':
                        
                        # Адрес утилиты конвертора в bam
                        ful_adress_util_egg_bam = os.path.join(bpy.context.scene.hatcher.dir_Panda3D_Bin, "egg2bam.exe")

                        util_list = self.layout.split()

                        # Проверка существования файла утилиты конвертации.
                        if os.path.isfile(ful_adress_util_egg_bam):
                        
                            convert_bam = util_list.row()
                            convert_bam.prop(bpy.context.active_object.hatcher, "chexbox_convert_bam", text = "Convert to bam")
                            convert_bam.active = True
                            
                        else:
                            util_list.label(text='egg2bam.exe not found')
                            
                        # Адрес утилиты просмотра.
                        ful_adress_util_view = os.path.join(bpy.context.scene.hatcher.dir_Panda3D_Bin, "pview.exe")

                        # Проверка существования файла утилиты просмотра.
                        if os.path.isfile(ful_adress_util_view):
                        
                            view_model = util_list.row()
                            view_model.prop(bpy.context.active_object.hatcher, "chexbox_view_model", text = "View model")
                            view_model.active = True
                            
                        else:
                            util_list.label(text='pview.exe not found')
                    else:
                        layout.label(text='For access to utils specify the installation path panda3d')
                else:
                    layout.label(text='Set directory project !!!')
            else:
                layout.label(text='Select the type of mesh object')
        else:
            layout.label(text='active object is not selected')
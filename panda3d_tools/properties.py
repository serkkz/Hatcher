# -*- coding: utf-8 -*-
import bpy
from bpy.props import *
from bpy.types import (PropertyGroup)
from bpy.types import UIList

# Xранит пользовательские данные для объектов.
class Hatcher_obj(PropertyGroup):

    # Переменная для хранения адреса egg.
    catalog_model: StringProperty(subtype='DIR_PATH', default = 'Object')

    chexbox_convert_bam: BoolProperty(name="", description="Convert to bam", default=False)
    
    chexbox_view_model: BoolProperty(name="", description="View model", default=False)

    coordinatesystem: EnumProperty(items=(('Z-Up', "Z-Up", ""), ('Y-Up', "Y-Up", "")), default='Z-Up')
    
    collide_type: EnumProperty(items=(('Plane', "Plane", ""), ('Polygon', "Polygon", ""), ('Polyset', "Polyset", ""), ('Sphere', "Sphere", ""), ('Box', "Box", ""), ('InvSphere', "InvSphere", ""), ('Tube', "Tube", ""), ('None', "None", "")), default='None')

    collide_flag_1: EnumProperty( items=(('event', "event", ""), ('intangible', "intangible", ""), ('descend', "descend", ""), ('keep', "keep", ""), ('level', "level", ""), ('None', "None", "")), default='None')                    
    collide_flag_2: EnumProperty(items=(('event', "event", ""), ('intangible', "intangible", ""), ('descend', "descend", ""), ('keep', "keep", ""), ('level', "level", ""), ('None', "None", "")), default='None')
    collide_flag_3: EnumProperty(items=(('event', "event", ""), ('intangible', "intangible", ""), ('descend', "descend", ""), ('keep', "keep", ""), ('level', "level", ""), ('None', "None", "")), default='None')
    collide_flag_4: EnumProperty(items=(('event', "event", ""), ('intangible', "intangible", ""), ('descend', "descend", ""), ('keep', "keep", ""), ('level', "level", ""), ('None', "None", "")), default='None')
    collide_flag_5: EnumProperty(items=(('event', "event", ""), ('intangible', "intangible", ""), ('descend', "descend", ""), ('keep', "keep", ""), ('level', "level", ""), ('None', "None", "")), default='None')
    
    zones_index: IntProperty()
    
    # Переменная для хранения маски коллизии.
    collide_name: StringProperty()
    # Переменная для хранения маски коллизии.
    collide_mask: StringProperty( default = '1048575' )
    # Переменная для хранения маски, с какой маской происходит коллизия.
    from_collide_mask: StringProperty( default = '1048575' )
    # Переменная для хранения маски, от какой маски происходит коллизия.
    into_collide_mask: StringProperty( default = '1048575' )

# Xранит пользовательские даные для сцены
class Hatcher_scene(PropertyGroup):

    # Переменная для хранения адреса установленный панды.
    dir_Panda3D_Bin: StringProperty(subtype='DIR_PATH')
    
    # Переменная для хранения адреса проекта.
    dir_path_project: StringProperty(subtype='DIR_PATH')

class Hatcher_list_egg_add(PropertyGroup):

    path_egg: StringProperty(subtype='FILE_PATH')

# Хранит пользовальскте данные для полигонов.
class Hatcher_faces(PropertyGroup):

    faces_name_buffer:StringProperty()
    faces_name:StringProperty()
    
    faces_materal_buffer:StringProperty()
    faces_materal:StringProperty()
bl_info = {"name": "Tools", 
           "description": "Tools", 
           "author": "serg-kkz", 
           "version": (0, 6),
           "blender": (2, 80, 0),
           "location": "UI", 
           "warning": "alpha testing", 
           "wiki_url": "https://github.com/serkkz/Hatcher/wiki", 
           "tracker_url": "https://github.com/serkkz/Hatcher/issues",
           "category": "Panda3D"}

import bpy, bpy_types, bmesh
from bpy.props import *
from bpy.types import PropertyGroup

from .panda3d_tools.setting import Setting
from .panda3d_tools.collide import Collide
from .panda3d_tools.vertex import Vertexs
from .panda3d_tools.polygon import Polygons

from .panda3d_tools.properties import  Hatcher_obj, Hatcher_scene, Hatcher_list_egg_add, Hatcher_faces

from .panda3d_tools.list_hather import Hatcher_list_egg
from .panda3d_tools.include_egg import Include, Add_file, Del_file

from .panda3d_tools.uv_add_menu import Unwrap_menu
from .panda3d_tools.edit_map_uv import Edit_UV

from .panda3d_tools.export_standart import Export_egg
from .panda3d_tools.apply_name_faces import Apply_name_faces, Pass_operator, Delete_group, Deselect_face, Select_face

classes = (
    Setting,
    Collide,
    Vertexs,
    Polygons,

    Hatcher_obj,
    Hatcher_scene,
    Hatcher_list_egg_add,
    Hatcher_faces,
    
    Hatcher_list_egg,
    Include,
    Add_file,
    Del_file,
    
    Unwrap_menu,
    Edit_UV,
    
    Export_egg,
    
    Apply_name_faces,
    Pass_operator,
    Delete_group,
    Deselect_face,
    Select_face,
)

def register():

    from bpy.utils import register_class
    
    for cls in classes:
        register_class(cls)
        
    bpy.types.Scene.hatcher = PointerProperty(type=Hatcher_scene)
    bpy.types.Object.hatcher = PointerProperty(type=Hatcher_obj)
    bpy.types.Object.hatcher_list_egg_groop = CollectionProperty(type=Hatcher_list_egg_add)
    bpy.types.WindowManager.hatcher = PointerProperty(type = Hatcher_faces)

def unregister():

    from bpy.utils import unregister_class
    
    for cls in reversed(classes):
        unregister_class(cls)
        
    del bpy.types.Scene.hatcher
    del bpy.types.Object.hatcher
    del bpy.types.Object.hatcher_list_egg_groop
    del bpy.types.WindowManager.hatcher
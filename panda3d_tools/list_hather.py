import bpy
from bpy.props import IntProperty, CollectionProperty
from bpy.types import Panel, UIList

class Hatcher_list_egg(bpy.types.UIList):

    bl_idname = "HATCHER_LIST_EGG_UL_List"
    bl_label = "EGG List"

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):

        layout.prop(item, "path_egg", text="File path egg")
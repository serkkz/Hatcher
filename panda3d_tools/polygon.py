import bpy, bmesh
from bpy.props import *
from bpy.types import (PropertyGroup)
from .globals import selfaces

class Polygons(bpy.types.Panel):
    bl_idname = "POLYGON_PT_Panel"
    bl_label = "Polygon"
    bl_category = "Hatcher"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        if context.active_object.type == "MESH":
            if context.active_object.mode == "EDIT":
                if context.tool_settings.mesh_select_mode[2] == True:
                    return True

    def draw(self, context):
        
        me = context.edit_object.data
        bm = bmesh.from_edit_mesh(me)
        
        bm.faces.ensure_lookup_table()
        
        # Добавляем выбраные лица в список.
        for f in bm.faces:
            if f.select:
                selfaces.append(f.index)
        bmesh.update_edit_mesh(me)
        
        try:
            name_face = bm.faces.layers.string['name']
        except:
            name_face = bm.faces.layers.string.new('name')
            
            for face in bm.faces:
                face[name_face] = bytes("", 'utf-8')

        row = self.layout.row()
        row.enabled = False
        
        row.prop(context.window_manager.hatcher, "faces_name", text = "Name face")
        
        # Если выбранных лиц больше одного.
        if len(selfaces) >= 2:
            context.window_manager.hatcher.faces_name = "?"
            row = self.layout.row()
            row.prop(context.window_manager.hatcher, "faces_name_buffer", text = "Enter a name for the group")
        else:
            if not selfaces:
                context.window_manager.hatcher.faces_name = ''
            else:
                context.window_manager.hatcher.faces_name = bm.faces[selfaces[0]][name_face].decode("utf-8")
                
            row = self.layout.row()
            row.prop(context.window_manager.hatcher, "faces_name_buffer", text = "Enter a name face")

        text_name = "Apply"
        row_button = self.layout.row()
        
        if not selfaces:
            row_button.enabled = False
            text_name = "Select faces and enter a name"
        else:
            if context.window_manager.hatcher.faces_name_buffer == '':
                row_button.enabled = False
                text_name = "Select faces and enter a name"
                
        send = row_button.operator("mesh.apply_name_faces", text=text_name)
        send.index_list = " ".join(str(x) for x in selfaces)
 
        row = self.layout.row()
        row.template_list("MESH_UL_vgroups", "", context.object, "vertex_groups", context.object.vertex_groups, "active_index", rows=2)

        if context.object.vertex_groups and (context.object.mode == 'EDIT' and context.object.type == 'MESH'):
            row = self.layout.row()
            sub = row.row(align=True)
            send_select = sub.operator("mesh.select_face", text="Select")
            send_select.index_list = " ".join(str(x) for x in selfaces)
            
            sub = row.row(align=True)
            send_delete = sub.operator("mesh.deselect_face", text="Delete")
            send_delete.index_list = " ".join(str(x) for x in selfaces)
            send_delete.bool_delete = 1

        selfaces.clear()
        
        bmesh.update_edit_mesh(me)
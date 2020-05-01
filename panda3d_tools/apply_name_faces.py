import bpy
import bmesh
from .globals import selfaces

# Класс для обновления и назначения имени полигонов.
# Так же создание группы лиц для быстрого выбора.
class Apply_name_faces(bpy.types.Operator):
    '''Set a name for a group of polygons'''
    bl_idname = "mesh.apply_name_faces"
    bl_label = "Apply_name_faces"

    index_list: bpy.props.StringProperty()

    def execute(self, context):

        me = context.edit_object.data
        bm = bmesh.from_edit_mesh(me)

        bm.faces.ensure_lookup_table()

        # Создаем на "лету" новые свойства для лиц.
        try:
            name_face = bm.faces.layers.string['name']
        except:
            name_face = bm.faces.layers.string.new('name')
            for face in bm.faces:
                face[name_face] = bytes("", 'utf-8')

        # Если имя строчки было пустое.
        if context.window_manager.hatcher.faces_name_buffer == '':
            pass
        else:

            # Проходим по элементам в строчке, преобразовав её в список.
            for element in self.index_list.split():
                bm.faces[int(element)][name_face] = bytes(context.window_manager.hatcher.faces_name_buffer, 'utf-8')
            bmesh.update_edit_mesh(me)
            
            # Создаем группу полигонов, для быстрого доступа.
            face = context.object.vertex_groups.new()
            face.name = context.window_manager.hatcher.faces_name_buffer
            bpy.ops.object.vertex_group_assign()
            face.lock_weight = True

            # Нужно обновить режим моде, для внесения изменений на объекте.
            if bpy.context.mode=='EDIT_MESH':
                context.object.update_from_editmode()

            # Нужно удалить пустые группы, которые не содержат полигонов.
            del_list_name = []
            for group in context.object.vertex_groups:
                if [ v for v in context.object.data.vertices if group.index in [ vg.group for vg in v.groups ] ] == []:
                    # Добавляем имя группы которя не содержит вершин в список.
                    del_list_name.append(group.name)

            # Проходим по спику с именами и удаляем.
            for del_group in del_list_name:
                vg = context.object.vertex_groups.get(del_group)
                context.object.vertex_groups.remove(vg)

        context.window_manager.hatcher.faces_name_buffer = ''

        return {'FINISHED'}

# Заглушка для неактивной кнопки.
class Pass_operator(bpy.types.Operator):
    '''Not implemented at the moment'''
    bl_idname = "mesh.pass_operator"
    bl_label = "Pass_operator"
    def execute(self, context):
        return {'FINISHED'}

# Выделение полигонов, со сбросом не нужных полигонов.
class Select_face(bpy.types.Operator):
    '''Select the polygon group'''
    bl_idname = "mesh.select_face"
    bl_label = "Select_face"
    
    index_list: bpy.props.StringProperty()
    
    
    def vertex_active(self, me):
        
        #BMVert
        
        bm = bmesh.from_edit_mesh(me)

        for elem in reversed(bm.select_history):
            if isinstance(elem, bmesh.types.BMFace):
                return elem
        else:
            return None
    
    
    def execute(self, context):


        me = context.object.data
        bm = bmesh.from_edit_mesh(me)
        bm.faces.ensure_lookup_table()
        
        
        print (self.vertex_active(me))
        
        '''# Проходим по элементам в строчке, преобразовав её в список.
        for element in self.index_list.split():
            bm.faces[int(element)].select_set(False)

        # Выбираем активный слой.
        bpy.ops.object.vertex_group_set_active( group = context.object.vertex_groups.active.name )
        bpy.ops.object.vertex_group_select()
        
        bmesh.update_edit_mesh(me)'''

        return {'FINISHED'}

# Снять выделение полигонов взамен блендера, так как функция имеет дефект.
class Deselect_face(bpy.types.Operator):
    '''Delete the polygon group'''
    bl_idname = "mesh.deselect_face"
    bl_label = "Deselect_face"

    index_list: bpy.props.StringProperty()
    bool_delete: bpy.props.IntProperty()

    def execute(self, context):

        me = context.object.data
        bm = bmesh.from_edit_mesh(me)
        bm.faces.ensure_lookup_table()
        
        # Создаем на "лету" новые свойства для лиц.
        try:
            name_face = bm.faces.layers.string['name']
        except:
            name_face = bm.faces.layers.string.new('name')
            for face in bm.faces:
                face[name_face] = bytes("", 'utf-8')

        # Проходим по элементам в строчке, преобразовав её в список.
        for element in self.index_list.split():
            bm.faces[int(element)].select_set(False)
        
        bmesh.update_edit_mesh(me)
        
        if self.bool_delete == 1:
            bpy.ops.mesh.delete_group()

        return {'FINISHED'}

# Удаление группы вершин и очистить значения.
class Delete_group(bpy.types.Operator):
    '''Delete the polygon group'''
    bl_idname = "mesh.delete_group"
    bl_label = "Delete_group"

    def execute(self, context):
        
        me = context.object.data
        bm = bmesh.from_edit_mesh(me)
        bm.faces.ensure_lookup_table()
        
        bpy.ops.object.vertex_group_deselect()
        bpy.ops.object.vertex_group_set_active( group = context.object.vertex_groups.active.name )
        bpy.ops.object.vertex_group_select()
        
        # Добавляем выбраные лица в список.
        for f in bm.faces:
            if f.select:
                selfaces.append(f.index)
        bmesh.update_edit_mesh(me)
        
        # Создаем на "лету" новые свойства для лиц.
        try:
            name_face = bm.faces.layers.string['name']
        except:
            name_face = bm.faces.layers.string.new('name')
            for face in bm.faces:
                face[name_face] = bytes("", 'utf-8')

        # Проходим по элементам в строчке, преобразовав её в список.
        for element in selfaces:
            # Записываем пустое значение
            bm.faces[int(element)][name_face] = bytes('', 'utf-8')

        bmesh.update_edit_mesh(me)

        context.object.vertex_groups.remove(context.object.vertex_groups.active)
        
        return {'FINISHED'}
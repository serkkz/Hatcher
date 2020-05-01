# -*- coding: utf-8 -*-
import bpy
import bmesh
import io
import os
import shutil
import subprocess

# Коректировка пути для панды
def cor_path(path, type=None):
    raw = '{!r}'.format(path)
    rezr = raw.replace("\\", "/").replace("//", "/").replace("'", '')
    if type:
        rez = rezr.replace("\\", "/")
    else:
        u = rezr[0]
        p = rezr[:].split('/')
        x = p[1:]
        x.insert(0, p[0].lower().replace(":", ""))
        rez = '/' + '/'.join(x)
    return rez

#Получение относительной директории и относительной директории с именем файла
def getRelative(pathstart, dircopytex, texadress):
    # Принимат полный адрес файла, для извлечения имени.
    # Путь экспорта модели.
    # Путь копирования текстуры полный.
    # Возращает кортеж, относительный путь и вычисленый полный путь с именем.

    # Раскладываем адрес изображения на директорию и имя.
    (dirName, fileName) = os.path.split(texadress)
    # Вычесление относительного пути.
    relpath = os.path.relpath(dircopytex, pathstart)
    # К директории добавляем имя файла, и получаем полный относительный адрес.
    fulrelpath = os.path.join(relpath, fileName)
    # Возращаем скоррективыный относительный путь.
    return (relpath, fulrelpath)

# Класс для экспорта egg.
class Export_egg(bpy.types.Operator):
    """ Exporting the model"""
    bl_idname = "mesh.generate_egg"
    bl_label = "Generator"

    def invoke(self, context, event):

        # Создаем данные из сетки.
        bm = bmesh.new()
        bm.from_mesh(context.object.data)
        
        # Получаем директорию проекта.
        path_project = context.scene.hatcher.dir_path_project
        
        # Получаем относительную директорию модели.
        path_catalog_model = bpy.data.objects[context.object.name].hatcher.catalog_model

        # Объединяем путь проекта и относительную директорию модели.
        path_project_and_path_catalog_model = os.path.join(path_project, path_catalog_model)

        # Проверяем существует ли директория
        if os.path.exists(path_project_and_path_catalog_model):
            pass
        else:
            # Если нет, то создаем
            os.makedirs(path_project_and_path_catalog_model)
            
        
        # Объединяем путь директории и имя файла.
        path_save = os.path.join(path_project_and_path_catalog_model, context.object.name)

        # Кэш для пула вертексов, сюда будем помещать чтоб записать в файл в нужном порядке.
        vertex_cache = []
        
        # Кэш для пула полигонов, сюда будем помещать чтоб записать в файл в нужном порядке.
        polygons_cache = []
            
        # Кэш для группы вершин которые состовляют один полигон.
        vert = []

        # Проверка есть ли активные текстурные координаты у объекта.
        if context.object.data.uv_layers.active:
            # Если есть то создаем переменную с данными.
            uv_layer = context.object.data.uv_layers.active.data
        else:
            uv_layer = None

        # Открываем файл для записи.
        egg = open(path_save + '.egg', 'w')
        
        # Запись строки о системе координат.
        egg.write('<CoordinateSystem> { ' + bpy.data.objects[context.object.name].hatcher.coordinatesystem + ' }\n\n')
            
        # Запись о версии hatcher.
        egg.write('<Comment> { "Exporter Hatcher version 0.6" }\n\n')
            
        # Открываем пул вершин.
        vertex_cache.append(' <VertexPool> {} {{\n'.format(context.object.name))

        id_vertex = 0

        # Перебираем полигоны активного объекта.
        for poly in context.object.data.polygons:
        
            # Перебираем вершины полигона.
            for i in poly.vertices[:]:
                # Получаем данные из вершин
                vert_data = context.object.data.vertices[i]
                # Открываем вершину 
                vertex_cache.append('  <Vertex> {} {{ {} \n'.format(id_vertex, '{0:.6f}'.format(vert_data.co[0]).rstrip('0').rstrip('.') +' '+ '{0:.6f}'.format(vert_data.co[1]).rstrip('0').rstrip('.') +' '+  '{0:.6f}'.format(vert_data.co[2]).rstrip('0').rstrip('.')))
                # Проверка используется ли сглаживание 
                if poly.use_smooth:
                    vertex_cache.append('   <Normal> {{ {} {} {} }}\n'.format('{0:.6f}'.format(vert_data.normal[0]).rstrip('0').rstrip('.'), '{0:.6f}'.format(vert_data.normal[1]).rstrip('0').rstrip('.'), '{0:.6f}'.format(vert_data.normal[2]).rstrip('0').rstrip('.')))
                # Проверка статуса переменой с текстурными координатами. 
                if uv_layer:
                    # Активный слой записываем без имени UV
                    vertex_cache.append('   <UV> {{ {} {} }}\n'.format('{0:.6f}'.format(uv_layer[id_vertex].uv[0]).rstrip('0').rstrip('.'), '{0:.6f}'.format(uv_layer[id_vertex].uv[1]).rstrip('0').rstrip('.')))
                    # Проходим по не активным слоям
                    for uv in context.object.data.uv_layers:
                        # Если имя не равно активному слою, то записываем.
                        if uv.name != context.object.data.uv_layers.active.name:
                            vertex_cache.append('   <UV> {} {{ {} {} }}\n'.format(uv.name,'{0:.6f}'.format(uv.data[id_vertex].uv[0]).rstrip('0').rstrip('.'), '{0:.6f}'.format(uv.data[id_vertex].uv[1]).rstrip('0').rstrip('.')))
                # Закрываем  вершину
                vertex_cache.append('  }\n')
                
                id_vertex += 1
                
            # Всего вершин из которых состоит полигон
            total_vert = poly.loop_total
            # Перебираем вершины для извлечения информации
            for i in range(total_vert):
                # Запись в кеш с корректировкой номера
                vert.append(str(poly.loop_start + i))
                
            bm.faces.ensure_lookup_table()
            
            try:
                name_face = bm.faces.layers.string['name']
            except:
                name_face = bm.faces.layers.string.new('name')
                for face in bm.faces:
                    face[name_face] = bytes("", 'utf-8')

            if bm.faces[poly.index][name_face].decode("utf-8") != '':
                # Открываем группу полигонов
                polygons_cache.append(' <Polygon> {id} {{ \n'.format(id = bm.faces[poly.index][name_face].decode("utf-8")))
            else:
                # Открываем группу полигонов
                polygons_cache.append(' <Polygon> {id} {{ \n'.format(id = poly.index))

            # Добавляем запись к полигону с именем слота материала.
            #polygons_cache.append('  <MRef> {{ {} }}\n'.format(name_mat.name))
            
            # Запись строки о направлении нормали
            polygons_cache.append('  <Normal> {{ {} {} {} }}\n'.format('{0:.6f}'.format(poly.normal[0]).rstrip('0').rstrip('.'), '{0:.6f}'.format(poly.normal[1]).rstrip('0').rstrip('.'), '{0:.6f}'.format(poly.normal[2]).rstrip('0').rstrip('.')))
            # Запись строки с номерами вершин из которых состоит полигон
            polygons_cache.append('  <VertexRef> {{ {} <Ref> {{ {} }} }}\n'.format(','.join(vert).replace(",", " "), context.object.name))
            # Закрываем группу полигонов
            polygons_cache.append('  }\n')
            # Очистка кеша для следующей группы вершин 
            vert[:] = []

        # Закрываем  пул вершин
        vertex_cache.append(' }\n\n')

        # Открываем группу объекта 
        egg.write('<Group>  {} {{\n'.format(context.object.name))
        
        egg.write(' <Scalar> collide-mask {{ {} }}\n'.format(context.active_object.hatcher.collide_mask))
        egg.write(' <Scalar> from-collide-mask {{ {} }}\n'.format(context.active_object.hatcher.from_collide_mask))
        egg.write(' <Scalar> into-collide-mask {{ {} }}\n'.format(context.active_object.hatcher.into_collide_mask))

        list_flags = []

        context.object.hatcher.collide_type
        
        if context.object.hatcher.collide_type != "None":
        
            if context.object.hatcher.collide_flag_1 != "None":
            
                list_flags.append(context.object.hatcher.collide_flag_1)
                
            if context.object.hatcher.collide_flag_2 != "None":
            
                list_flags.append(context.object.hatcher.collide_flag_2)
                
            if context.object.hatcher.collide_flag_3 != "None":
            
                list_flags.append(context.object.hatcher.collide_flag_3)
                
            if context.object.hatcher.collide_flag_4 != "None":
            
                list_flags.append(context.object.hatcher.collide_flag_4)
                
            if context.object.hatcher.collide_flag_5 != "None":
            
                list_flags.append(context.object.hatcher.collide_flag_5)
            
            # Проверка есть ли записанные флаги в списке.
            if list_flags:
                
                # Записываем с флагами.
                egg.write(' <Collide> {} {{ {} {} }}\n'.format(context.active_object.hatcher.collide_name, context.object.hatcher.collide_type, ','.join(list_flags).replace(",", " ")))

            else:
            
                # Записываем без флагов.
                egg.write(' <Collide> {} {{ {} }}\n'.format(context.active_object.hatcher.collide_name, context.object.hatcher.collide_type))

                
        # Записываем все вершины в виртуальный файл
        for data_vert in vertex_cache:
        
            egg.write(data_vert)
             
        # Записываем все материалы в виртуальный файл
        for data_poly in polygons_cache:
        
            egg.write(data_poly)
            
        # Проверяем есть ли списке egg файлы
        if context.object.hatcher_list_egg_groop.items() != []: 
        
            # Проходим по списку с egg файлами
            for data_egg_file in context.object.hatcher_list_egg_groop:
                
                # Проверяем указан ли адрес файла
                if data_egg_file.path_egg:

                    egg.write('<File> {{ "{}" }}\n'.format(cor_path(data_egg_file.path_egg)))

        # Закрываем группу объекта
        egg.write('}')
                 
        # Закрываем файл.
        egg.close()

        if context.active_object.hatcher.chexbox_convert_bam:
            # Адрес утилиты конвектора в bam
            ful_adress_util_egg_bam = os.path.join(context.scene.hatcher.dir_Panda3D_Bin, "egg2bam.exe")
            egg_bam = subprocess.Popen(ful_adress_util_egg_bam+' -o '+str(path_save + '.bam')+' '+str(path_save + '.egg'), shell=True, stdout=subprocess.PIPE)
            out_egg_bam = egg_bam.stdout.readlines()
            
            if out_egg_bam:
                print (out_egg_bam)
            
            if context.active_object.hatcher.chexbox_view_model:
                # Адрес утилиты просмотра
                ful_adress_util_view = os.path.join(context.scene.hatcher.dir_Panda3D_Bin, "pview.exe") 
                view = subprocess.Popen(ful_adress_util_view+' '+str(path_save + '.bam'), shell=True, stdout=subprocess.PIPE)
                out_view = view.stdout.readlines()
                if out_view:
                    print (out_view)
        else:
            if context.active_object.hatcher.chexbox_view_model:
        
                # Адрес утилиты просмотра
                ful_adress_util_view = os.path.join(context.scene.hatcher.dir_Panda3D_Bin, "pview.exe") 
                view = subprocess.Popen(ful_adress_util_view+' '+str(path_save + '.egg'), shell=True, stdout=subprocess.PIPE)
                out_view = view.stdout.readlines()
                if out_view:
                    print (out_view)

        return {'FINISHED'}

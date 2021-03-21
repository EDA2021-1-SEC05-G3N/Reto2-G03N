"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import time
import tracemalloc
import config as cf
import model
import csv
from datetime import datetime

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros

def initCatalog():
    """
    Llama la función de inicialización del catalogo del modelo.
    """
    catalog = model.newCatalog()
    return catalog





# Funciones para la carga de datos

def loadData(catalog):
    """
    Carga los datos de los archivos y carga los datos en la
    estructura de datos
    """

    delta_time = -1.0
    delta_memory = -1.0

    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()


    loadVideos(catalog)
    loadCategories(catalog)
    #loadCountries(catalog)


    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)

    return delta_time, delta_memory

def loadVideos(catalog):
    """
    Carga los libros del archivo.  Por cada video se toman los datos necesarios:
    video id, trending date, category id, views, nombre del canal, país, nombre del 
    video, likes, dislikes, fecha de publicación, likes y tags.
    """

    videosfile = cf.data_dir + 'videos-large.csv'
    
    input_file = csv.DictReader(open(videosfile, encoding='utf-8'))
    for video in input_file:
        cada_video = {'video_id': video['video_id'],
                  'trending_date': datetime.strptime(video['trending_date'], '%y.%d.%m').date(),
                  'category_id': int(video['category_id']),
                  'views': int(video['views']),
                  'channel_title': video['channel_title'],
                  'country': video['country'],
                  'title': video['title'],
                  'likes': video['likes'],
                  'dislikes': video['dislikes'],
                  'publish_time': video['publish_time'],
                  'tags': video['tags']}
                  
        model.addVideo(catalog, cada_video)

def loadCategories (catalog):
    """
    Carga las categorías del archivo. Por cada categoría su guarda su id y su nombre.
    """

    categoriesfile = cf.data_dir + 'category-id.csv'

    input_file = csv.DictReader(open(categoriesfile, encoding='utf-8'), delimiter="\t")
    for category in input_file:
        category_name =  category['name'].strip()
        category_id = int(category['id'])

        model.addCategory(catalog, category_name, category_id)

def loadCountries(catalog):

    videosfile = cf.data_dir + 'videos-large.csv'
    
    input_file = csv.DictReader(open(videosfile, encoding='utf-8'))
    



# Funciones de ordenamiento

#1
def sortVideosByViews(lista_filtros, cantidad):
    """
    Ordena los videos por views.
    """
    return model.sortVideosByViews(lista_filtros, cantidad)

#2
def sortVideosByID(filtro_pais):
    """
    Ordena los videos por id.
    """
    return model.sortVideosByID(filtro_pais)

#3
def sortVideosByID_date(filtro_categoria):
    """
    Ordena los videos por dos criterios: en primer lugar por su id y segundo por su trending_date. 
    """
    return model.sortVideosByID_date(filtro_categoria)

#4
def sortVideosByLikes (lista_filtros):
    """
    Ordena los videos por likes.
    """
    return model.sortVideosByLikes(lista_filtros)





# Funciones de consulta sobre el catálogo

#1
def get_id_categoria (categoria, catalog):
    """
    Retorna el id de la categoría solicitada.
    """
    return model.get_id_categoria(categoria, catalog)

#1
def filtrar_pais_categoria (id_categoria, pais, catalog):
    """
    Retorna una lista que cumple con los requerimientos de país y categoría.
    """
    return model.filtrar_pais_categoria(id_categoria, pais, catalog)

#2
def filtrar_pais (pais, catalog):
    """
    Retorna una lista que cumple con el requerimiento de país.
    """
    return model.filtrar_pais(pais, catalog)

#2
def getTendencia2 (sorted_list):
    """
    Retorna el video con más días en tendencia.
    """
    return model.getTendencia2(sorted_list)

#3
def filtrar_categoria (id_categoria, catalog):
    """
    Retorna una lista que cumple con el requerimiento de categoría.
    """
    return model.filtrar_categoria(id_categoria, catalog)

#3
def getTendencia3 (sorted_list):
    """
    Retorna el video con más días en tendencia. En este caso, tiene en cuenta que 
    no se cuente doble como tendencia el mismo día en países distintos. 
    """
    return model.getTendencia3(sorted_list)

#4
def filtrar_pais_tag (tag, pais, catalog):
    """
    Retorna una lista que cumple con los requerimientos de país y tag. 
    """
    return model.filtrar_pais_tag(tag, pais, catalog)
    
#4
def acortar_lista (sorted_list, cantidad):
    """
    Retorna una lista que cumple con el requerimiento de la cantidad de videos. 
    """
    return model.acortar_lista(sorted_list, cantidad)





#Funciones con el orden de las ejecuciones de cada requerimiento:

#1
def requerimiento_1(categoria, pais, cantidad, catalog):

    id_categoria = get_id_categoria(categoria, catalog)
    lista_filtros = filtrar_pais_categoria(id_categoria, pais, catalog)
    sorted_list = sortVideosByViews(lista_filtros, cantidad)

    return sorted_list

#2
def requerimiento_2 (pais, catalog):
    
    filtro_pais = filtrar_pais(pais, catalog)
    sorted_list = sortVideosByID(filtro_pais)
    tendencia = getTendencia2(sorted_list)

    return tendencia

#3
def requerimiento_3 (categoria, catalog):

    id_categoria = get_id_categoria(categoria, catalog)
    filtro_categoria = filtrar_categoria(id_categoria, catalog)
    sorted_list = sortVideosByID_date(filtro_categoria)
    tendencia_categoria = getTendencia3(sorted_list)

    return tendencia_categoria

#4
def requerimiento_4 (tag, pais, cantidad, catalog):

    lista_filtros = filtrar_pais_tag (tag, pais, catalog)
    sorted_list = sortVideosByLikes (lista_filtros)
    lista_acortada = acortar_lista (sorted_list, cantidad)

    return lista_acortada

#5
def requerimiento_5 (categoria, cantidad, catalog):

    category_id = model.requerimiento_5(categoria, catalog)
    lista_filtro = model.filtrar_categoria(category_id, catalog)
    lista_ordenada = model.sortVideosByLikes(lista_filtro)
    lista_acortada = model.acortar_lista(lista_ordenada, cantidad)

    return lista_acortada

# ======================================
# Funciones para medir tiempo y memoria
# ======================================


def getTime():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def getMemory():
    """
    toma una muestra de la memoria alocada en instante de tiempo
    """
    return tracemalloc.take_snapshot()


def deltaMemory(start_memory, stop_memory):
    """
    calcula la diferencia en memoria alocada del programa entre dos
    instantes de tiempo y devuelve el resultado en bytes (ej.: 2100.0 B)
    """
    memory_diff = stop_memory.compare_to(start_memory, "filename")
    delta_memory = 0.0

    # suma de las diferencias en uso de memoria
    for stat in memory_diff:
        delta_memory = delta_memory + stat.size_diff
    # de Byte -> kByte
    delta_memory = delta_memory/1024.0
    return delta_memory
﻿"""
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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
assert cf
import time
from DISClib.Algorithms.Sorting import mergesort


"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, 
otra para las categorias de los mismos.
"""

# Construccion de modelos

def newCatalog():
    """
    Inicializa el catálogo de videos. Crea una lista vacia para guardar
    todos los videos, adicionalmente, crea una lista vacia para los videos,
    una lista vacia para los views y una lista vacia para las categorias de 
    los videos. Retorna el catalogo inicializado.
    """
    catalog = {'videos': None,
               'category': None,
               'countries': None,
               'categories': None
                }

    catalog['videos'] = lt.newList('SINGLE_LINKED', cmpfunction = comparevideo_id1)
    
    catalog['category'] = mp.newMap(32, 
    maptype= 'PROBING',
    loadfactor= 0.75,    
    comparefunction= None
    )
    
    catalog['countries'] = mp.newMap(10,
    maptype= 'PROBING',
    loadfactor= 0.75,
    comparefunction= None
    )

    catalog['categories'] = mp.newMap(32,
    maptype= 'PROBING',
    loadfactor= 0.75,
    comparefunction= None
    )
    
    return catalog




# Funciones para agregar informacion al catalogo 

def addVideo(catalog, video):
    """
    Añade un video al final, de la lista recibida
    """
    lt.addLast(catalog['videos'], video)
    addVideoCountry(catalog, video)
    addVideoCategory(catalog, video)

def addVideoCountry(catalog, video):
    """
    Esta funcion adiciona un libro a la lista de libros que
    fueron publicados en un año especifico.
    Los años se guardan en un Map, donde la llave es el año
    y el valor la lista de libros de ese año.
    """

    countries_map = catalog['countries']
 
    pubcountry = video['country']

    existcountry = mp.contains(countries_map, pubcountry)

    if existcountry:
        entry = mp.get(countries_map, pubcountry)
        country_values = me.getValue(entry)
    else:
        country_values = newYear(pubcountry)
        mp.put(countries_map, pubcountry, country_values)
    lt.addLast(country_values['videos'], video)
        
 


def newYear(pubcountry):
    """
    Esta funcion crea la estructura de libros asociados
    a un año.
    """
    entry = {'country': "", "videos": None}
    entry['country'] = pubcountry
    entry['videos'] = lt.newList('SINGLE_LINKED')
    return entry



def addVideoCategory(catalog, video):
    """
    Esta funcion adiciona un libro a la lista de libros que
    fueron publicados en un año especifico.
    Los años se guardan en un Map, donde la llave es el año
    y el valor la lista de libros de ese año.
    """

    categories_map = catalog['categories']
 
    pubcategory = video['category_id']

    existcategory = mp.contains(categories_map, pubcategory)

    if existcategory:
        entry = mp.get(categories_map, pubcategory)
        category_values = me.getValue(entry)
    else:
        category_values = newYear(pubcategory)
        mp.put(categories_map, pubcategory, category_values)
    lt.addLast(category_values['videos'], video)
        
 


def newYear(pubcategory):
    """
    Esta funcion crea la estructura de libros asociados
    a un año.
    """
    entry = {'category': "", "videos": None}
    entry['category'] = pubcategory
    entry['videos'] = lt.newList('SINGLE_LINKED')
    return entry


def addCategory(catalog, category_id, category_name):
    """
    Añade una categoria al final, de la lista recibida
    """
    if category_id == None:
        pass
    else:
        mp.put(catalog['category'], category_id, category_name)



# Funciones de consulta

#1
def filtrar_pais_categoria (categoria, pais, catalog):
    """
    Crea una lista nueva para ordenar los datos segun su id.
    Y recorre la lista dada, para guardar en la nueva lista 
    solo los videos que correspondan con el id y el pais
    """
    nueva_lista = lt.newList("ARRAY_LIST", cmpfunction = comparevideo_id1)

    lista_paises = (me.getValue(mp.get(catalog['countries'], pais)))["videos"]

    for x in lt.iterator(lista_paises):
        if me.getValue(mp.get(catalog['category'], int(x['category_id']))) == categoria:
            lt.addLast(nueva_lista, x)

    return nueva_lista

#2
def filtrar_pais (pais, catalog):
    """
    Crea una lista nueva para ordenar los datos segun su id.
    Y recorre la lista dada, para guardar en la nueva lista 
    solo los videos que correspondan con el respectivo pais
    """
    lista_paises = (me.getValue(mp.get(catalog['countries'], pais)))["videos"]

    return lista_paises

#2
def getTendencia2(sorted_list):

    mayor = lt.firstElement(sorted_list)
    conteo = 0

    sig = None
    conteo_sig = 0

    for x in lt.iterator(sorted_list):
        if x['video_id'] == mayor["video_id"]:
            conteo += 1
 
        elif sig == None: 
            sig = x
            conteo_sig += 1

        elif x['video_id'] == sig["video_id"]:
                conteo_sig += 1
                
        else:
            if conteo_sig > conteo:
                mayor = sig
                conteo = conteo_sig
            sig = x
            conteo_sig = 1

    return mayor, conteo

#3
def filtrar_categoria (categoria, catalog):
    """
    Crea una lista nueva para ordenar los datos segun su id y su trending date.
    Y recorre la lista dada, para guardar en la nueva lista 
    solo los videos que correspondan con el respectivo id
    Ignorando los que su id sea "#NANE?"
    """
    nueva_lista = lt.newList("ARRAY_LIST", cmpfunction = cmpVideosByID_date)

    for x in lt.iterator(catalog['videos']):
        if x['video_id'] == '#NAME?':
            pass        
        else:
            categoria_x = me.getValue(mp.get(catalog['category'], int(x['category_id'])))
            if categoria_x == categoria:
                lt.addLast(nueva_lista, x)

    return nueva_lista   

#3
def getTendencia3 (sorted_list):

    mayor = lt.firstElement(sorted_list)
    conteo = 1

    sig = None
    conteo_sig = 1

    for x in lt.iterator(sorted_list):
        if x['video_id'] == mayor["video_id"]:
            if x['trending_date'] != mayor["trending_date"]:
                conteo += 1
 
        elif sig == None: 
            sig = x
            conteo_sig += 1

        elif x['video_id'] == sig["video_id"]:
            if x['trending_date'] != sig["trending_date"]:
                conteo_sig += 1
                
        else:
            if conteo_sig > conteo:
                mayor = sig
                conteo = conteo_sig
            sig = x
            conteo_sig = 1

    return mayor, conteo

#4
def filtrar_pais_tag (tag, pais, catalog):
    """
    Crea una lista nueva para ordenar los datos segun sus likes.
    Y recorre la lista dada, para guardar en la nueva lista 
    solo los videos que correspondan con el pais dado,
    y que tengan en sus id's el id dado.
    Antes de leer los tag, se dividen por "|" para poderlos leer bien
    """
    nueva_lista = lt.newList("ARRAY_LIST", cmpfunction = cmpVideosByLikes)

    lista_paises = (me.getValue(mp.get(catalog['countries'], pais)))["videos"]

    for x in lt.iterator(lista_paises):
        lista_tags = (x['tags'].split("|"))
        for y in lista_tags:
            if tag in str(y):
                lt.addLast(nueva_lista, x)

    return nueva_lista

#4
def acortar_lista (sorted_list, cantidad):
    """
    Crea una lista nueva para ordenar los datos segun sus likes.
    Y va guardando unicamente los datos que tienen diferente title
    """
    lista_final = lt.newList("ARRAY_LIST", cmpfunction = cmpVideosByLikes)

    for x in lt.iterator(sorted_list):
        if lt.isEmpty(lista_final):
            lt.addLast(lista_final, x)
        else:
            cond = True
            for y in lt.iterator(lista_final):
                if y['title'] == x['title']:
                    cond = False
            if cond == True:
                lt.addLast(lista_final, x)
                if lt.size(lista_final) == cantidad: 
                    break
        if lt.size(lista_final) == cantidad:
            break

    return lista_final






# Funciones utilizadas para comparar elementos dentro de una lista

def comparevideo_id1(video1, video2):
    """
    Devuelve verdadero (True) si los 'id' de video1 son menores que los del video2
    Args:
    video1: informacion del primer video que incluye su valor 'video_id'
    video2: informacion del segundo video que incluye su valor 'video_id'
    """
    return video1["video_id"] < video2["video_id"]

def cmpVideosByID_date (video1, video2):
    """
    Devuelve verdadero (True) si los 'id' de video1 son menores que los del video2
    Args:
    video1: informacion del primer video que incluye su valor 'video_id'
    video2: informacion del segundo video que incluye su valor 'video_id'
    Y si los id son iguales los compara por su trending date
    """
    if video1['video_id'] != video2['video_id']:
        return video1["video_id"] < video2["video_id"]   
    else:
        return video1["trending_date"] < video2["trending_date"]

def cmpVideosByViews(video1, video2):
    """
    Devuelve verdadero (True) si los 'views' de video1 son mayores que los del video2
    Args:
    video1: informacion del primer video que incluye su valor 'views'
    video2: informacion del segundo video que incluye su valor 'views'
    """
    return (float(video1['views']) > float(video2['views']))

def cmpVideosByLikes(video1, video2):
    """
    Devuelve verdadero (True) si los 'likes' de video1 son mayores que los del video2
    Args:
    video1: informacion del primer video que incluye su valor 'likes'
    video2: informacion del segundo video que incluye su valor 'likes'
    """
    return (float(video1['likes']) > float(video2['likes']))





# Funciones de ordenamiento

#1
def sortVideosByViews (lista_filtros, cantidad):
    """
    Ordena la lista recibida organizando los datos segun sus Views
    Y crea una lista nueva para guardar los datos allí, para retornar su copia
    """
    sorted_list = mergesort.sort(lista_filtros, cmpVideosByViews)

    sub_list = lt.subList(sorted_list, 1, cantidad)
    sub_list = sub_list.copy()

    return sub_list

#2
def sortVideosByID (filtro_pais):
    """
    Ordena la lista recibida organizando los datos segun sus id
    """
    sorted_list = mergesort.sort(filtro_pais, comparevideo_id1)

    return sorted_list 

#3
def sortVideosByID_date (filtro_categoria):
    """
    Ordena la lista recibida organizando los datos segun sus id o sus trending date
    """
    sorted_list = mergesort.sort(filtro_categoria, cmpVideosByID_date)

    return sorted_list

#4
def sortVideosByLikes (lista_filtros):
    """
    Ordena la lista recibida organizando los datos segun sus Likes
    """
    sorted_list = mergesort.sort(lista_filtros, cmpVideosByLikes)
    
    return sorted_list

#5
def requerimiento_5 (categoria, catalog):

    pareja = mp.get(catalog['category'], categoria)
    category_id = me.getValue(pareja)

    return category_id

def VideosPorPais (catalog, pais):
    
    x = mp.get(catalog['countries'], pais) 
    valor = me.getValue(x)

    return valor




# Construccion de modelos

# Funciones para agregar informacion al catalogo

# Funciones para creacion de datos

# Funciones de consulta

# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento
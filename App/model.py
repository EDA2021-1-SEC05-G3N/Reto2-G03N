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

    catalog['videos'] = lt.newList('ARRAY_LIST', cmpfunction = comparevideo_id1)
    
    catalog['category'] = mp.newMap(32, 
    maptype= 'PROBING',
    loadfactor= 0.75,    
    comparefunction= None
    )
    
    catalog['countries'] = mp.newMap(20,
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
    Añade un video al final, de la lista recibida. 
    """
    lt.addLast(catalog['videos'], video)
    addVideoCountry(catalog, video)
    addVideoCategory(catalog, video)

def addVideoCountry(catalog, video):
    """
    Esta funcion adiciona un video a la lista de videos.
    Los países se guardan en un Map, donde la llave es el país
    y el valor la lista de videos de ese país.
    """

    countries_map = catalog['countries']
 
    pubcountry = video['country']

    existcountry = mp.contains(countries_map, pubcountry)

    if existcountry:
        entry = mp.get(countries_map, pubcountry)
        country_values = me.getValue(entry)
    else:
        country_values = newCountry(pubcountry)
        mp.put(countries_map, pubcountry, country_values)
    lt.addLast(country_values['videos'], video) 
 

def newCountry(pubcountry):
    """
    Esta funcion crea la estructura de videos asociados
    a un año.
    """
    entry = {'country': "", "videos": None}
    entry['country'] = pubcountry
    entry['videos'] = lt.newList('ARRAY_LIST')
    return entry


def addVideoCategory(catalog, video):
    """
    Esta funcion adiciona un libro a la lista de libros que
    fueron publicados en un año especifico.
    Los años se guardan en un Map, donde la llave es el año
    y el valor la lista de libros de ese año.
    """

    categories_map = catalog['categories']
 
    pubcategory = int(video['category_id'])

    existcategory = mp.contains(categories_map, pubcategory)

    if existcategory:
        entry = mp.get(categories_map, pubcategory)
        category_values = me.getValue(entry)
    else:
        category_values = newCategory(pubcategory)
        mp.put(categories_map, pubcategory, category_values)
    lt.addLast(category_values['videos'], video)
        
 
def newCategory(pubcategory):
    """
    Esta funcion crea la estructura de libros asociados
    a un año.
    """
    entry = {'category': "", "videos": None}
    entry['category'] = pubcategory
    entry['videos'] = lt.newList('ARRAY_LIST')
    return entry


def addCategory(catalog, category_id, category_name):
    """
    Añade una categoría al mapa con el nombre de las 
    categorías como llave y el cotegory_id como valor. 
    """
    if category_id == None:
        pass
    else:
        mp.put(catalog['category'], category_name, category_id)



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
    numero_id = me.getValue(mp.get(catalog['category'], categoria))

    for x in lt.iterator(lista_paises):
        if int(x['category_id']) == numero_id:
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

    actual = lt.firstElement(sorted_list)
    conteo = 0

    mayor = actual
    conteo_mayor = 0

    for x in lt.iterator(sorted_list):
        if x['video_id'] == actual["video_id"]:
            conteo += 1
        
        else:
            if conteo > conteo_mayor:
                mayor = actual
                conteo_mayor = conteo
            actual = x
            conteo = 1

    return mayor, conteo_mayor

#3
def filtrar_categoria (categoria, catalog):
    """
    Crea una lista nueva para ordenar los datos segun su id y su trending date.
    Y recorre la lista dada, para guardar en la nueva lista 
    solo los videos que correspondan con el respectivo id
    Ignorando los que su id sea "#NANE?"
    """
    nueva_lista = lt.newList("ARRAY_LIST", cmpfunction = cmpVideosByID_date)

    numero_id = me.getValue(mp.get(catalog['category'], categoria))
    lista_categorias = (me.getValue(mp.get(catalog['categories'], numero_id)))["videos"]

    for x in lt.iterator(lista_categorias):
        if x['video_id'] != '#NAME?':
            lt.addLast(nueva_lista, x)

    return nueva_lista   

#3
def masrepetido1(lista_videos):
    i=0
    contador=0
    numerodeapariciones=0
    video=""
    while i < lt.size(lista_videos):
        video1 =lt.getElement(lista_videos,i)
        video2 =lt.getElement(lista_videos,i+1)
        if video1["video_id"] == video2["video_id"] :
           contador+= 1
        else:
            if contador > numerodeapariciones:
               numerodeapariciones = contador
               video=(lt.getElement(lista_videos,i))
            contador =0
        i+=1
    return (video, numerodeapariciones+1)

#4
def filtrar_pais_tag (tag, pais, catalog):
    """
    Crea una lista nueva para ordenar los datos segun sus likes.
    Obtiene la lista con los países que se encuentra en el map countries. 
    Recorre esta lista para obtener los videos con el tag que se busca.
    Antes de leer los tag, se dividen por "|" para poderlos leer bien.
    """
    nueva_lista = lt.newList("ARRAY_LIST", cmpfunction = cmpVideosByLikes)

    lista_paises = (me.getValue(mp.get(catalog['countries'], pais)))["videos"]

    for x in lt.iterator(lista_paises):
        lista_tags = (x['tags'].split("|"))
        for y in lista_tags:
            if tag in str(y):
                lt.addLast(nueva_lista, x)

    return nueva_lista

def acortar_lista (sorted_list, cantidad):
    """
    Crea una lista nueva para ordenar los datos según sus likes.
    Y va guardando únicamente los datos que tienen diferente title
    """
    lista_final = lt.newList("ARRAY_LIST", cmpfunction = cmpVideosByLikes)

    lt.addLast(lista_final, (lt.firstElement(sorted_list)))
    titulo = lt.firstElement(sorted_list)['title']
    lista_titulos = [titulo]
    conteo = 1

    for x in lt.iterator(sorted_list):

        if conteo == cantidad:
            break

        if x['title'] not in lista_titulos:
            lt.addLast(lista_final, x)
            lista_titulos.append(x['title'])
            conteo += 1

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
    Si los 'id' son iguales, devuelve verdadero si el trending date del video1 es
    menor que el del video2 
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
    Ordena la lista recibida organizando los datos según sus Views
    Y crea una lista nueva para guardar los datos allí, para retornar su copia
    """
    sorted_list = mergesort.sort(lista_filtros, cmpVideosByViews)

    sub_list = lt.subList(sorted_list, 1, cantidad)
    sub_list = sub_list.copy()

    return sub_list

#2
def sortVideosByID (filtro_pais):
    """
    Ordena la lista recibida organizando los datos según sus id
    """
    sorted_list = mergesort.sort(filtro_pais, comparevideo_id1)

    return sorted_list 

#3
def sortVideosByID_date (filtro_categoria):
    """
    Ordena la lista recibida organizando los datos según sus id, como
    segundo parámetro de ordenamiento usa los trending date.
    """
    sorted_list = mergesort.sort(filtro_categoria, cmpVideosByID_date)

    return sorted_list

#4
def sortVideosByLikes (lista_filtros):
    """
    Ordena la lista recibida organizando los datos según sus Likes.
    """
    sorted_list = mergesort.sort(lista_filtros, cmpVideosByLikes)
    
    return sorted_list
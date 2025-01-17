﻿"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
assert cf
import time
import sys


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("\nBienvenido")
    print("0- Cargar datos del .csv")
    print("1- Req 1 - Videos con más views (categoría, país y cantidad)")
    print("2- Req 2 - Video tendencia (país)")
    print("3- Req 3 - Video tendencia (categoría)")
    print("4- Req 4 - Videos con más likes (tag, país y cantidad)")


def initCatalog():
    """
    Inicializa el catalogo de libros
    """
    return controller.initCatalog()

def loadData(catalog):
    """
    Carga los libros en la estructura de datos
    """
    return controller.loadData(catalog)



# Funciones para imprimir los datos en la consola

def printVideosMasViews(datos):
    lista = datos["elements"]
    for v in lista:
        print("\nFecha de tendencia: ",v['trending_date'])
        print("Nombre del video: ", v['title'])
        print("Nombre del canal: ", v['channel_title'])
        print("Fecha de publicación: ", v['publish_time'])
        print("Reproducciones: ", v['views'])
        print("Likes: ", v['likes'])
        print("Dislikes: ", v['dislikes'])

def printTendenciaPais(datos):
    print("\nNombre del video: ", datos[0]['title'])
    print("Nombre del canal: ", datos[0]['channel_title'])
    print("País: ", datos[0]['country'])
    print("Número de días como tendencia: ", datos[1])

def printTendenciaCategoria(datos):
    print("\nNombre del video: ", datos[0]['title'])
    print("Nombre del canal: ", datos[0]['channel_title'])
    print("Categoría: ", datos[0]['category_id'])
    print("Número de días como tendencia: ", datos[1])

def printVideosMasLikes(datos):
    lista = datos[0]["elements"]
    for v in lista:
        print("\nNombre del video: ", v['title'])
        print("Nombre del canal: ", v['channel_title'])
        print("Fecha de publicación : ", v['publish_time'])
        print("Reproducciones: ", v['views'])
        print("Likes: ", v['likes'])
        print("Dislikes: ", v['dislikes'])
        print("Tags: ", v['tags'])


catalog = None



"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')

    if int(inputs[0]) == 0:

        print("Cargando información de los archivos ....")
        catalog = initCatalog()
        answer = loadData(catalog)

        print('Videos cargados: ' + str(lt.size(catalog['videos'])))
        print('Categorías cargadas: ' + str(mp.size(catalog['category'])))
        print("Tiempo [ms]: ", f"{answer[0]:.3f}", "  ||  ",
              "Memoria [kB]: ", f"{answer[1]:.3f}")


    elif int(inputs[0]) == 1:

        categoria = input('Ingrese la categoría: ')
        pais = input('Ingrese el país: ')
        cantidad = int(input('Ingrese el número de videos: '))

        respuesta = controller.requerimiento_1(categoria, pais, cantidad, catalog)
        printVideosMasViews(respuesta[0])

        print("Tiempo [ms]: ", f"{respuesta[1]:.3f}", "  ||  ",
              "Memoria [kB]: ", f"{respuesta[2]:.3f}")


    elif int(inputs[0]) == 2:

        pais = input("Ingrese el país: ")
        
        respuesta = controller.requerimiento_2(pais, catalog)
        printTendenciaPais(respuesta[0])

        print("Tiempo [ms]: ", f"{respuesta[1]:.3f}", "  ||  ",
              "Memoria [kB]: ", f"{respuesta[2]:.3f}")
    

    elif int(inputs[0]) == 3:

        categoria = input('Ingrese la categoría: ')

        respuesta = controller.requerimiento_3(categoria, catalog)
        printTendenciaCategoria(respuesta[0])
    
        print("Tiempo [ms]: ", f"{respuesta[1]:.3f}", "  ||  ",
              "Memoria [kB]: ", f"{respuesta[2]:.3f}")


    elif int(inputs[0]) == 4:

        tag = input('Ingrese el tag: ')
        pais = input('Ingrese el país: ')
        cantidad = int(input('Ingrese el número de videos: '))

        respuesta = controller.requerimiento_4(tag, pais, cantidad, catalog)
        printVideosMasLikes(respuesta)

        print("Tiempo [ms]: ", f"{respuesta[1]:.3f}", "  ||  ",
              "Memoria [kB]: ", f"{respuesta[2]:.3f}")

    else:
        sys.exit(0)
sys.exit(0)
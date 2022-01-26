# -*- coding: utf-8 -*-
"""
Created on Tue Jan 25 16:01:33 2022

@author: luis Art
"""

import pandas as pd
import pandasql as ps
import time 
import numpy as np
from selenium import webdriver
import matplotlib.pyplot as plt

"""
Se crea un DataFrame donde quedaran guardados los datos obtenidos de las 
distintas paginas web ademas de tambien convertirlo a excel
"""
aux1=pd.DataFrame() # Se crea un DataFrame guardado en la variable aux1
aux1.to_excel("df_productos.xlsx",index=False) # Se convierte el DataFrame a un archivo de tipo excel 

"""
Se crea la funcion buscador de precios la cual llevara todo el codigo 
para extraer la informacion de las paginas web, en este caso sera la de Palacio
de Hierro donde lo abreviaremos como PH
"""
def Buscador_Precios_Selenium_Palacio(producto):
    path="C:\webdriver\chromedriver.exe" # Se define la variable que lleva la ubicacion en nuestra computadora de nuestro webdriver
    driver=webdriver.Chrome(path) # Se conecta el webdriver a Chrome
    url="https://www.elpalaciodehierro.com/buscar?q="+producto # Aqui va el url de la pagina web de la tienda junto con la variable que ingresara el usuario del producto que quiera buscar
    driver.get(url) # Se consulta el URL previamente escrito a través del driver y su metodo get
    
    productos=driver.find_elements_by_class_name("b-product") # Se busca el nombre de la clase donde se encuentra la informacion de cada producto
    
    lista_urls=list() # Se crea una lista vacia donde se añadiran los url de cada producto 
    for i in range(len(productos)): # Con el ciclo se ingresa a cada elemento de la lista productos
        try:
            lista_urls.append(productos[i].find_element_by_tag_name("a").get_attribute("href")) # Se buscan los url por el nombre de la etiqueta y se agrega a lista_urls
        except:
            lista_urls.append(np.nan) # En caso de no tener url se agrega nan en su lugar

    lista_nombres=list() # Se crea una lista vacia donde se añadiran los nombres de cada producto 
    for i in range(len(productos)):  # Con el ciclo se ingresa a cada elemento de la lista productos
        try:
            lista_nombres.append(productos[i].find_elements_by_tag_name("a")[1].text) # Se buscan los nombres de los productos por el nombre de la etiqueta y se añade el elemento que se encuentra en la posicio 1 a lista_nombres
        except:
            lista_nombres.append(np.nan) # En caso de no tener nombre se agrega nan en su lugar

    lista_precios=list() # Se crea una lista vacia donde se añadiran los precios de cada producto 
    lista_promos=list() # Se crea una lista vacia donde se añadiran los precios con descuento (en caso de tener) de cada producto 
    for i in range(len(productos)):  # Con el ciclo se ingresa a cada elemento de la lista productos
        try:
            lista_precios.append(productos[i].find_elements_by_class_name("b-product_price")[0].text.split("\n")[0]) # Se buscan los precios por el nombre de la clase, se separa y se añade el elemento que se encuentra en la posicion 0 a lista_precios
        except:
            lista_precios.append(np.nan) # En caso de no tener precio se agrega nan en su lugar
        try:
            lista_promos.append(productos[i].find_elements_by_class_name("b-product_price")[0].text.split("\n")[1]) # Se buscan los precios con descuento por el nombre de la clase, se separa y se añade el elemento que se encuentra en la posicion 1 a lista_promos
        except:
            lista_promos.append(np.nan) # En caso de no tener precio con descuento se agrega nan en su lugar
            
    df_productos=pd.DataFrame({"Nombre":lista_nombres,"URL":lista_urls,"Precio1":lista_precios,"Precio2":lista_promos}) # Se agregan los nombres de cada columna al DataFrame 
    df_productos["Autoservicio"]="PH" # Se agrega la columna Autoservicio al DataFrame estableciendo que en cada renglon de la misma va el nombre del autoservicio abreviado
    df_productos["Producto"]=producto # Se agrega la columna Producto al DataFrame estableciendo que en cada renglon de la misma va el producto
    df_productos["Fecha"]=time.strftime("%d/%m/%y")  # Se agrega la columna Fecha al DataFrame estableciendo que en cada renglon de la misma va la fecha en la que se hizo la extraccion de datos

    df_productos=df_productos[["Fecha","Autoservicio","Producto","Nombre","URL","Precio1","Precio2"]] # Se reordenan las columnas en el DataFrame

    df_productos=df_productos.reset_index(drop=True)

    datos_webscraper=pd.read_excel("df_productos.xlsx") # Se crea un DataFrame vacio en formato excel

    datos_webscraper=pd.concat([datos_webscraper,df_productos],axis=0) # Se concatena el DataFrame vacio creado en la anterior linea con el creado aqui en el codigo 

    datos_webscraper.to_excel("df_productos.xlsx",index=False) # Ya que estan concatenados ambos DataFrame se convierte a formato excel

    driver.quit() # Finaliza la funcion
    print(df_productos) # Se imprime el DataFrame en individual de cada producto
    
    
"""
El proceso anterior es repetido en esta nueva funcion pero ahora con la pagina
web de Sears abreviandolo como SRS, los comentarios en cada renglon son 
analogos a la funcion anterior
"""  
def Buscador_Precios_Selenium_Sears(producto):

    path="C:\webdriver\chromedriver.exe"
    driver=webdriver.Chrome(path)
    url="https://www.sears.com.mx/resultados/q="+producto+"/pagina=1"
    driver.get(url)
    
    productos= driver.find_elements_by_class_name("cardProduct")
    
    lista_urls=list()
    for i in range(len(productos)):
        try:
            lista_urls.append(productos[i].find_element_by_tag_name("a").get_attribute("href"))
        except:
            lista_urls.append(np.nan)
            
    lista_nombres=list()
    for i in range(len(productos)):
        try:
            lista_nombres.append(productos[i].find_elements_by_tag_name("p")[0].text)
        except:
            lista_nombres.append(np.nan)
            
    lista_precios=list()
    lista_promos=list()
    for i in range(len(productos)):
        try:
            lista_precios.append(productos[i].find_elements_by_class_name("priceDiscountContent")[0].text)
        except:
            lista_precios.append(np.nan)
        try:
            lista_promos.append(productos[i].find_elements_by_class_name("precio1")[0].text)
        except:
            lista_promos.append(np.nan)

    df_productos=pd.DataFrame({"Nombre":lista_nombres,"URL":lista_urls,"Precio1":lista_precios,"Precio2":lista_promos})
    df_productos["Autoservicio"]="SRS"
    df_productos["Producto"]=producto
    df_productos["Fecha"]=time.strftime("%d/%m/%y")

    df_productos=df_productos[["Fecha","Autoservicio","Producto","Nombre","URL","Precio1","Precio2"]]

    df_productos=df_productos.reset_index(drop=True)

    datos_webscraper=pd.read_excel("df_productos.xlsx")

    datos_webscraper= pd.concat([datos_webscraper,df_productos],axis=0)

    datos_webscraper.to_excel("df_productos.xlsx",index=False)

    driver.quit()
    print(df_productos) 
    
"""
El proceso anterior es repetido en esta nueva funcion pero ahora con la pagina
web de Coppel abreviandolo como CPP, los comentarios en cada renglon son 
analogos a las dos funciones anteriores
"""  
def Buscador_Precios_Selenium_Coppel(producto):
    path="C:\webdriver\chromedriver.exe"
    driver=webdriver.Chrome(path)
    url="https://www.coppel.com/SearchDisplay?categoryId=&storeId=10151&catalogId=10051&langId=-5&sType=SimpleSearch&resultCatEntryType=2&showResultsPage=true&searchSource=Q&pageView=&pageGroup=Search&beginIndex=0&pageSize=12&searchTerm="+producto+"&authToken=-1002%252CJdh5JVzqovGDGuZIS9A0yAc11LCiDPi1CWNOoTX%252B9xo%253D"
    driver.get(url)
    
    productos=driver.find_elements_by_class_name("product")
    
    lista_urls=list()
    for i in range(len(productos)):
        try:
            lista_urls.append(productos[i].find_element_by_tag_name("a").get_attribute("href"))
        except:
            lista_urls.append(np.nan)

    lista_nombres=list()
    for i in range(len(productos)):
        try:
            lista_nombres.append(productos[i].find_elements_by_tag_name("p")[0].text.split("\n")[0])
        except:
            lista_nombres.append(np.nan)

    lista_precios=list()
    lista_promos=list()
    for i in range(len(productos)):
        try:
            lista_precios.append(productos[i].find_elements_by_class_name("priceTable")[0].text.split("\n")[0])
        except:
            lista_precios.append(np.nan)
        try:
            lista_promos.append(productos[i].find_elements_by_class_name("price")[0].text)
        except:
            lista_promos.append(np.nan)
            
    df_productos=pd.DataFrame({"Nombre":lista_nombres,"URL":lista_urls,"Precio1":lista_precios,"Precio2":lista_promos})
    df_productos["Autoservicio"]="CPP"
    df_productos["Producto"]=producto
    df_productos["Fecha"]=time.strftime("%d/%m/%y")

    df_productos=df_productos[["Fecha","Autoservicio","Producto","Nombre","URL","Precio1","Precio2"]]

    df_productos=df_productos.reset_index(drop=True)

    datos_webscraper=pd.read_excel("df_productos.xlsx")

    datos_webscraper=pd.concat([datos_webscraper,df_productos],axis=0)

    datos_webscraper.to_excel("df_productos.xlsx",index=False)

    driver.quit()
    print(df_productos) 
    
for productos in ["pantalon","abrigo","playera"]: # Se inicia el ciclo donde ingresaremos los productos de los cuales queremos saber su informacion
    Buscador_Precios_Selenium_Palacio(productos) # Se manda a llamar a la funcion con la tienda de Palacio de Hierro 
    Buscador_Precios_Selenium_Sears(productos) # Se manda a llamar a la funcion con la tienda de Sears
    Buscador_Precios_Selenium_Coppel(productos) # Se manda a llamar a la funcion con la tienda de Coppel
    
df_productos=pd.read_excel("df_productos.xlsx") # El DataFrame previamente creado es leido en formato excel
print(df_productos) # Se imprime el DataFrame ya con la informacion de todos los productos de las 3 paginas web

"""
Se crea la funcion precios floats la cual llevara el codigo donde cambiaremos
los precios de string a floats asi como quitar algunos simbolos o letras sobrantes
"""
def precios_floats(datos):     
    for i in range(len(datos["Precio1"])): # Con el ciclo se ingresa a cada elemento en la columna de Precios1
        try:
            datos["Precio1"].iloc[i]=datos["Precio1"].iloc[i].strip("$") # Se selecciona la columna de Precios1 y se quita el simbolo de pesos ($) en cada renglon
        except:
            pass
        
    for i in range(len(datos["Precio2"])): # Con el ciclo se ingresa a cada elemento en la columna de Precios2
        try:
            datos["Precio2"].iloc[i]=datos["Precio2"].iloc[i].strip("$") # Se selecciona la columna de Precios2 y se quita el simbolo de pesos ($) en cada renglon
        except:
            pass
    
    datos["Precio1"]=datos["Precio1"].replace(",","",regex=True) # Se reemplaza la coma que separa los miles en cada renglon para que quede todo junto en la columna de Precio1 
    datos["Precio2"]=datos["Precio2"].replace(",","",regex=True) # Se reemplaza la coma que separa los miles en cada renglon para que quede todo junto en la columna de Precio2
    
    datos["Precio1"]=datos["Precio1"].replace("M","",regex=True) # En caso de tener alguna letra M se reemplaza en cada renglon para que unicamente quede la cantidad en la columna de Precio1
    datos["Precio2"]=datos["Precio2"].replace("M","",regex=True) # En caso de tener alguna letra M se reemplaza en cada renglon para que unicamente quede la cantidad en la columna de Precio2
    
    datos["Precio1"]=datos["Precio1"].replace("X","",regex=True) # En caso de tener alguna letra X se reemplaza en cada renglon para que unicamente quede la cantidad en la columna de Precio1
    datos["Precio2"]=datos["Precio2"].replace("X","",regex=True) # En caso de tener alguna letra X se reemplaza en cada renglon para que unicamente quede la cantidad en la columna de Precio2
    
    datos["Precio1"]=datos["Precio1"].replace("N","",regex=True) # En caso de tener alguna letra N se reemplaza en cada renglon para que unicamente quede la cantidad en la columna de Precio1
    datos["Precio2"]=datos["Precio2"].replace("N","",regex=True) # En caso de tener alguna letra N se reemplaza en cada renglon para que unicamente quede la cantidad en la columna de Precio2
         
    datos['Precio1'] = pd.to_numeric(datos['Precio1'], errors='coerce') # Se convierten las cantidades de tipo cadena a tipo numerico de la columna Precio1
    datos['Precio2'] = pd.to_numeric(datos['Precio2'], errors='coerce') # Se convierten las cantidades de tipo cadena a tipo numerico de la columna Precio2

    datos.to_excel("df_productos_limpio.xlsx",index=False) # Se crea otro excel con las columnas de Precio1 y Precio2 ya modificadas 
        
    print(datos.dtypes) # Se visualizan los tipos de datos de cada columna 
    return datos

precios_floats(df_productos) # Se aplica la funcion precios floats al DataFrame donde se encuentran todos los productos de las 3 paginas web
df_productos=pd.read_excel("df_productos_limpio.xlsx") # El DataFrame previamente actualizado es concatenado en un nuevo excel 
print(df_productos) # Se imprime el DataFrame ya con las cantidades en tipo numerico y sin los simbolos y/o letras sobrantes

"""
A continuacion se hacen 8 consultas del tipo SQL sobre el ultimo DataFrame 
(el que tiene las cantidades en tipo numerico) que lleva por nombre df_productos 
"""
print("Consultas SQL")
print(ps.sqldf("select Autoservicio, Precio1, Precio2 from df_productos where(Producto='pantalon') and (Precio2 is not null) and (Precio1<800)"))
print(ps.sqldf("select count(*) from df_productos where(Autoservicio='PH') and (599<Precio1) and (Producto='playera')"))
print(ps.sqldf("select sum(Precio1) as sumatotal from df_productos where(Producto='abrigo') and (Precio2 is not null) and(1500<Precio1) and (Autoservicio='PH')"))
print(ps.sqldf("select Producto, Precio1 from df_productos where(Autoservicio='SRS') and (Producto='pantalon') and (Precio1 between '200' and '500')"))
print(ps.sqldf("select count(*) from df_productos where(Autoservicio='CPP' or Autoservicio='PH') and (Precio2 is not null)"))
print(ps.sqldf("select Precio2 from df_productos where(Autoservicio='SRS' or Autoservicio='PH') and (Precio2<999)"))
print(ps.sqldf("select avg(Precio1) as preciopromedio from df_productos where(Autoservicio='PH') and (Producto='pantalon')"))
print(ps.sqldf("select Producto from df_productos where(Autoservicio='SRS' or Autoservicio='CPP' or Autoservicio='PH') and (Precio2 between '1500' and '3000')"))

"""
En esta ultima parte se hacen 4 distintas graficas de barras para comparar
los precios de cada producto entre las 3 distintas tiendas seleccionadas
"""
prueba1=ps.sqldf("select Autoservicio, Precio1 from df_productos where(Producto='pantalon') and (Autoservicio='CPP' or Autoservicio='SRS' or Autoservicio='PH')") # Se declara una variable en donde se guarda la informacion de los precios originales de las 3 tiendas del producto para poder graficarla
graf1=prueba1.plot("Autoservicio","Precio1",kind="bar",color="orange",label="Precios") # Se convierte a plot la variable anterior ademas de elegir el tipo de grafica, el color y poner la leyenda de que estan expresando las barras
plt.title("Precios de Pantalones",fontsize=20) # Se crea el titulo que llevara la grafica junto con el tamaño de la fuente del mismo
plt.ylabel("Precios originales",fontsize=15) # Se agrega el nombre que llevara el eje y junto con el tamaño de la fuente del mismo
plt.xlabel("Tiendas departamentales",fontsize=15) # Se agrega el nombre que llevara el eje x junto con el tamaño de la fuente del mismo
plt.legend() # Se hace esta funcion de plt para que muestre los nombres de los ejes en la grafica
plt.show() # Se muestra la grafica 


"""
Los comentarios de cada renglon de las lineas anteriores son analogos en las
siguientes graficas unicamente cambiando el producto en las primeras 2 y en la 
ultima se agregan los 3 productos
"""
prueba2=ps.sqldf("select Autoservicio, Precio1 from df_productos where(Producto='abrigo') and (Autoservicio='CPP' or Autoservicio='SRS' or Autoservicio='PH')")
graf2 = prueba2.plot("Autoservicio","Precio1",kind ="bar",color="red",label="Precios")
plt.title("Precios de Abrigos",fontsize=20) 
plt.ylabel("Precios originales",fontsize=15)
plt.xlabel("Tiendas departamentales",fontsize=15)
plt.legend()
plt.show()

prueba3=ps.sqldf("select Autoservicio, Precio1 from df_productos where(Producto='playera') and (Autoservicio='CPP' or Autoservicio='SRS' or Autoservicio='PH')")
graf3=prueba3.plot("Autoservicio","Precio1",kind="bar",color="purple",label="Precios") 
plt.title("Precios de Playeras",fontsize=20) 
plt.ylabel("Precios originales", fontsize=15)
plt.xlabel("Tiendas departamentales",fontsize=15)
plt.legend()
plt.show()

prueba4=ps.sqldf("select Autoservicio, Precio1 from df_productos where(Producto='pantalon' or Producto='abrigo' or Producto='playera') and (Autoservicio='CPP' or Autoservicio='SRS' or Autoservicio='PH')")
graf4=prueba4.plot("Autoservicio","Precio1",kind="bar",color="brown",label="Precios") 
plt.title("Precios de todos los productos",fontsize=20) 
plt.ylabel("Precios originales",fontsize= 15) 
plt.xlabel("Tiendas departamentales",fontsize=15)
plt.legend()
plt.show()

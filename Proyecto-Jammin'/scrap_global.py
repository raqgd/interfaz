from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
# from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
import csv
import os
import json

#------------------------------------------------Variables-----------------------------------------------------------------

#Creo la clase para los equipos
class Equipo:
    def __init__(self, id_equipo, nombre_equipo):
        self.id_equipo = id_equipo
        self.nombre_equipo = nombre_equipo

    def obtener_informacion(self):
        return f"ID del equipo: {self.id_equipo}, Nombre del equipo: {self.nombre_equipo}"

#Creo los objetos Equipo
equipos = [
    Equipo(id_equipo=48, nombre_equipo="Alavés"),
    Equipo(id_equipo=21, nombre_equipo="Almería"),
    Equipo(id_equipo=1, nombre_equipo="Athletic"),
    Equipo(id_equipo=2, nombre_equipo="Atlético"),
    Equipo(id_equipo=3, nombre_equipo="Barcelona"),
    Equipo(id_equipo=4, nombre_equipo="Betis"),
    Equipo(id_equipo=499, nombre_equipo="Cádiz"),
    Equipo(id_equipo=5, nombre_equipo="Celta"),
    Equipo(id_equipo=9, nombre_equipo="Getafe"),
    Equipo(id_equipo=222, nombre_equipo="Girona"),
    Equipo(id_equipo=10, nombre_equipo="Granada"),
    Equipo(id_equipo=11, nombre_equipo="Las Palmas"),
    Equipo(id_equipo=408, nombre_equipo="Mallorca"),
    Equipo(id_equipo=50, nombre_equipo="Osasuna"),
    Equipo(id_equipo=14, nombre_equipo="Rayo Vallecano"),
    Equipo(id_equipo=15, nombre_equipo="Real Madrid"),
    Equipo(id_equipo=16, nombre_equipo="Real Sociedad"),
    Equipo(id_equipo=17, nombre_equipo="Sevilla"),
    Equipo(id_equipo=19, nombre_equipo="Valencia"),
    Equipo(id_equipo=20, nombre_equipo="Villarreal"),
]

#----------------------------------------------------Funcion/es-----------------------------------------------------------  

def get_datos(datos):
        #Guardo los datos del jugador(Nombre y Apellido)
        name = driver.find_element(By.XPATH, "//div[@class='player-info']//div[@class='name']").text
        surname = driver.find_element(By.XPATH, "//div[@class='player-info']//div[@class='surname']").text
        nombre = name + " " + surname
        datos.append(nombre)
        print(datos)

        #Utiliza BeautifulSoup para encontrar el nombre del equipo
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        team_name = soup.find('a', {'class': 'btn btn-sw-link', 'data-title': True})
        if team_name:
            nombre_mi_equipo = team_name['data-title']
            datos.append(nombre_mi_equipo)
        else:
            print(name, surname, "Nombre del equipo no encontrado")
        
        #Guarda la posicion
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        pos_1 = soup.find('i', {'class': 'pos-1 pos-big'})
        pos_2 = soup.find('i', {'class': 'pos-2 pos-big'})
        pos_3 = soup.find('i', {'class': 'pos-3 pos-big'})
        pos_4 = soup.find('i', {'class': 'pos-4 pos-big'})
           
        if pos_1:
            nombre_pos = "Portero"
            datos.append(nombre_pos)
                
        if pos_2:
            nombre_pos = "Defensa"
            datos.append(nombre_pos)

        if pos_3:
            nombre_pos = "Centro"
            datos.append(nombre_pos)
            
        if pos_4:
            nombre_pos = "Delantero"
            datos.append(nombre_pos)
        
        
        # Guardo los valores del jugador(Valor, Puntos, Media, Partidos, Goles y Tarjetas)
        wait = WebDriverWait(driver, 10)  # Espera hasta 10 segundos
        tabla_valores = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'label-value-scroll')))
        items = tabla_valores.find_elements(By.CLASS_NAME, "item")     
        for item in items:
            valor = item.find_element(By.CLASS_NAME, "value")
            datos.append(valor.text)
        

        #Guardo el rival del proximo partido y si juegan en casas o fuera
        array_rivales = []
        array_numeros = []
        casa_o_fuera = 0;
        box_match = driver.find_element(By.CLASS_NAME, 'box-next-match')
        tabla_valores = box_match.find_element(By.CLASS_NAME, 'label-value-flex')
        item_rival = tabla_valores.find_element(By.CLASS_NAME, "item")
        value = item_rival.find_element(By.CLASS_NAME, "value")
        
        rivales = value.find_elements(By.CLASS_NAME, "team-logo")
        for rival in rivales:
            url = rival.get_attribute("src")
            nombre_archivo = os.path.basename(url) # Obtener el nombre del archivo de la URL
            numero, extension = os.path.splitext(nombre_archivo)  # Separar el número y la extensión
            array_numeros.append(numero)
        #Lo paso de numero a nombre
        i=0
        while i < len(equipos):
            if(str(equipos[i].id_equipo) == array_numeros[0]):
                nombre = equipos[i].nombre_equipo
                array_rivales.append(nombre)
            i+=1
        i=0
        while i < len(equipos):
            if(str(equipos[i].id_equipo) == array_numeros[1]):
                nombre =equipos[i].nombre_equipo
                array_rivales.append(nombre)
            i+=1

        #Comprubeo cual de los dos es el rival COMPROBAR SI VA BIEN
        if (array_rivales[0] == nombre_mi_equipo):
                datos.append(array_rivales[1])
                casa_o_fuera = 0
        elif(array_rivales[1] == nombre_mi_equipo):
                datos.append(array_rivales[0])
                casa_o_fuera = 1
        datos.append(casa_o_fuera)
        print(datos)


        #Guardo la media en casa y fuera. Usamos tabla_valores
        item_rivales = tabla_valores.find_elements(By.CLASS_NAME, "item")
        estad_rivales = []
        i=2
        for i in range(len(item_rivales)):
            valor = item_rivales[i].find_element(By.CLASS_NAME, "value")
            estad_rivales.append(valor.text) 
            i += 1
        estad_rivales.pop(0)
        datos.extend(estad_rivales)
        
        time.sleep(1)
        
        #Miro si hay alguna lesion y la guardo como estado
        try:
            status = driver.find_element(By.CLASS_NAME, 'box alert-status')
            status_al = status.find_element(By.CLASS_NAME, 'alert-content')
            texto_status = status_al.find_element(By.XPATH, "/html/body/div[3]/div[6]/div/div[1]/div/div/p")
            datos.append(texto_status)
            
        except NoSuchElementException:
            texto_status = "En forma"
            datos.append(texto_status)

        #Guardo num de la jornada y puntuación
        jornada = driver.find_element(By.XPATH, "//div[@class='line btn btn-player-gw']")
        jornada_num = jornada.find_element(By.CLASS_NAME, "gw") # Jornada num
        try:
            jornada_score = jornada.find_element(By.CLASS_NAME, "score") #Score
            score = jornada_score.get_attribute("innerHTML")
        except NoSuchElementException:
            score = 0;
        jnum = jornada_num.get_attribute("innerHTML")
        # score = jornada_score.get_attribute("innerHTML")
        datos.append(jnum)
        datos.append(score)

#------------------------------------------------Cabecera--------------------------------------------------------

#Hago el array que contiene la cabecera
cabecera = ['Nombre y apellido', 'Team', 'Posicion', 'Value', 'Points', 'Average', 'Matches', 'Goals', 'Cards', 'Rival', '¿Casa o Fuera?', 'Media en Casa', 'Media fuera', 'Estado', 'Nº Jornada', 'Puntos'] 
#Los uno en el array cabecera segun la posicion y escribo la cabecera 
# Ruta del archivo
archivo_csv = "logo/carpeta_csv/scraping_total.csv"
# Comprobar si el archivo existe
if os.path.exists(archivo_csv):
    print(f"El archivo {archivo_csv} ya existía")
else:
    with open('logo/carpeta_csv/scraping_total.csv', mode='a', newline='', encoding = 'utf-8-sig') as archivo_csv:
        escritor_csv = csv.writer(archivo_csv, delimiter=';')
        escritor_csv.writerow(cabecera) 
    print(f"El archivo {archivo_csv} no tenía cabecera, se ha escrito una nueva.")
    
#-------------------------------------------Drivers e Inicio de Sesion-------------------------------------------

#Cargo los drivers y la web
driver = webdriver.Chrome()
url = 'https://misterfantasy.es/es/'
driver.get(url)

time.sleep(1)

#Pincho en el boton jugar
boton = driver.find_element(By.XPATH, '/html/body/main/div[1]/div/div/div[1]/a')
boton.click()

#Rechazo las cookies
element = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div/div/div/div[2]/button[2]/span'))
)
element.click()
#Skip tutorial
element = WebDriverWait(driver, 100).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div[2]/div[2]/button'))
)
for skipTutorial in range(4):
    element.click()
    time.sleep(1)

#Voy al gmail e inicio sesion
boton = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[2]/div/button[3]')
boton.click()
gmail = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[2]/div/form/div[1]/input')
gmail.send_keys('jammin060@gmail.com')
contraseña = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[2]/div/form/div[2]/input')
contraseña.send_keys('Pc1Pc2@#')
boton = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[2]/div/form/div[3]/button')
boton.click()

time.sleep(1)

#------------------------------------------------Todos los Jugadores-----------------------------------------------------

# Voy al apartado mas
boton = driver.find_element(By.XPATH, '/html/body/div[3]/header/div[2]/ul/li[5]')
boton.click()

time.sleep(1)

# Entro en los jugadores
boton = driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/div[1]/button[2]')
boton.click()

time.sleep(2)

# damos a ver mas
avanzar = 10
intento = 0
while intento < avanzar:
    time.sleep(2)

    try:
        driver.execute_script("window.scrollTo(0, 50000);")
        boton = driver.find_element(By.XPATH, "/html/body/div[6]/div[3]/div[3]/div[1]/button")

        # Si encuentra el botón, clickea
        boton.click()

    except NoSuchElementException:
        print("Botón no encontrado en el intento", intento + 1)
        break  # Sale del bucle si no se encuentra el botón

    intento += 1

# Guardo los enlaces de los jugadores
array_jugadores = []
jugadores = driver.find_element(By.CLASS_NAME, "player-list")
link = jugadores.find_elements(By.CLASS_NAME, "btn-sw-link")
array_jugadores = [i.get_attribute("href") for i in link]

for array_jugador in array_jugadores:
    datos = []
    driver.get(array_jugador)
    get_datos(datos)
    with open('carpeta_csv/scraping_total.csv', mode='a', newline='', encoding = 'utf-8-sig') as archivo_csv:
            escritor_csv = csv.writer(archivo_csv, delimiter=';')
            escritor_csv.writerow(datos)
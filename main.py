from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi
#importaciones necesarias para el scrapeo
from PyQt5.QtCore import QThread, pyqtSignal
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
import sys
import csv
import re

#Clase QThread para ejecutar selenium en paralelo
class SeleniumThread(QThread):
    finished_signal = pyqtSignal(list, str, list)

    def __init__(self):
        super().__init__()

    def run(self):
        try:
            # CÓDIGO DE SELENIUM
            sys.stdout.reconfigure(encoding='utf-8')

            #Establecemos la página que queremos abrir
            driver = webdriver.Chrome()
            url = 'https://mister.mundodeportivo.com/'

            #Abrir adblock
            options = webdriver.ChromeOptions()
            options.add_argument('--ignore-certificate-errors')
            options.add_argument('--disable-notifications')
            driver = webdriver.Chrome(options=options)
            driver.maximize_window()

            #Abrimos la página
            driver.get(url)
            time.sleep(1)

            #Aceptar cookies
            wait = WebDriverWait(driver, 10)
            boton_cookies = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div/div/div[2]/button[2]')
            boton_cookies.click()

            time.sleep(0.2)

            #Le damos a empezar 4 veces
            for i in range(4):
                    boton_empezar = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[2]/div[2]/button')
                    boton_empezar.click()
                    time.sleep(0.2)

            #Darle al boton iniciar con google
            boton_google = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[2]/div/button[3]')
            boton_google.click()
            time.sleep(.5)

            #Metemos el email
            email = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[2]/div/form/div[1]/input')
            email.send_keys('dreamleagueassistant@gmail.com')
            time.sleep(0.2)

            #Metemos contraseña
            password = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[2]/div/form/div[2]/input')
            password.send_keys('PC1_GR_ 4')
            time.sleep(0.2)

            #Le damos a iniciar sesion
            boton_iniciar = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[2]/div/form/div[3]/button')
            boton_iniciar.click()
            time.sleep(.5)


            #Nos vamos al equipo
            boton_mercado = driver.find_element(By.XPATH, '//*[@id="content"]/header/div[2]/ul/li[3]/a')
            boton_mercado.click()
            time.sleep(.5)

            #Encontramos media total
            media_total = driver.find_element(By.XPATH, '//*[@id="content"]/div[2]/div[3]/div[1]/div[2]/div[1]').get_attribute('innerText')
            media_total_numero = media_total.split()[2].replace(',', '.')

            #Encontramos media portero
            media_portero = driver.find_element(By.XPATH, '//*[@id="content"]/div[2]/div[3]/div[1]/div[2]/div[2]').get_attribute('innerText')
            media_portero = media_portero.replace(',', '.')

            #Encontramos media defensa
            media_defensa = driver.find_element(By.XPATH, '//*[@id="content"]/div[2]/div[3]/div[1]/div[2]/div[3]').get_attribute('innerText')
            media_defensa = media_defensa.replace(',', '.')

            #Encontramos media mediocentro
            media_mediocentro = driver.find_element(By.XPATH, '//*[@id="content"]/div[2]/div[3]/div[1]/div[2]/div[4]').get_attribute('innerText')
            media_mediocentro = media_mediocentro.replace(',', '.')

            #Encontramos media delantero
            media_delantero = driver.find_element(By.XPATH, '//*[@id="content"]/div[2]/div[3]/div[1]/div[2]/div[5]').get_attribute('innerText')
            media_delantero = media_delantero.replace(',', '.')

            # Econtramos el presupuesto del equipo
            presupuesto = driver.find_element(By.XPATH, '//*[@id="content"]/div[2]/div[5]/div/div[1]/div[2]').get_attribute('innerText')

            #Nos vamos a tabla de clasificación
            boton_clasificacion = driver.find_element(By.XPATH, '//*[@id="content"]/header/div[2]/ul/li[4]/a')
            boton_clasificacion.click()
            time.sleep(.5)

            #clickamos general
            boton_general = driver.find_element(By.XPATH, '//*[@id="content"]/div[2]/div[1]/div/button[1]')
            boton_general.click()
            time.sleep(.5)

            contenedor_equipos = driver.find_element(By.XPATH, '//*[@id="content"]/div[2]/div[2]/div[1]/ul')
            equipos = contenedor_equipos.find_elements(By.CLASS_NAME, 'user-row')

            estadisticas_equipo = []

            for equipo in equipos:
                    info = equipo.find_element(By.CLASS_NAME, 'info')
                    nombre = info.find_element(By.CLASS_NAME, 'name').get_attribute('innerText')

                    if nombre == 'M31-G4-DLA':
                            jugadores_y_precio = info.find_element(By.CLASS_NAME, 'played').get_attribute('innerText')
                            jugadores, precio = jugadores_y_precio.split(' · ')
                            jugadores = jugadores.replace(' jugadores', '')
                            points = equipo.find_element(By.CLASS_NAME, 'points').get_attribute('innerText')

                            matches = re.findall(r'([+-]?\d+)', points)

                            # El primer elemento en 'matches' es el número de puntos
                            num_puntos = int(matches[0])
                            try:
                                    # El segundo elemento en 'matches' es el diferencial de puntos con el signo
                                    dif_puntos = int(matches[1])
                            except:
                                    dif_puntos = 0

                            equipo_stats = {
                            'Nombre': nombre,
                            'jugadores': jugadores,
                            'Valor de plantilla': precio,
                            'Puntos': num_puntos,
                            'Diferencial de puntos': dif_puntos,
                            'Media total': media_total_numero,
                            'Media portero': media_portero,
                            'Media defensa': media_defensa,
                            'Media mediocentro': media_mediocentro,
                            'Media delantero': media_delantero,
                            'Presupuesto': presupuesto
                            }
                            estadisticas_equipo.append(equipo_stats)

            with open('estadisticas_equipo.csv', 'w', newline='', encoding='utf-8') as csvfile:
                    fieldnames = ['Nombre', 'jugadores', 'Valor de plantilla', 'Puntos', 'Diferencial de puntos', 'Media total', 'Media portero', 'Media defensa', 'Media mediocentro', 'Media delantero', 'Presupuesto']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                    writer.writeheader()
                    for equipo in estadisticas_equipo:
                            writer.writerow(equipo)

            # For example, let's simulate some Selenium actions
            title = driver.title
            driver.quit()

            # Emit the signal with the result
            self.finished_signal.emit(['Selenium Thread Finished'], estadisticas_equipo)
            
        except Exception as e:
            print(f"Error en SeleniumThread: {str(e)}")
        finally:
            # Asegúrate de cerrar el controlador incluso si ocurre una excepción
            driver.quit()
        
#Clase de ejecución de la ventana
class MiVentana(QMainWindow):
    def __init__(self):
        super(MiVentana, self).__init__()

        # Cargar la interfaz de usuario diseñada en Qt Designer
        loadUi("dla.ui", self)  # Reemplaza "ventana.ui" con el nombre de tu archivo .ui

        # Clickar boton equipo lleva a pagina equipo
        self.botonequipo.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.equipo_page))

        # Clickar boton predicciones lleva a pagina predicciones
        self.botonpredicciones.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.predicciones_page))

        # Create an instance of the SeleniumThread
        self.selenium_thread = SeleniumThread()

        # Connect signals between the thread and the UI
        self.selenium_thread.finished_signal.connect(self.on_selenium_thread_finished)

        # Start the SeleniumThread when the UI is loaded
    def on_selenium_thread_finished(self, result, team_stats):
        print(result)
        print(team_stats)
        #print(f"Scraped data for team: {budget}")

        # Llamar al método leercsv después de la ejecución de Selenium
        datos_equipo = []
        self.leercsv(datos_equipo)

        # Imprimir la lista con los datos del equipo
        print(datos_equipo[0]['Nombre'])

    #funcion para leer csv
    def leercsv(self, datos_equipo):
        # Leer el archivo CSV y almacenar los datos en una lista 
        csv_equipo = 'estadisticas_equipo.csv'

        with open(csv_equipo, 'r', encoding='utf-8') as csvfile:
            csvreader = csv.reader(csvfile, delimiter=';')
            # Saltar la primera fila (encabezado)
            next(csvreader, None)
            for row in csvreader:
        # Crear un diccionario con los nombres de las columnas y los valores de la fila
                equipo_info = {
                    'Nombre': row[0],
                    'Jugadores': int(row[1]),
                    'Valor de plantilla': row[2],
                    'Puntos': int(row[3]),
                    'Diferencial de puntos': int(row[4]),
                    'Media total': float(row[5]),
                    'Media portero': float(row[6]),
                    'Media defensa': float(row[7]),
                    'Media mediocentro': float(row[8]),
                    'Media delantero': float(row[9]),
                    'Presupuesto': row[10]
                }
                # Agregar el diccionario a la lista
                datos_equipo.append(equipo_info)

        
if __name__ == "__main__":
    app = QApplication([])
    ventana = MiVentana()
    ventana.show()
    app.exec_()
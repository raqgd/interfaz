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
import subprocess
import sys
import csv
import re
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import json


#Clase de ejecución de la ventana
class MiVentana(QMainWindow):
    def __init__(self):
        super(MiVentana, self).__init__()

        # Cargar la interfaz de usuario diseñada en Qt Designer
        loadUi("dla.ui", self)  # Reemplaza "ventana.ui" con el nombre de tu archivo .ui

        #Funcionalidades página
        # Clickar boton equipo lleva a pagina equipo
        self.botonequipo.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.equipo_page))

        # Clickar boton predicciones lleva a pagina predicciones
        self.botonpredicciones.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.predicciones_page))


#CODIGOS SCRAPEO    

#CÓDIGO 1: SCRAPEAR NUESTRO EQUIPO

    
    def scrapequipo(self):
        sys.stdout.reconfigure(encoding='utf-8')
        subprocess.run(['python', 'scrapequipo.py'])

#CÓDIGO 2: SCRAPEO DATOS JUGADORES

    def scrapDatosJugadores(self):
        sys.stdout.reconfigure(encoding='utf-8')
        subprocess.run(['python', 'PricesPlayers.py'])


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
                    'Puntos': float(row[3]),
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

    def scrapTeamMarketButtonClicked(self):
        # Ejecutar los scripts al presionar el botón
        subprocess.run(['python', 'scrap_team.py'])
        subprocess.run(['python', 'scrap_market.py'])

        time.sleep(2)

        data_list_market = []
        data_list_team = []
        self.readCsvForTextBrowser(data_list_market, data_list_team)

        # Imprimir los datos en teamResults
        formatted_data = '\n'.join(data_list_market)
        self.marketResults.setPlainText(formatted_data)

        # Imprimir los datos en teamResults
        formatted_data = '\n'.join(data_list_team)
        self.teamResults.setPlainText(formatted_data)

    #ejecutar codigos de scrapeo
        
        # Llamar al método de scraping al iniciar la interfaz
        self.scrapDataOnUIStart()

    def scrapDataOnUIStart(self):
        # Agrega aquí el código de scraping que deseas ejecutar al iniciar la interfaz
        self.scrapequipo()
        self.scrapDatosJugadores()
        

#main
        
if __name__ == "__main__":
    app = QApplication([])
    ventana = MiVentana()
    ventana.show()
    app.exec_()
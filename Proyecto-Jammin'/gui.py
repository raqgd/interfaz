import sys
import subprocess
import time
import csv
import fileinput
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QTextBrowser, QComboBox
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.svm import SVC

class mainY(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Jammin' - Proyecto de Computación I")
        self.setGeometry(100, 100, 800, 400)

        # Widgets
        self.projectNameLabel = QLabel("Jammin' - Proyecto de Computación I")
        self.scrapTeamMarketButton = QPushButton('Scrapear Mercado y Equipo')
        self.scrapButton = QPushButton('Scrapear Todo')
        self.teamLabel = QLabel("Mercado")
        self.marketLabel = QLabel("Equipo")
        self.teamResults = QTextBrowser()
        self.marketResults = QTextBrowser()
        self.modelLabel = QLabel("Elige el modelo para hacer el análisis. Se necesita haber scrapeado previamente.")
        self.modelComboBox = QComboBox()  # Agrega esta línea para crear el QComboBox
        self.modelComboBox.addItem('Regresión Logística')
        self.modelComboBox.addItem('Random Forest Classifier')
        self.modelCompraButton = QPushButton('Predicción de Compra')
        self.resultsModel = QTextBrowser()
        self.membersLabel = QLabel("Hecho por Javier da Silva Costa, Paula Sáenz, Mario Redondo y Rafael Sánchez")
        self.copyrightLabel = QLabel("Jammin© - Universidad Europea de Madrid (UEM)")
        self.modelVentaButton = QPushButton('Predicción de Venta')
        self.resultsModelV = QTextBrowser()
        self.modeloVender = QLabel("El modelo utilizado ha sido Random Forest Regressor")
        # Layouts
        intro_layout = QVBoxLayout()
        intro_layout.addWidget(self.projectNameLabel)
        intro_layout.addWidget(self.scrapTeamMarketButton)
        intro_layout.addWidget(self.scrapButton)

        name_team_market_layout = QHBoxLayout()
        name_team_market_layout.addWidget(self.teamLabel)
        name_team_market_layout.addWidget(self.marketLabel)

        team_market_layout = QHBoxLayout()
        team_market_layout.addWidget(self.marketResults)
        team_market_layout.addWidget(self.teamResults)

        model_layout = QVBoxLayout()
        model_layout.addWidget(self.modelLabel)
        model_layout.addWidget(self.modelComboBox)  # Agrega esta línea para agregar el QComboBox al layout
        model_layout.addWidget(self.modelCompraButton)
        model_layout.addWidget(self.resultsModel)
        model_layout.addWidget(self.modelVentaButton)
        model_layout.addWidget(self.modeloVender)
        model_layout.addWidget(self.resultsModelV)
        model_layout.addWidget(self.membersLabel)
        model_layout.addWidget(self.copyrightLabel)
        

        main_layout = QVBoxLayout()
        main_layout.addLayout(intro_layout)
        main_layout.addLayout(name_team_market_layout, stretch=1)
        main_layout.addLayout(team_market_layout, stretch=1)
        main_layout.addLayout(model_layout)
    
        self.setLayout(main_layout)

        # Conectar la señal clicked del botón a la función correspondiente
        self.scrapTeamMarketButton.clicked.connect(self.scrapTeamMarketButtonClicked)
        self.scrapButton.clicked.connect(self.scrapButtonClicked)
        self.modelCompraButton.clicked.connect(self.modelCompraButtonClicked)
        self.modelVentaButton.clicked.connect(self.modelVentaButtonClicked)
        self.show()

    def onComboBoxChanged(self, index):
        # Este método se llama cuando cambia la selección en el QComboBox
        selected_option = self.sender().currentText()
        print(f'Opción seleccionada: {selected_option}')

    def readCsvForTextBrowser(self, data_list_market, data_list_team):
        # Leer el archivo CSV y almacenar los datos en una lista
        csv_file_path_market = 'carpeta_csv/scraping_mercado.csv' 
        csv_file_path_team = 'carpeta_csv/scraping_equipo.csv'

        with open(csv_file_path_market, 'r', encoding='utf-8') as csvfile:
            csvreader = csv.reader(csvfile, delimiter=';')
            # Saltar la primera fila (encabezado)
            next(csvreader, None)
            for row in csvreader:
                importantOnly = row[:4]
                player_info = f"· {', '.join(importantOnly)}"
                data_list_market.append(player_info)

        player_info = ""
        with open(csv_file_path_team, 'r', encoding='utf-8') as csvfile:
            csvreader = csv.reader(csvfile, delimiter=';')
            # Saltar la primera fila (encabezado)
            next(csvreader, None)
            for row in csvreader:
                importantOnly = row[:4]
                player_info = f"· {', '.join(importantOnly)}"
                data_list_team.append(player_info)

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

    def scrapButtonClicked(self):
        # Ejecutar los scripts al presionar el botón
        subprocess.run(['python', 'scrap_team.py'])
        subprocess.run(['python', 'scrap_market.py'])
        subprocess.run(['python', 'scrap_global.py'])

        time.sleep(5)

        data_list_market = []
        data_list_team = []
        self.readCsvForTextBrowser(data_list_market, data_list_team)

        # Imprimir los datos en teamResults
        formatted_data = '\n'.join(data_list_market)
        self.marketResults.setPlainText(formatted_data)

        # Imprimir los datos en teamResults
        formatted_data = '\n'.join(data_list_team)
        self.teamResults.setPlainText(formatted_data)

    def modelCompraButtonClicked(self):
        self.resultsModel.clear()
        selected_model = self.modelComboBox.currentText()

        # Modificar el separador de ; a , en el archivo CSV original
        csv_file_path = 'carpeta_csv/scraping_total.csv'
        
        # Leer el archivo CSV original con ; como delimitador
        modelo = pd.read_csv(csv_file_path, encoding='utf-8', sep=';')
        
        modelo = modelo[modelo['Rival'] != "0"]
        
        columnas_a_modificar = ['Media en Casa', 'Media fuera', 'Average']
        columnas_a_factorizar = ['Team', 'Posicion', 'Rival', 'Estado']
        modelo['Nº Jornada'] = modelo['Nº Jornada'].str.replace('J', '')
        for columna in columnas_a_factorizar:
            modelo[columna], _ = pd.factorize(modelo[columna])
        
        for columna in modelo.columns:
            if columna in columnas_a_modificar:
                modelo[columna] = modelo[columna].replace('[.,]', '', regex=True).astype(float)
                modelo[columna] = modelo[columna].replace(',', '.', regex=False).astype(float)
        
        features = ['Points', 'Average', 'Matches', 'Goals', 'Cards', 'Media en Casa', 'Media fuera', 'Nº Jornada']
        X = modelo[features]
        y = modelo['Value']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        if selected_model == 'Regresión Logística':
            model = LogisticRegression()
        elif selected_model == 'Random Forest Classifier':
            model = RandomForestClassifier()
        else:
            print("Modelo no reconocido.")
            return
            
        # Entrenar el modelo
        model.fit(X_train_scaled, y_train)
        
        # Realizar predicciones
        predictions = model.predict(X_test_scaled)

        # Obtener características relevantes para hacer predicciones
        features = ['Points', 'Average', 'Matches', 'Goals', 'Cards', 'Media en Casa', 'Media fuera', 'Nº Jornada']
        csv_file_mercado = 'carpeta_csv/scraping_mercado.csv'  # Cambiar a scraping_mercado.csv
        
        # Leer el archivo CSV original con ; como delimitador
        df_mercado = pd.read_csv(csv_file_mercado, encoding='utf-8', sep=';')
        df_mercado = df_mercado[df_mercado['Rival'] != "0"]
        # Modificar los valores en la columna 'Value'
        
        # Columnas que deseas factorizar
        columnas_a_factorizar = ['Team', 'Rival', 'Estado']
        df_mercado['Nº Jornada'] = df_mercado['Nº Jornada'].str.replace('J', '')
        df_mercado['Nº Jornada'] = (df_mercado['Nº Jornada'].astype(int) + 1).astype(str)
        # Iterar sobre las columnas y aplicar la factorización
        for columna in columnas_a_factorizar:
            df_mercado[columna], _ = pd.factorize(df_mercado[columna])
        # Iterar sobre todas las columnas y modificar los datos si la columna está en columnas_a_modificar
        for columna in df_mercado.columns:
            if columna in columnas_a_modificar:
                df_mercado[columna] = df_mercado[columna].replace('[.,]', '', regex=True)
                df_mercado[columna] = df_mercado[columna].str.replace(',', '.', regex=False).astype(float)

        # Crear un diccionario para almacenar los jugadores recomendados por posición
        jugadores_recomendados_por_posicion = {}
        
        # Obtener las posiciones únicas en el conjunto de datos del mercado
        posiciones_unicas = df_mercado['Posicion'].unique()
        
        # Iterar sobre las posiciones y encontrar el jugador más recomendado para cada posición
        for posicion in posiciones_unicas:
            # Filtrar jugadores del mercado por posición
            jugadores_posicion = df_mercado[df_mercado['Posicion'] == posicion].copy()
        
            # Seleccionar las mismas características que usaste para entrenar el modelo
            X_posicion = jugadores_posicion[features]
        
            # Escalar características para mejorar el rendimiento del modelo (usando el mismo scaler que en el modelo original)
            X_posicion_scaled = scaler.transform(X_posicion)
               
            # Realizar predicciones para los jugadores de la posición
            predictions_posicion = model.predict(X_posicion_scaled)
        
            # Agregar las predicciones como una nueva columna en el DataFrame de la posición
            jugadores_posicion['Predicted_Value'] = predictions_posicion
        
            # Convertir las columnas 'Predicted_Value' y 'Value' a tipos numéricos, eliminando los puntos y comas
            jugadores_posicion['Predicted_Value'] = pd.to_numeric(jugadores_posicion['Predicted_Value'].str.replace('[.,]', '', regex=True))
            jugadores_posicion['Value'] = pd.to_numeric(jugadores_posicion['Value'].str.replace('[.,]', '', regex=True))
        
            # Calcular la diferencia entre 'Predicted_Value' y 'Value' actual
            jugadores_posicion['Difference'] = jugadores_posicion['Predicted_Value'] - jugadores_posicion['Value']
        
            # Ordenar el DataFrame por 'Difference' en orden descendente
            jugadores_posicion = jugadores_posicion.sort_values(by='Difference', ascending=False)
        
            # Imprimir información sobre los jugadores recomendados por posición
            result_text = f"Jugadores Recomendados para la Posición {posicion}:\n"
            for _, jugador_recomendado_posicion in jugadores_posicion.iterrows():
                nombre_jugador = jugador_recomendado_posicion['Nombre y apellido']  # Reemplaza 'Nombre' con la columna real que contiene los nombres
                diferencia = jugador_recomendado_posicion['Difference']
                precio_actual = jugador_recomendado_posicion['Value']
                # Construir la cadena con la información del jugador y la diferencia
                if diferencia > 0:
                    result_text += f"{nombre_jugador}: +{diferencia} ↗ ------------------ Precio Actual: {precio_actual}\n"
                elif diferencia == 0:
                    result_text += f"{nombre_jugador}: {diferencia} ------------------ Precio Actual: {precio_actual}\n"
                else:
                    result_text += f"{nombre_jugador}: {diferencia} ↘ ------------------ Precio Actual: {precio_actual}\n"
    
            result_text += "\n"
    
            # Establecer el texto en el QTextBrowser
            self.resultsModel.append(result_text)
    def modelVentaButtonClicked(self):
        self.resultsModelV.clear()
    
        # Modificar el separador de ; a , en el archivo CSV original
        csv_file_path = 'carpeta_csv/scraping_total.csv'
        
        # Leer el archivo CSV original con ; como delimitador
        modelo = pd.read_csv(csv_file_path, encoding='utf-8', sep=';')
        
        modelo = modelo[modelo['Rival'] != "0"]
        modelo['Value'] = pd.to_numeric(modelo['Value'].replace('[.,]', '', regex=True)).astype(float)
        columnas_a_modificar = ['Media en Casa', 'Media fuera', 'Average']
        columnas_a_factorizar = ['Team', 'Posicion', 'Rival', 'Estado']
        modelo['Nº Jornada'] = modelo['Nº Jornada'].str.replace('J', '')
        for columna in columnas_a_factorizar:
            modelo[columna], _ = pd.factorize(modelo[columna])
        
        for columna in modelo.columns:
            if columna in columnas_a_modificar:
                modelo[columna] = modelo[columna].replace('[.,]', '', regex=True).astype(float)
                modelo[columna] = modelo[columna].replace(',', '.', regex=False).astype(float)
        
        features = ['Points', 'Average', 'Matches', 'Goals', 'Cards', 'Media en Casa', 'Media fuera', 'Nº Jornada']
        X = modelo[features]
        y = modelo['Value']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
    
        model = RandomForestRegressor()    
        model.fit(X_train_scaled, y_train)
    
        # Leer el archivo CSV de scraping_equipo.csv
        csv_file_path_equipo = 'carpeta_csv/scraping_equipo.csv'
        df_equipo = pd.read_csv(csv_file_path_equipo, encoding='utf-8', sep=';')
    
        # Aplicar las mismas transformaciones que se hicieron durante el entrenamiento del modelo
        df_equipo['Nº Jornada'] = df_equipo['Nº Jornada'].str.replace('J', '')
        for columna in columnas_a_factorizar:
            df_equipo[columna], _ = pd.factorize(df_equipo[columna])
    
        for columna in df_equipo.columns:
            if columna in columnas_a_modificar:
                df_equipo[columna] = df_equipo[columna].replace('[.,]', '', regex=True).astype(float)
                df_equipo[columna] = df_equipo[columna].replace(',', '.', regex=False).astype(float)
    
        # Seleccionar las mismas características que usaste para entrenar el modelo
        X_equipo = df_equipo[features]
    
        # Escalar características para mejorar el rendimiento del modelo
        X_equipo_scaled = scaler.transform(X_equipo)
    
        # Realizar predicciones para los jugadores del equipo
        predictions_equipo = model.predict(X_equipo_scaled)
    
        # Agregar las predicciones como una nueva columna en el DataFrame original
        df_equipo['Predicted_Value'] = predictions_equipo
    
        # Convertir las columnas 'Predicted_Value' y 'Value' a tipos numéricos, eliminando los puntos y comas
        df_equipo['Predicted_Value'] = pd.to_numeric(df_equipo['Predicted_Value'].replace('[.,]', '', regex=True))
        df_equipo['Value'] = pd.to_numeric(df_equipo['Value'].replace('[.,]', '', regex=True))
    
        # Calcular la diferencia entre 'Predicted_Value' y 'Value' actual
        df_equipo['Difference'] = df_equipo['Predicted_Value'] - df_equipo['Value']
    
        # Ordenar el DataFrame por 'Difference' en orden descendente
        df_equipo = df_equipo.sort_values(by='Difference', ascending=False)
    
        # Tomar los 3 jugadores con la peor diferencia
        jugadores_venta = df_equipo.tail(3)
    
        # Imprimir información sobre los 3 jugadores con la peor diferencia y su predicted_value
        result_text = "3 Jugadores que deberías vender:\n"
        for _, jugador_venta in jugadores_venta.iterrows():
            nombre_jugador = jugador_venta['Nombre y apellido']  # Reemplaza 'Nombre' con la columna real que contiene los nombres
            diferencia = jugador_venta['Difference']
            predicted_value = jugador_venta['Predicted_Value']
            precio_actual = jugador_venta['Value']
            # Construir la cadena con la información del jugador, la diferencia y el predicted_value
            result_text += f"{nombre_jugador}: Diferencia: {diferencia}, Valor Futuro: {predicted_value} Valor Actual: {precio_actual}\n"
    
        # Establecer el texto en el QTextBrowser
        self.resultsModelV.append(result_text)


def main():
    app = QApplication(sys.argv)
    ex = mainY()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

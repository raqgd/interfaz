import time
import re

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import csv

# URL del formulario de inicio de sesión
login_url = 'https://mister.mundodeportivo.com/new-onboarding/auth/email'

# Datos de inicio de sesión (correo electrónico y contraseña)
email = 'dreamleagueassistant@gmail.com'
password = 'PC1_GR_ 4'

# Configura el navegador
driver = webdriver.Chrome()
driver.get(login_url)

# Acepto las cookies si salen y si no hago un pass
try:
    cookies_accept_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'didomi-notice-agree-button')))
    cookies_accept_button.click()
except:
    pass

# Encuentra el campo de correo electrónico y contraseña e ingresa los datos
email_field = driver.find_element(By.ID, 'email')
password_field = driver.find_element(By.XPATH, '//input[@placeholder="Contraseña"]')

email_field.send_keys(email)
password_field.send_keys(password)

# Envía el formulario
password_field.send_keys(Keys.RETURN)

time.sleep(5)

driver.get('https://mister.mundodeportivo.com/more#players')

button = True

while button:

    try:
        driver.find_element(By.CLASS_NAME, 'search-players-more')
        time.sleep(3)
        driver.find_element(By.CLASS_NAME, 'search-players-more').click()
    except:
        button = False


enlaces = []

jugadores_card = driver.find_element(By.CLASS_NAME, 'player-list').find_elements(By.TAG_NAME, 'li')

for j in jugadores_card:
    enlaces.append(j.find_element(By.TAG_NAME, 'a').get_attribute('href'))

for z, e in enumerate(enlaces):

    driver.get(e)

    regex_id = r'/players/(\d+)'
    id = int(re.search(regex_id, e).group(1))

    time.sleep(3)

    scripts = driver.find_elements(By.TAG_NAME, 'script')

    data = None

    for s in scripts:

        d = s.get_attribute('innerHTML')

        if 'valuesChart' in d:
            data = d

    match = re.search(r'valuesChart\((.*)\)', data)

    json_obj = None

    if match:
        if match:
            json_str = match.group(1)
            json_obj = json.loads(json_str)

    #Sacamos el header pero una vez lo tenemos en el csv no necesitamos esta linea de codigo
    #header = ['id']

    #for j in json_obj['points']:
        #header.append(j['date'])

    #Si el nombre esta en blanco ponemos el apellido solo pero si tiene texto hacemos la mezcla de los dos para que este completo
    player_name = f'{driver.find_element(By.CLASS_NAME, "name").text.strip()} {driver.find_element(By.CLASS_NAME, "surname").text.strip()}' if driver.find_element(By.CLASS_NAME, "name").text.strip() else driver.find_element(By.CLASS_NAME, "surname").text.strip()

    body = [id, player_name]

    with open('pricesPlayers.csv', mode = 'r', newline = '', encoding = 'utf-8') as archivo_csv:
        lector_csv = csv.reader(archivo_csv)
        top_line = next(lector_csv, None)

    i = 2

    for j in json_obj['points']:

        while j['date'] != top_line[i]:
            body.append(0)
            i+= 1

        body.append(int(j['value']))
        i+= 1

    with open('pricesPlayers.csv', mode = 'a', newline = '', encoding = 'utf-8') as archivo_csv:
        escritor = csv.writer(archivo_csv)

        escritor.writerow(body)

    print(f'Done : {e}/{len(enlaces)}')

driver.quit()

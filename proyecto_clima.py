#Importacion de librerias necesarias.

import os
import time
import datetime
import json
import requests
from claves_api import * #Cambiar esta linea por un archivo claves_api.py con los datos requeridos personales de la API
from twilio.rest import Client
import pandas as pd
import tqdm

api_key =  WEATHER_API_KEY#Seteo de API Key utilizado para el clima 
#ciudad_clima = input('Ingrese la ciudad a realizar la busqueda del clima  \n') #Pedida de ciudad donde revisar el clima
ciudad_clima = 'Mexico'
query = 'http://api.weatherapi.com/v1/forecast.json?key='+api_key+'&q='+ciudad_clima+'&days=1&aqi=no&alerts=no' ##Formando Request tipo GET para obtener los datos
resultado = requests.get(query).json() #Guardamos el resultado del tipo request en formato JSON
datos = [] #Lista que guardara el reporte del clima

def get_forecast_now(peticion_json): #Funcion para encontrar el reporte del clima consultado por hora actual
    hora = datetime.datetime.now().hour #Accedemos a la hora actual de ejecutar este programa para obtener el horario.

    fecha = peticion_json['forecast']['forecastday'][0]['hour'][hora]['time'].split(' ')[0] 
    temperatura = peticion_json['forecast']['forecastday'][0]['hour'][hora]['temp_c']
    pronostico = peticion_json['forecast']['forecastday'][0]['hour'][hora]['condition']['text']
    #lluvia = True if(peticion_json['forecast']['forecastday'][0]['hour'][hora]['will_it_rain']) else False
    lluvia = peticion_json['forecast']['forecastday'][0]['hour'][hora]['will_it_rain'] 
    prob_lluvia = peticion_json['forecast']['forecastday'][0]['hour'][hora]['chance_of_rain']

    return hora,fecha,temperatura,pronostico,lluvia,prob_lluvia

def get_forecast(peticion_json,iterador): #Funcion para encontrar el reporte del clima consultado por dia
    hora = int(peticion_json['forecast']['forecastday'][0]['hour'][iterador]['time'].split(' ')[1].split(':')[0])
    fecha = peticion_json['forecast']['forecastday'][0]['hour'][iterador]['time'].split(' ')[0] 
    temperatura = peticion_json['forecast']['forecastday'][0]['hour'][iterador]['temp_c']
    pronostico = peticion_json['forecast']['forecastday'][0]['hour'][iterador]['condition']['text']
    #lluvia = True if(peticion_json['forecast']['forecastday'][0]['hour'][iterador]['will_it_rain']) else False
    lluvia = peticion_json['forecast']['forecastday'][0]['hour'][iterador]['will_it_rain'] 
    prob_lluvia = peticion_json['forecast']['forecastday'][0]['hour'][iterador]['chance_of_rain']

    return hora,fecha,temperatura,pronostico,lluvia,prob_lluvia



for i in tqdm.tqdm(range(len(resultado['forecast']['forecastday'][0]['hour']))): #Guarda los datos del clima para todo el dia usando un iterador.
    datos.append(get_forecast(resultado,i))

columnas = ['Hora','Fecha','Temperatura','Pronostico','Lluvia','Prob_lluvia'] #Seteo de columnas para nuestra data_frame

'''Construimos el data frame y lo limpiamos para solo quedarnos con la hora y el pronostico del tiempo'''

datos = pd.DataFrame(datos,columns=columnas)
lluvia_df = datos[(datos['Lluvia']) & (datos['Hora'] > 8) & (datos['Hora']<20)]
lluvia_df = lluvia_df[['Hora','Pronostico']]
lluvia_df.set_index('Hora',inplace = True)

mensaje = 'Hola, el pronostico de lluvia en '+ciudad_clima+' para el dia '+datos['Fecha'][0]+ '\n\n'+str(lluvia_df) #Construimos mensaje a enviar

numero_tel = PHONE_NUMBER
account_sid_twillio = TWILIO_ACCOUNT_SID
auth_token_twillio = TWILIO_AUTH_TOKEN

client = Client(account_sid_twillio, auth_token_twillio)
message = client.messages.create(
                    body=mensaje,
                    from_=numero_tel,
                    to='+525582992236')

print('Mensaje Enviado ' + message.sid)
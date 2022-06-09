import requests
import PySimpleGui as sg
import time
from datetime import datetime, timedelta
from dateutil import tz

#IDs y Llaves del canal prinicpal del sensor A los dispositivos  PurpleAir

#Van en orden del 1 al 30.
keys = ['TMTVNTYUXGGT7MK3', 'T5VPQSVT9BAE5ZI1',"F2K1DV64M1Z75VU4", "O94LWPUDGE645M0W","3DHCZRPJ1M6YIFV7",
        "LMP9I4DYO31RLQCM", "4YNO8GQDC5V4D8AH", "YR676V09QO1KX1Q7", "YTLP8VLPWKIJ9G4K", "ODM4VO7RDXCYWL2O",
        "0S1GMA57I3VO7TN8","IJ44H5T0VGAPOM1X", "4MGD149UTH64IKO1","D1EPGDRFWRLFDRWL", "3GOKID03X1ZQI7UO",
        "IO35IQWN7OD7QZRI", "KYOJ88GAQ573QZOG","D6NQDA4PSE9FDW9N","KR2E9MGDRAR8U4FI", "TV45OPQDRKXEOYF3",
        "WXQHTF7MVPTGUV3H", "HWHD61TYPRC08IJ0", "TEQLCBVA8W53X6MQ", "LYE31WD6M75Z3J8E", "CF8HVDROSC9N04O7",
        "BCJV79PNCBA20CEI", "ITO12LYZ84AXMSB1", "LAU5S4Y8NY6F9FNK", "9WAVRBGJHR27Q9SB", "FP815UH9YRZ77MY1"]

channel_ids =[1367948, 1367997, 1336916, 1367985, 1369647, 
              1369624, 1379154, 1368013, 1369640, 1367969,
              1379214, 1367956, 1367952, 1336974, 1368009, 
              1453911, 1452796, 1451589, 1450382, 1452792,
              1452813, 1450481, 1447356, 1452808, 1451577,
              1451621, 1452812, 1452804, 1450358, 1450485]

from_zone = tz.tzutc()

def Gui():
    # Se crea la interfaz principal del programa.
    layout = [[sg.Text('Monitoreo de los sensores PurpleAir en vivo.')],
            [sg.Text('Este programa permite realizar un monitoreo en vivo de los sensores en el campo, comprobando que estos esten transmitiendo datos continuamente al servidor')],
            [sg.Text('Indica cada cuanto tiempo se comprobara que los sensores envian datos: '), sg.Input(key='Period')],
            [sg.Text('Favor de escribir el correo que recibira las advertencias: '), sg.Input(key='Correo')],
            [sg.Button('Continue'), sg.Button('Exit')]]

    window = sg.Window('Monitoreo de los sensores', layout, size=(720,480))
    event, value = window.read()

    period = value['Period']
    email = value['Correo']

    if event == 'Exit':
        pass
    
    chain = list(range(1,len(keys)+1))
    lay = []
    layout = []

    r = 0
    c = 0
    for ii in chain:
        if ii%9 == 0:
            r += 1
            c = 0
            layout.append(lay)
            lay = []
        lay.append(sg.Input(ii,key=f'{r},{c}', size=(5,1)))
        c += 1
    if lay:
        layout.append(lay)
        lay = []

    lay = [[sg.Text('Favor de indicar los sensores a monitorizar', justification='center', expand_x=True, expand_y=True)],
            [sg.Text('Escribe el número de identificación de los sensores en los recuadros (Ejemplo: 1, 6, 23)')],
            [sg.Frame('Disposición de los sensores', layout, element_justification='center', expand_x=True)],
            [sg.Button('Continue',key='Next'),sg.Button('Return',key='sensor_info'),sg.Button('Exit')]]

    window.close()
    window = sg.Window('Monitoreo de los sensores', lay, size=(720,480))
    event, value = window.read()

    if event == 'Exit':
        pass

    lay = [sg.Text('El programa se inicializara...')]
    window.close()
    window = sg.Window('Monitoreo de los sensores', lay)
    
    time.sleep(5)
    window.close()

    lay = [[sg.Text('El programa actualmente esta funcionando.')],
            [sg.Text('Si algun sensor deja de enviar datos, se notificara con un e-mail.')],
            [sg.Text('Para finalizar el programa, solo cierra esta ventana.')]]
    window = sg.Window('Monitoreo de los sensores', lay)

    return period, email, value

def Data_extraction():
    """
        @name: Data_extraction
        @brief: Función que extrae datos de los sensores purple air
        @params: None
        @return: Datos de todos los sensores.
    """
    dates = []

    # Extrae por cada sensor, los datos de la ultima medición
    for ii in range(len(keys)):
        key = keys[ii]
        channel = channel_ids[ii]
        data = Read_sensor(channel, key)

        date = data[0]['created_at'].strip('Z').replace('T', ' ')
        date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S').replace(tzinfo=from_zone)

        if date.second >= 30:
            date = date + timedelta(seconds=60-date.second)
        else:
            date = date - timedelta(seconds=date.second)

        dates.append(date)
    
    return dates

def Read_sensor(channel_id, read_key):
    url = 'https://api.thingspeak.com/channels/{}/feeds.json?api_key='.format(channel_id)
    url = url + read_key

    data = requests.get(url).json()

    feeds = data['feeds']
    return feeds
import requests
import PySimpleGUI as sg
import time
import sys
import csv
from datetime import datetime, timedelta
from dateutil import tz

"""
Este archivo fue creado para contener las funciones que utilizara el código main.

Creado por Adrian Morales.
Fecha de finalización: 20/06/2022
"""

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

IDS_KEY = {}
for ii in range(len(keys)):
    IDS_KEY[ii+1] = (channel_ids[ii],keys[ii])

from_zone = tz.tzutc()

# Tema y fuente
sg.theme('LightGreen2')
font = ('Times New Roman', 14)

def Gui_start():
    """
        @name: Gui_start
        @brief: Crea la interfaz de arranque, solicitando datos al usuario.
        @params: 
        @return: period, email, key, key2, window
    """
    # Se crea la interfaz principal del programa.
    layout = [[sg.Text('Monitoreo de los sensores PurpleAir en vivo.\n', justification='center', font=('Times New Roman', 20), expand_x=True)],
            [sg.Text('Este programa permite realizar un monitoreo en vivo de los sensores en el campo,\ncomprobando que estos esten transmitiendo datos continuamente al servidor.', expand_x=True)],
            [sg.Text('Indica cada cuantos minutos se comprobara que los sensores envian datos (> 2 min): ',size = (64,1)), sg.Input(key='Period',expand_x=True)],
            [sg.Text('Favor de escribir el correo que recibira las advertencias: '), sg.Input(key='Correo')],
            [sg.Text('\nNota: El programa tiene registrado las llaves y ids de 30 sensores,\nsi desea trabajar con más sensores, favor de seleccionar el recuadro:')],
            [sg.Checkbox('Cargar llaves y Ids', default=False, key='Cargar')],
            [sg.Button('Continue'), sg.Button('Exit')]]

    window = sg.Window('Monitoreo de los sensores', layout, font=font, size=(720,480), grab_anywhere=True)
    event, value = window.read()

    if event in ('Exit', sg.WIN_CLOSED):
        window.close()
        sys.exit()

    try:
        period = float(value['Period'])
    except:
        layout = [[sg.Text('Favor de introducir un número en el recuadro de minutos\n', justification='center', font=('Times New Roman', 20))],
                [sg.Text('¡Se detecto un error al leer el periodo!')],
                [sg.Button('Try again'), sg.Button('Exit')]]
        window.close()
        window = sg.Window('Monitoreo de los sensores', layout, font=font, size=(720,480), grab_anywhere=True)
        event, value = window.read()
        if event in ('Exit', sg.WIN_CLOSED):
            window.close()
            sys.exit()
        window.close()
        return 0,0,0,False,window

    email = value['Correo']
    key = value['Cargar']

    if ('@' in email) and (email != ''):
        return period, email, key, True, window
    else:
        layout = [[sg.Text('Favor de introducir un correo valido.\n', justification='center', font=('Times New Roman', 20))],
                [sg.Text('¡Se detectó un error al leer el correo dado!')],
                [sg.Button('Try again'), sg.Button('Exit')]]
        window.close()
        window = sg.Window('Monitoreo de los sensores', layout, font=font, size=(720,480), grab_anywhere=True)
        event, value = window.read()
        if event in ('Exit', sg.WIN_CLOSED):
            window.close()
            sys.exit()
        window.close()
        return 0,0,0,False,window

def Cargar(window):
    """
        @name: Cargar
        @brief: Se ejecuta si el usuario desea comprobar sensores nuevos que no estan añadidos en este código.
        @params: window
        @return: Actualiza la variable global de IDs y Keys.
    """

    layout = [[sg.Text('Carga de archivo csv\n', justification='center', font=('Times New Roman', 20), expand_x=True)],
                [sg.Text('Selecciona el archivo con los Ids y llaves de los sensores a trabajar')],
                [sg.Input(), sg.FileBrowse()],
                [sg.Button('Continue'), sg.Button('Exit')]]
        
    window.close()
    window = sg.Window('Monitoreo de los sensores', layout, font=font, size=(720,480), grab_anywhere=True)
    event, value = window.read()
    if event in ('Exit', sg.WIN_CLOSED):
        window.close()
        sys.exit()

    try:
        with open(value['Browse'], mode='rt', encoding="utf8") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            global IDS_KEY
            IDS_KEY = {}
            linea = 0
            for row in csv_reader:
                if linea == 0:
                    linea = 1
                    continue
                IDS_KEY[int(row[0])] = (row[1], row[2])
        
        return False, window

    except:
        layout = [[sg.Text('Favor de cargar un archivo tipo CSV que contenga:', justification='center', font=('Times New Roman', 20))],
                [sg.Text('No, Ids, Keys como columnas.', font=('Times New Roman', 20))],
                [sg.Button('Try again'), sg.Button('Exit')]]
        window.close()
        window = sg.Window('Monitoreo de los sensores', layout, font=font, size=(720,480), grab_anywhere=True)
        event, value = window.read()
        if event in ('Exit', sg.WIN_CLOSED):
            window.close()
            sys.exit()

        return True, window

def Posicion(window):
    """
        @name: Posicion
        @brief: Función que genera una interfaz con los numeros de sensores a monitorear.
        @params: window
        @return: Sensores, window
    """
    # Se crea una matriz para desplegar los sensores que el usuario seleccionara.

    chain = list(IDS_KEY.keys())
    lay = []
    layout = []

    r = 0
    c = 0
    jj = 0
    for ii in chain:
        if jj%10 == 0:
            r += 1
            c = 0
            layout.append(lay)
            lay = []
        lay.append(sg.Input(ii,key=f'{r},{c}', size=(5,1)))
        c += 1
        jj += 1
    if lay:
        layout.append(lay)
        lay = []

    frame = [[sg.Frame('Sensores a monitorizar', layout, element_justification='center', expand_x=True)]]

    lay = [[sg.Text('Favor de indicar los sensores a monitorizar\n', justification='center', font=('Times New Roman', 20), expand_x=True)],
            [sg.Text('Escribe el número de identificación de los sensores en los recuadros (Ejemplo: 1, 6, 23).')],
            [sg.Text('En el recuadro se despliegan todos los sensores disponibles a monitorizar, si no requiere')],
            [sg.Text('verificar alguno de ellos, deje en blanco su recuadro.')],
            [sg.Column(frame, scrollable=True, expand_y=True, justification='center')],
            [sg.Button('Continue',key='Next'),sg.Button('Exit')]]

    window.close()
    window = sg.Window('Monitoreo de los sensores', lay, font=font, size=(720,480), grab_anywhere=True)
    event, value = window.read()

    if event in ('Exit', sg.WIN_CLOSED):
        window.close()
        sys.exit()

    # Extraigo los valores dados por el usuario y los quito los repetidos.
    value = list(set(list(value.values())))

    # Quito los espacios vacios.
    if '' in value:
        value.remove('')
    
    # Hago una prueba para evitar que el usuario rompa el código.
    try:
        # Los paso de string a enteros y ordeno.
        sensors = []
        for ii in value:
            sensors.append(int(ii))
        sensors.sort()

        # Compruebo que los numeros esten dentro de los numeros dados por el usuario o del 1 a 30.
        num = list(IDS_KEY.keys())
        llave = False

        for ii in sensors:
            if ii in num:
                pass

            else:
                llave = True
                # Si no se encuentra en el rango, se levanta un error y se pide ingresar de nuevo los datos.
                layout = [[sg.Text('Favor de introducir únicamente números enteros que estén')],
                [sg.Text('entre el 1 y 30, o entre los números del archivo csv cargado.')],
                [sg.Button('Try again'), sg.Button('Exit')]]
                window.close()
                window = sg.Window('Monitoreo de los sensores', layout, font=('Times New Roman', 18), size=(720,480), grab_anywhere=True)
                event, value = window.read()
                if event in ('Exit', sg.WIN_CLOSED):
                    window.close()
                    sys.exit()
                break

        if llave:
            return True, window
        else:
            return sensors, window

    except:
        layout = [[sg.Text('Favor de introducir únicamente números enteros que estén')],
                [sg.Text('entre 1 y 30, o entre los números del archivo csv cargado.')],
                [sg.Button('Try again'), sg.Button('Exit')]]
        window.close()
        window = sg.Window('Monitoreo de los sensores', layout, font=('Times New Roman', 18), size=(720,480), grab_anywhere=True)
        event, value = window.read()
        if event in ('Exit', sg.WIN_CLOSED):
            window.close()
            sys.exit()
        
        return True, window
    
def Aviso_programa(window,email):
    """
        @name: Aviso_programa
        @brief: Genera un mensaje del funcionamiento del programa.
        @params: window, email
        @return: window.
    """
    window.close()
    time.sleep(2)

    lay = [[sg.Text('El programa actualmente está funcionando.', font=('Times New Roman', 20))],
            [sg.Text('Si algun sensor deja de enviar datos, se notificara con un e-mail hacia,')],
            [sg.Text(f'{email}\n')],
            [sg.Text('Para finalizar el programa, solo cierra esta ventana.')]]
    window = sg.Window('Monitoreo de los sensores', lay, font = font, grab_anywhere=True)
    return window

def Data_extraction(value):
    """
        @name: Data_extraction
        @brief: Función que extrae datos de los sensores purple air
        @params: value: Número de sensores a extraer.
        @return: Datos de los sensores dados.
    """
    dates = []

    # Extrae por cada sensor, los datos de la ultima medición
    for ii in value:
        
        # Si falla la lectura de datos, el programa avisa sobre esto y finaliza todos los procesos
        # ya que se deben revisar cosas importantes por parte del usuario para evitar esto.
        try:
            channel = IDS_KEY[ii][0]
            key = IDS_KEY[ii][1]
            data = Read_sensor(channel, key)
        except:
            layout = [[sg.Text('¡Error fatal al intentar leer los datos de un sensor!', font=('Times New Roman',18))],
                [sg.Text(f'El error ocurrió al extraer datos del sensor {ii}.')],
                [sg.Text('Errores posibles:')],
                [sg.Text('1.- Se introdujo mal alguna Id o llave en el archivo csv.')],
                [sg.Text('2.- Mala conexión de internet.')],
                [sg.Text('3.- Problemas con el servidor de PurpleAir.')],
                [sg.Text(f'El programa finalizará después de esta ventana...')],
                [sg.Button('Exit')]]
            window = sg.Window('Monitoreo de los sensores', layout, font=font, size=(720,480), grab_anywhere=True)
            event, value = window.read()
            window.close()
            sg.popup_auto_close('Cerrando programa...', font=('Times New Roman',16))
            dates = True
            break

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
    url = url + read_key + "&results=1"

    data = requests.get(url).json()

    feeds = data['feeds']
    return feeds

def No_outlook():
    layout = [[sg.Text('No se detecta alguna cuenta valida.', justification='center', font=('Times New Roman', 20), expand_x=True)],
            [sg.Text('Favor de introducir una cuenta microsoft a la computadora para el envio de correo.')],
            [sg.Button('Exit')]]

    window = sg.Window('Monitoreo de los sensores', layout, font=font, size=(720,480), grab_anywhere=True, element_justification='c')
    event, value = window.read()

    if event in ('Exit', sg.WIN_CLOSED):
        window.close()
        sys.exit()
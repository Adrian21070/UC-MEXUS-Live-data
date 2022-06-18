import time
import email_sending as Mail
import PySimpleGUI as sg
import multiprocessing
from datetime import datetime
from live_data import *

def verificacion(period, user, value):
    # Obtengo la hora antes de entrar a la extracción de datos
    time_0 = datetime.now()
    
    # Se extrae por primera vez las mediciones
    dates_v1 = Data_extraction(value)

    # Obtengo la hora depues de salir de la extracción de datos
    time_1 = datetime.now()

    retrasos = [0 for i in range(len(dates_v1))]

    email_sensors = []

    while True:
        # Calculo lo que tardo en extraer los datos.
        delta_time = (time_1 - time_0).seconds

        # Pauso por ciertos minutos el programa
        if period*60 - delta_time < 0:
            pass

        else:
            time.sleep(period*60 - delta_time)

        # Obtengo la hora antes de entrar a la extracción de datos
        time_0 = datetime.now()

        # Se vuelve a extraer datos
        dates_v2 = Data_extraction(value)

        # Verificamos si existen nuevos datos.
        for ii in range(len(dates_v1)):
            delta = dates_v2[ii] - dates_v1[ii]

            # Verificamos que el sensor si este en el mismo dia de mediciones
            # puede que no haya inicializado y tenga un dato desde hace dias.
            if delta.days != 0:
                retrasos[ii] = period

            else:
                # Si se reportaron datos entre el tiempo de espera, el retraso es 0.
                if delta.seconds >= period/2:
                    retrasos[ii] = 0

                else:
                    # Caso contrario se aumenta el retraso, en este caso directamente se cataloga como
                    # sensor para enviar correo.

                    #retrasos[ii] = retrasos[ii] + period
                    email_sensors.append(value[ii])

                #if retrasos[ii] >= period:
                #    # Almaceno el numero del sensor que tuvo perdida de información mayor a x minutos
                #    retrasos[ii] = 0
                #    email_sensors.append(value[ii])
        
        # Se envian correos si email_sensors no esta vacio.
        if email_sensors:
            Mail.Send_email(user, email_sensors)
            sg.Popup('Se desconectaron algunos sensores!!!', keep_on_top=True)
            email_sensors = []

        # Obtengo la hora depues de salir del proceso
        time_1 = datetime.now()

def interfaz():
    # Creación de interfaz
    period, user, value, window = Gui()

    # Se corre en paralelo la comprobación del funcionamiento de los sensores.
    p2 = multiprocessing.Process(target = verificacion, args=(period,user,value))
    p2.start()

    # Bucle que confirma si el usuario desea salir de la ejecución del programa.
    while True:
        event, value = window.read()
        if event in (None, sg.WIN_CLOSED):

            # El usuario debe confirmar que si desea salir
            lay = [[sg.Text('¿Estas segur@ de salir del programa?', font=('Times New Roman',24))],
                    [sg.Button('Exit'), sg.Button('Keep running')]],
            window = sg.Window('Monitoreo de los sensores', lay, font=('Times New Roman',18), grab_anywhere=True)
            event, value = window.read()
            window.close()

            if event in ('Exit', sg.WIN_CLOSED):
                # Termina todos los procesos y cierra el programa.
                if p2.is_alive():
                    p2.terminate()
                #sys.exit()
                break

            else:
                # Se crea la ventana de "Programa en funcionamiento"
                lay = [[sg.Text('El programa actualmente esta funcionando.')],
                    [sg.Text('Si algun sensor deja de enviar datos, se notificara con un e-mail.')],
                    [sg.Text('Para finalizar el programa, solo cierra esta ventana.')]]
                window = sg.Window('Monitoreo de los sensores', lay, font = font, grab_anywhere=True)
                continue

if __name__=='__main__':
    # Se realizaran muestros cada x minutos, se esperaria tener algun dato en este periodo
    # si no se presenta algun dato nuevo, es decir una nueva fecha, se marcara como un retraso
    # de x minutos para ese sensor, esto se ira acumulando y si pasa un tiempo dado en minutos,
    # se enviara un e-mail como forma de alarma para avisar este error.
    # Si detecta un nuevo dato antes de pasar el tiempo dado en minutos, se reinicia este retraso a 0. 
    p1 = multiprocessing.Process(target = interfaz)
    p1.start()
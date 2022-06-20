import email_sending as Mail
import PySimpleGUI as sg
import multiprocessing
from datetime import datetime
from live_data import *

def verificacion(period, user, value, stop_bool):
    # Obtengo la hora antes de entrar a la extracción de datos
    time_0 = datetime.now()
    bucle = True
    
    # Se extrae por primera vez las mediciones
    dates_v1 = Data_extraction(value)
    if isinstance(dates_v1, bool):
        stop_bool.value += 1
        bucle = False

    if bucle:
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
            if isinstance(dates_v1, bool):
                stop_bool.value += 1
                break

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
                try:
                    Mail.Send_email(user, email_sensors)
                    sg.Popup('Se desconectaron algunos sensores!!!', auto_close=True, auto_close_duration=8, keep_on_top=True, font=('Times New Roman',16))
                    email_sensors = []
                except:
                    layout = [[sg.Text('¡Error fatal al intentar enviar un correo!\n', font=('Times New Roman',20), justification='center', expand_x=True)],
                        [sg.Text('Favor de introducir correctamente el correo y revisar que la conexión,')],
                        [sg.Text('a internet sea estable.')],
                        [sg.Button('Exit')]]
                    window = sg.Window('Monitoreo de los sensores', layout, font=font, grab_anywhere=True)
                    event, value = window.read()
                    sg.popup_auto_close('Cerrando programa...', font=('Times New Roman',16))
                    stop_bool.value += 1
                    break

            # Obtengo la hora depues de salir del proceso
            time_1 = datetime.now()

            # Actualizo mis fechas anteriores
            dates_v1 = dates_v2

def is_closed(window, stop_bool2, user):
    # Bucle que confirma si el usuario desea salir de la ejecución del programa.
    while True:
        event, value = window.read()
        if event in (None, sg.WIN_CLOSED):
            # El usuario debe confirmar que si desea salir
            lay = [[sg.Text('¿Estas segur@ de salir del programa?', font=('Times New Roman',24))],
                    [sg.Button('Exit'), sg.Button('Keep running')]],
            window = sg.Window('Monitoreo de los sensores', lay, font=('Times New Roman',16), grab_anywhere=True)
            event, value = window.read()

            if event in ('Exit', sg.WIN_CLOSED):
                # Termina todos los procesos y cierra el programa.
                window.close()
                stop_bool2.value += 1
                break
                #sys.exit()

            else:
                # Se crea la ventana de "Programa en funcionamiento"
                window = Aviso_programa(window,user)
                #lay = [[sg.Text('El programa actualmente esta funcionando.')],
                #    [sg.Text('Si algun sensor deja de enviar datos, se notificara con un e-mail.')],
                #    [sg.Text('Para finalizar el programa, solo cierra esta ventana.')]]
                #window = sg.Window('Monitoreo de los sensores', lay, font = font, grab_anywhere=True)
                continue

if __name__=='__main__':

    # Se realizaran muestros cada x minutos, se esperaria tener algun dato en este periodo
    # si no se presenta algun dato nuevo, es decir una nueva fecha, se marcara como un retraso
    # de x minutos para ese sensor, esto se ira acumulando y si pasa un tiempo dado en minutos,
    # se enviara un e-mail como forma de alarma para avisar este error.
    # Si detecta un nuevo dato antes de pasar el tiempo dado en minutos, se reinicia este retraso a 0.

    # Creación de interfaz
    while True:
        period, user, key, key2, window = Gui_start()
        if key2:
            break

    if key == True:
        while key:
            key, window = Cargar(window)

    del key, key2

    while True:
        value, window = Posicion(window)
        if not isinstance(value, bool):
            break

    window = Aviso_programa(window, user)

    # Se envia un correo de prueba para verificar la conexión con el usuario.
    try:
        Mail.email_test(user)
        sg.popup('Se envió un correo de prueba,\nverifica si la conexión fue satisfactoria.', auto_close=True, auto_close_duration=5, font=('Times New Roman',16))
    except:
        layout = [[sg.Text('¡Error fatal al intentar enviar un correo!\n', font=('Times New Roman',20), justification='center', expand_x=True)],
                        [sg.Text('Favor de introducir correctamente el correo y revisar que la conexión,')],
                        [sg.Text('a internet sea estable.')],
                        [sg.Button('Exit')]]
        window = sg.Window('Monitoreo de los sensores', layout, font=font, grab_anywhere=True)
        event, value = window.read()
        sg.popup_auto_close('Cerrando programa...')
        sys.exit()

    # Se corre en paralelo la comprobación del funcionamiento de los sensores.
    stop_bool = multiprocessing.Value('i',0)
    stop_bool2 = multiprocessing.Value('i',0)

    p1 = multiprocessing.Process(target = verificacion, args=(period,user,value,stop_bool))
    p1.start()
    
    p2 = multiprocessing.Process(target = is_closed, args=(window, stop_bool2, user))
    p2.start()
    
    while True:
        p2.join(1)
        p1.join(5)
        #print(stop_bool)
        #print(stop_bool2)
        if stop_bool.value > 0:
            if p2.is_alive():
                p2.terminate()
            break
        
        if stop_bool2.value > 0:
            if p1.is_alive():
                p1.terminate()
            break
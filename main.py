import time
from datetime import datetime
from live_data import *
import email as Mail

if __name__=='__main__':
    # Se realizaran muestros cada 5 minutos, se esperaria tener algun dato en este periodo
    # si no se presenta algun dato nuevo, es decir una nueva fecha, se marcara como un retraso
    # de 5 minutos para ese sensor, esto se ira acumulando y si pasa los 15 minutos, se enviara
    # un email como forma de alarma para avisar este error.
    # Si detecta un nuevo dato antes de pasar los 15 minutos, se reinicia este retraso a 0. 

    # Creación de interfaz
    period, user, value = Gui()

    # Obtengo la hora antes de entrar a la extracción de datos
    time_0 = datetime.now()
    
    # Se extrae por primera vez las mediciones
    dates_v1 = Data_extraction()

    # Obtengo la hora depues de salir de la extracción de datos
    time_1 = datetime.now()

    retrasos = [0 for i in range(len(dates_v1))]

    email_sensors = []

    while True:
        # Calculo lo que tardo en extraer los datos.
        delta_time = (time_1 - time_0).seconds

        # Pauso por 5 minutos el programa
        time.sleep(300-delta_time)

        # Obtengo la hora antes de entrar a la extracción de datos
        time_0 = datetime.now()

        # Se vuelve a extraer datos
        dates_v2 = Data_extraction()

        # Verificamos si existen nuevos datos.
        for ii in range(len(dates_v1)):
            delta = dates_v2[ii] - dates_v1[ii]

            # Verificamos que el sensor si este en el mismo dia de mediciones
            # puede que no haya inicializado y tenga un dato desde hace dias.
            if delta.days != 0:
                retrasos[ii] = 15

            else:
                if delta.seconds >= 60:
                    retrasos[ii] = 0
                else:
                    retrasos[ii] = retrasos[ii] + 5

                if retrasos[ii] >= 15:
                    # Almaceno el numero del sensor que tuvo perdida de información mayor a 15 minutos
                    email_sensors.append(ii+1)

                # De sobra?
                elif retrasos[ii] == 0:
                    if ii+1 in email_sensors:
                        email_sensors.remove(ii+1)
                        
                # Reiniciar email_sensors
        
        # Se envian correos si email_sensors no esta vacio.
        if email_sensors:
            Mail.Email(user, email_sensors)

        
        # Obtengo la hora depues de salir del proceso
        time_1 = datetime.now()
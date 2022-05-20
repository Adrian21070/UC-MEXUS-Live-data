import time
from live_data import *

if __name__=='__main__':
    # Se realizaran muestros cada 5 minutos, se esperaria tener algun dato en este periodo
    # si no se presenta algun dato nuevo, es decir una nueva fecha, se marcara como un retraso
    # de 5 minutos para ese sensor, esto se ira acumulando y si pasa los 15 minutos, se enviara
    # un email como forma de alarma para avisar este error.
    # Si detecta un nuevo dato antes de pasar los 15 minutos, se reinicia este retraso a 0. 
    
    # Se extrae por primera vez las mediciones
    dates_v1 = Data_extraction()

    retrasos = [0 for i in range(len(dates_v1))]

    email_sensors = []

    while True:
        # Pauso por 5 minutos el programa
        time.sleep(300)

        # Se vuelve a extraer datos
        dates_v2 = Data_extraction()
        
        # Verificamos si existen nuevos datos.
        for ii in range(len(dates_v1)):
            delta = dates_v2[ii] - dates_v1[ii]
            if delta >= 60:
                retrasos[ii] = 0
            else:
                retrasos[ii] = retrasos[ii] + 5

            if retrasos[ii] >= 15:
                # Almaceno el numero del sensor que tuvo perdida de información mayor a 15 minutos
                email_sensors.append(ii+1)
            elif retrasos[ii] == 0:
                if ii+1 in email_sensors:
                    pass
            # Reiniciar email_sensors
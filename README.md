# Live-data-extraction-UC-MEXUS
## Contenido
1. Introducción
2. Scripts y archivos
3. Funcionamiento
4. Advertencias

## Introducción
Este repositorio contiene tres scripts que en conjunto crean un sistema de monitoreo por medio de una interfaz gráfica simple, de unos sensores PurpleAir conectados a la red que recolectan datos de material particulado en su zona de instalación.

## Scripts y archivos
De forma general los archivos tienen las siguientes funciones:
- **main.py:** Script encargado de llevar el orden secuencial del programa.
- **functions.py:** Script que contiene las funciones utilizadas por main.py, principalmente funciones de interfaz gráfica.
- **email_sending_outlook.py:** Es el encargado de llamar a outlook para escribir y enviar correos con notificaciones de sensores desconectados.
- **Ids_llaves_monitoreo.csv:** Archivo csv que contiene los Ids y llaves primarias del canal A de los sensores PurpleAir, se puede ajustar y mandar a llamar para agregar más sensores distintos a los ya preestablecidos.

Nota: Scripts probados con Python 3.9 en Windows 10.

## Funcionamiento
El programa se inicializa desde **main**, este script manda a llamar una función para crear la interfaz gráfica de arranque, la cual solicita el correo que recibira alertas y el periodo de monitoreo, si se introduce un 10, cada diez minutos se comprobaran los sensores.
Tambien se pregunta si desea trabajar con otros sensores, si es así, se solicita un archivo csv con la plantilla dada en el archivo de **Ids_llaves_monitoreo**, en el cual se debe escribir las llaves y el número del sensor segun se requiera.

**main** genera un proceso asíncrono, el proceso 1 se encarga de mantener la interfaz y ser reactiva al usuario, dando la opción de finalizar el programa en el momento que se desee. El proceso 2, la mayoria del tiempo esta en espera, ya que unicamente se activa cuando pasa el tiempo dado por el usuario al inicio del programa, una vez se activa, descarga datos del servidor de PurpleAir, comprueba que sean datos nuevos para cada uno de los sensores, y si detecta una anomalía en ciertos sensores, anota sus números y se encarga de enviar un correo de aviso de desconexión de tales sensores. Si ninguno presenta anomalías, entra en estado de espera por los siguientes X minutos que ingreso el usuario.

## Advertencias
El código funciona gracias a la libreria de PySimpleGUI, fue probado en el sistema operativo Windows 10, y es necesario tener **Outlook** instalado en el dispositivo e ingresar un correo, ya que el código funciona en base a esta aplicación.

Tambien es necesario instalar las librerias requeridas, las cuales estan en el archivo **requirements_monitor.txt**, para esto se incluyo una guia de instalación en el archivo **Instrucciones_instalacion.txt**.
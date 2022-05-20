import requests
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
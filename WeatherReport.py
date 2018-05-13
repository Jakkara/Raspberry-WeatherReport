import os  
import time     #ajastin

os.system('modprobe w1-gpio')       #aktivoidaan gpio
os.system('modprobe w1-therm')      #ajurit

sensor_output_path = '/sys/bus/w1/devices/28-0417618cabff/w1_slave'

def read_file_data():
    file_reader = open(sensor_output_path,'r')  #skannaa tiedostoa lukeva olio
    lines = file_reader.readlines()     #lue tiedosto
    file_reader.close()     #sulje lukija
    return lines

def parse_temperature():
    lines = read_file_data()    #kutsutaan metodista tiedot
    while lines[0].strip()[-3:] != 'YES': # sensorin tiedosto ilmoittaa YES kun mittaus onnistuu
        time.sleep(0.2)     #jos mittaus ei onnistu, nuku ja yritn
        lines = read_file_data()
    temperature = lines[1].find('t=') #luetaann
    if temperature != -1:
        temperature_numbers = lines[1].strip()[temperature+2:]
        celsius = float(temperature_numbers) / 1000.0
        return celsius

while True:
    print(parse_temperature())
    time.sleep(1)

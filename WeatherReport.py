import os  
import time

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

import subprocess

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

### DISPLAY CONF ###

RST = None    #no reset connection on the display
disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)
disp.begin()
disp.clear()
disp.display()

width = disp.width      #display properties
height = disp.height

image = Image.new('1', (width, height))	#1-bit color,  size parameters according to screen according to screen
draw = ImageDraw.Draw(image)

draw.rectangle((0,0,width,height), outline=0, fill=0) #clear the image

padding = -2	#constants for easier manipulation
top = padding
bottom = height-padding
x = 0

font = ImageFont.load_default()
draw.text((x, top), "MARMOTA MARMOTA", font=font, fill=255)
disp.image(image)
disp.display()
time.sleep(.1)

### TEMPERATURE CONF ###

os.system('modprobe w1-gpio')		#activate gpio for temperature
os.system('modprobe w1-therm')      #library for temp readings
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

        write_text_to_display(celsius)

def write_text_to_display(text):
    draw.text((x, top), text, font=font, fill=255)
    disp.image(image)
    disp.display()
    time.sleep(.1)

while True:
	print(parse_temperature())
	time.sleep(1)

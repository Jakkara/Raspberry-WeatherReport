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

padding = 3	#constants for easier manipulation
top = padding
bottom = height-padding
x = 25

# font = ImageFont.load_default()

dir_path = os.path.dirname(os.path.realpath(__file__))
font = ImageFont.truetype(font = dir_path + "/VCR.ttf", size = 32)
#draw.text((x, top), "MARMOTA MARMOTA", font=font, fill=255)
#disp.image(image)
#disp.display()
#time.sleep(.1)

### TEMPERATURE CONF ###

os.system('modprobe w1-gpio')		#activate gpio for temperature
os.system('modprobe w1-therm')      #library for temp readings
sensor_output_path = '/sys/bus/w1/devices/28-0417618cabff/w1_slave'

def read_file_data():
	file_reader = open(sensor_output_path,'r')  # scan the temperature reading file
	lines = file_reader.readlines()     # read the result
	file_reader.close()     # close the reader
	return lines

def parse_temperature():
	lines = read_file_data()    # call the method for parsing
	while lines[0].strip()[-3:] != 'YES': # the sensor will show a 'YES' on succesful reading
		time.sleep(2)         # sleep on failure, try again later
		lines = read_file_data()
	temperature = lines[1].find('t=') # read the temp
	if temperature != -1:
		temperature_numbers = lines[1].strip()[temperature+2:]
		celsius = float(temperature_numbers) / 1000.0
		return celsius

def write_text_to_display(temperature):
	index_of_comma = temperature.find('.') #remove unnecessary decimals
	if index_of_comma != -1:
		temperature = temperature[0:index_of_comma+2]

	draw.rectangle((0,0,width,height), outline=0, fill=0) # clear the screen with a black rectangle
	draw.text((x, top), temperature, font=font, fill=255)   # write temp
	disp.image(image)
	disp.display()
	time.sleep(1)

while True:
	write_text_to_display(str(parse_temperature()))
	time.sleep(10)

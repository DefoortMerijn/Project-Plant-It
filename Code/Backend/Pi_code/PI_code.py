import serial
from RPi import GPIO
import time
import datetime
import LCD_shift
import LCD
import threading
import spidev
from Mcp import Mcp3008
import socketio
import calendar
import requests
url = 'http://127.0.0.1:5000/api/v1/DeviceLog'
sio = socketio.Client()

sio.connect('http://localhost:5000')
endpoint = '/api/v1'
obj = Mcp3008()
sensor_file_name = '/sys/bus/w1/devices/28-062018477183/w1_slave'
sensor_file = open(sensor_file_name, 'r')
obj_lcd = LCD_shift.Lcd_shift()


lampen = 23
water = 24
btn_temp = 13
btn_moist = 19
btn_li = 26
# ledtest = 24

screen = 1


# Code voor Hardware
def setup():
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(lampen, GPIO.OUT, initial=GPIO.HIGH)
    GPIO.setup(water, GPIO.OUT, initial=GPIO.HIGH)

    GPIO.setup(btn_temp,
               GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(btn_moist,
               GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(btn_li,
               GPIO.IN, pull_up_down=GPIO.PUD_UP)

    GPIO.add_event_detect(
        btn_temp, GPIO.FALLING, callback=btn_temp_callback, bouncetime=200)

    GPIO.add_event_detect(
        btn_moist, GPIO.FALLING, callback=btn_moist_callback, bouncetime=200)

    GPIO.add_event_detect(
        btn_li, GPIO.FALLING, callback=btn_li_callback, bouncetime=200)


def btn_temp_callback(pin):
    print("one")
    global screen
    screen = 1


def btn_moist_callback(pin):
    print("two")
    global screen
    screen = 2


def btn_li_callback(pin):
    print("three")
    global screen
    screen = 3


def lcd_screen():
    global screen
    # while True:

    if screen == 1:

        sensor_file = open(sensor_file_name, 'r')
        for line in sensor_file:
            temp = line[line.find("t=")+2:]
        degrees = round(int(temp)/1000, 1)
        obj_lcd.send_instructions(0x01)
        obj_lcd.write_message("Value Temp. : ")
        obj_lcd.send_instructions(0x80 | 0x40)
        obj_lcd.write_message(str(degrees))
        time.sleep(1)

    if screen == 2:
        wet = 378
        dry = 908
        Moisture = obj.read_channel(1)
        percentageHum = round(((Moisture - dry)/(wet - dry))*100)
        obj_lcd.send_instructions(0x01)
        obj_lcd.write_message("Value Moisture : ")
        obj_lcd.send_instructions(0x80 | 0x40)
        obj_lcd.write_message(str(percentageHum) + "%")
        time.sleep(1)

    if screen == 3:
        obj_lcd.send_instructions(0x01)
        obj_lcd.write_message("Value LDR : ")
        obj_lcd.send_instructions(0x80 | 0x40)
        ldr = round(obj.read_channel(0)/1023*100)
        obj_lcd.write_message(str(ldr) + "%")
        time.sleep(1)

        # time.sleep(0.0001)


def init_LCD():
    obj_lcd.send_instructions(0x38)
    obj_lcd.send_instructions(0x0F)
    obj_lcd.send_instructions(0x01)


def lees_light_graph():
    while True:
        LDR = round(obj.read_channel(0)/1023*100)
        print("Licht intensiteit: " + str(LDR) + " %")
        requests.post(url, data={'Sensor': 1, 'Value': LDR,  'Plant': 1})
        time.sleep(10)


def lampen_aan():
    while True:
        LDR = round(obj.read_channel(0)/1023*100)

        if LDR <= 11:
            GPIO.output(lampen, GPIO.LOW)
        else:
            GPIO.output(lampen, GPIO.HIGH)
        time.sleep(0.1)


@sio.event
def connect():
    print('connection established')


def add_water(data):

    while True:
        wet = 378
        dry = 908
        Moisture = obj.read_channel(1)
        moisture = round(((Moisture - dry)/(wet - dry))*100)
        if moisture >= data['Moisture']:
            print("teveel/genoeg water")

            GPIO.output(water, GPIO.HIGH)
            break
        if moisture < data['Moisture']:
            print("er wordt water toegevoegd")

            GPIO.output(water, GPIO.LOW)
        sio.sleep(0.0000001)


def lees_minuut_sensor_graph():
    while True:
        wet = 378
        dry = 908
        Moisture = obj.read_channel(1)
        percentageHum = round(((Moisture - dry)/(wet - dry))*100)
        print(percentageHum)
        print("Moisture Level: " + str(percentageHum) + " %")
        sensor_file = open(sensor_file_name, 'r')
        for line in sensor_file:
            temp = line[line.find("t=")+2:]
        degrees = round(int(temp)/1000, 1)
        print("Temperatuur: " + str(degrees) + " graden celcius")
        requests.post(url, data={'Sensor': 3, 'Value': degrees,  'Plant': 1})
        requests.post(
            url, data={'Sensor': 2, 'Value': percentageHum,  'Plant': 1})
        time.sleep(60)


def timer():
    while True:
        moisture = requests.get(
            'http://192.168.168.168:5000/api/v1/TimerMoisture')
        TimerMoisture = moisture.json()
        timer = requests.get('http://192.168.168.168:5000/api/v1/Timer')
        TimerData = timer.json()
        timerDay = TimerData['DayOfTheWeek']
        timerTime = TimerData['Time']
        timerMoisture = TimerMoisture['Moisture']
        print(timerMoisture)
        print(timerDay)
        print(timerTime)
        weekday = datetime.datetime.today().weekday()
        today = calendar.day_name[weekday]
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        print(current_time)
        print(today)
        if timerDay == today and timerTime == current_time:
            add_water(TimerMoisture)

        else:
            print("not time")
            GPIO.output(water, GPIO.HIGH)
        time.sleep(0.00001)


@sio.on('B2A_send_water')
def send_water(data):
    sio.start_background_task(add_water, data)


try:
    setup()

    init_LCD()
    sio.start_background_task(connect)

    threading.Thread(target=lampen_aan, daemon=True).start()
    # threading.Thread(target=lcd_screen, daemon=True).start()
    threading.Thread(target=lees_light_graph, daemon=True).start()
    threading.Thread(target=lees_minuut_sensor_graph, daemon=True).start()
    threading.Thread(target=timer, daemon=True).start()
    while True:
        lcd_screen()
        # print("Now this is pod racing")
        # time.sleep(100)


except KeyboardInterrupt as e:
    pass

finally:
    print('script stopt')
    GPIO.cleanup()
    obj.closespi()

from RPi import GPIO
import time
D0 = 16
D1 = 12
D2 = 25
D3 = 24
D4 = 23
D5 = 26
D6 = 19
D7 = 13

RS = 21
E = 20


class Lcd(object):
    def __init__(self, E_pin=E, RS_pin=RS, datapins=[16, 12, 25, 24, 23, 26, 19, 13]):
        self._rs_pin = RS_pin
        self._e_pin = E_pin
        self._datapins = datapins
        GPIO.setmode(GPIO.BCM)
        GPIO.setup((self._rs_pin, self._e_pin), GPIO.OUT, initial=GPIO.HIGH)

    def set_data_bits(self, value):
        mask = 0x01
        for i in range(0, 8):
            byte = value >> i
            GPIO.output(self.datapins[i], mask & byte)

    def send_instructions(self, value):
        GPIO.output(self._rs_pin, GPIO.LOW)
        self.set_data_bits(value)
        GPIO.output(self._e_pin, GPIO.LOW)
        time.sleep(0.01)
        GPIO.output(self._e_pin, GPIO.HIGH)

    def send_character(self, value):
        GPIO.output(self._rs_pin, GPIO.HIGH)
        self.set_data_bits(value)
        GPIO.output(self._e_pin, GPIO.LOW)
        time.sleep(0.001)
        GPIO.output(self._e_pin, GPIO.HIGH)

    def write_message(self, message):
        for byte in bytearray(message, encoding='utf8'):
            self.send_character(byte)

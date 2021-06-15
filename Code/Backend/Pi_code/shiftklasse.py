import time
from RPi import GPIO

# default pin numbers (BCM) - pas aan indien nodig
DS = 17  # serial data
OE = 27  # output enable (active low)
STCP = 22  # storage register clock pulse
SHCP = 5  # shift register clock pulse
MR = 6  # master reset (active low)


delay = 0.0000001


class ShiftKlasse:
    def __init__(self, ds_pin=DS, shcp_pin=SHCP, stcp_pin=STCP, mr_pin=MR, oe_pin=OE):

        self.ds_pin = ds_pin
        self.shcp_pin = shcp_pin
        self.stcp_pin = stcp_pin
        self.mr_pin = mr_pin
        self.oe_pin = oe_pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup([ds_pin, oe_pin, shcp_pin, stcp_pin, mr_pin],
                   GPIO.OUT, initial=GPIO.LOW)
        # volgende kan ook
        # for pin in ds_pin, oe_pin, shcp_pin, stcp_pin, mr_pin:
        #     GPIO.setup(pin, GPIO.OUT)
        #     GPIO.output(pin, GPIO.LOW)
        GPIO.output(self.mr_pin, GPIO.HIGH)

    def write_bit(self, value):

        # vul hier zelf aan, gebruik self.ds_pin en self.shcp_pin als pin variabelen
        GPIO.output(self.ds_pin, value)
        time.sleep(delay)
        GPIO.output(self.shcp_pin, GPIO.HIGH)
        time.sleep(delay)
        GPIO.output(self.shcp_pin, GPIO.LOW)
        time.sleep(delay)

    def copy_to_storage_register(self):

        # vul hier zelf aan, gebruik self.ds_pin en self.shcp_pin als pin variabelen
        GPIO.output(self.stcp_pin, GPIO.HIGH)
        time.sleep(delay)
        GPIO.output(self.stcp_pin, GPIO.LOW)
        time.sleep(delay)

    def write_byte(self, value):
        # vul hier zelf aan: code om een byte uit te splitsen in bits...
        mask = 0x80
        while mask:
            if value & mask == 0:
                self.write_bit(0)
            else:
                self.write_bit(1)
            mask >>= 1

    @property
    def output_enabled(self):
        return not GPIO.input(self.oe_pin)

    @output_enabled.setter
    def output_enabled(self, value):
        GPIO.output(self.oe_pin, not value)

    def reset_shift_register(self):

        GPIO.output(self.mr_pin, GPIO.LOW)
        time.sleep(delay)
        GPIO.output(self.mr_pin, GPIO.HIGH)
        time.sleep(delay)

    def reset_storage_register(self):

        self.reset_shift_register()
        self.copy_to_storage_register()

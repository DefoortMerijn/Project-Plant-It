import time
from RPi import GPIO
import spidev


class Mcp3008:
    def __init__(self, bus=0, device=0):

        self._bus = bus
        self._device = device
        self._spi = spidev.SpiDev()
        GPIO.setmode(GPIO.BCM)
        self._spi.open(self._bus, self._device)
        self._spi.max_speed_hz = 10 ** 5

    def read_channel(self, kanaal):

        uitgaande_bytes = [1, (0x80 | (kanaal << 4)), 0]
        potensio = self._spi.xfer(uitgaande_bytes)
        combinatie = ((potensio[1] << 8) | potensio[2])
        return combinatie

    def closespi(self):
        self._spi.close()

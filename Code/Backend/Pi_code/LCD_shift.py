from LCD import Lcd
from shiftklasse import ShiftKlasse

RS = 21
E = 20


class Lcd_shift(Lcd):
    def __init__(self, E_pin=E, RS_pin=RS, datapins=[16, 12, 25, 24, 23, 26, 19, 13]):
        super(Lcd_shift, self).__init__(E_pin, RS_pin, datapins)
        self._shiftregister = ShiftKlasse()

    def set_data_bits(self, value):
        self._shiftregister.write_byte(value)
        self._shiftregister.copy_to_storage_register()
        self._shiftregister.output_enabled = True

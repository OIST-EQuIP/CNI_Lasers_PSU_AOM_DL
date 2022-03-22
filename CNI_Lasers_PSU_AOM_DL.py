import pyvisa as visa
import time


class PSU_AOM_DL:
    def __init__(self, rm, port, trig_external=True, freq=100, current=0):
        self._port = rm.open_resource(port)
        self._repetition_frequency = freq
        self._current = current
        self._external_trigger = trig_external

        self._last_command = time.time()

    def close(self):
        self._port.close()

    @property
    def current(self):
        return self._current

    @current.setter
    def current(self, curr):
        self._current = curr
        prefix = b'\x55\xaa\x05\x00'
        bit1 = curr >> 8
        bit2 = curr - (bit1 << 8)
        sum = (bit1 + bit2 + 0x05)%256
        hex_command = prefix + bytes([bit1]) + bytes([bit2]) + bytes([sum])
        if curr.isnumeric() and -1 < int(curr) <= 10400:
            self._write(hex_command)
        else:
            raise Exception('Invalid repetition frequency. Must be between integer between 1 and 10 400(mA).')

    @property
    def repetition_frequency(self):
        return self._repetition_frequency

    @repetition_frequency.setter
    def repetition_frequency(self, freq):
        self._repetition_frequency = freq
        prefix = b'\x55\xaa\x06\x00'
        bit1 = freq >> 16
        bit2 = (freq - (bit1 << 16)) >> 8
        bit3 = freq - (bit1 << 16) - (bit2 << 8)
        sum = bit1 + bit2 + bit3 + 0x06
        hex_command = prefix + bytes([bit1]) + bytes([bit2]) + bytes([bit3]) + bytes([sum])

        if freq.isnumeric() and -1 < int(freq) <= 20e3:
            self._write(hex_command)
        else:
            raise Exception('Invalid repetition frequency. Must be between integer between 1 and 20 000(Hz).')

    @property
    def external_trigger(self):
        return self._external_trigger

    @external_trigger.setter
    def external_trigger(self, external):
        self._external_trigger = external
        if external == False:
            self._write(b'\x55\xaa\x05\x02\x00\x00\x07')
        if external == True:
            self._write(b'\x55\xaa\x05\x02\x00\x01\x08')
    ################
    # convert to Hex and send through pyvisa commands
    ################
    def _write(self, command):
        # The laser controller needs 0.15 seconds between commands
        while time.time()-self._last_command < 0.2:
            time.sleep(0.01)
        self._port.write_raw(command)
        self._last_command = time.time()


if __name__ == '__main__':
    rm = visa.ResourceManager('@py')
    port = rm.list_resources()[0]
    laser = PSU_AOM_DL(rm, port)
    laser.current = 1000  # set current in mA
    print(laser.current)
    laser.repetition_frequency = 1000  # set repitition frequency in Hz
    print(laser.repetition_frequency)
    laser.external_trigger = False  # Trigger using internal oscillator
    print(laser.external_trigger)
    laser._port.close()

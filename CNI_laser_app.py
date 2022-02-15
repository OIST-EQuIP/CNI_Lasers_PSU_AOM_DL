from CNI_Lasers_PSU_AOM_DL import PSU_AOM_DL as lc

import sys
import pyvisa as visa

from PyQt6 import QtWidgets as qtw
from PyQt6 import uic

UI_laser, baseClass = uic.loadUiType('UI/CNI_laser_widget.ui')


class LaserController(baseClass, UI_laser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rm = visa.ResourceManager("@py")

        self.setupUi(self)
        self.refresh_com_ports()

        # click and enter functionality
        self.connect_button.clicked.connect(self.connect)
        self.disconnect_button.clicked.connect(self.disconnect)
        self.refresh_button.clicked.connect(self.refresh_com_ports)
        self.current_input.returnPressed.connect(self.set_current_button.click)
        self.set_current_button.clicked.connect(self.set_current)
        self.repetition_freq_input.returnPressed.connect(self.set_frequency_button.click)
        self.set_frequency_button.clicked.connect(self.set_repetition_frequency)
        self.set_trigger_button.clicked.connect(self.set_trigger)
        self.set_all_button.clicked.connect(self.set_all)

        # Gray out button when not connected
        self.disconnect_button.setEnabled(False)
        self.set_current_button.setEnabled(False)
        self.set_frequency_button.setEnabled(False)
        self.set_trigger_button.setEnabled(False)
        self.set_all_button.setEnabled(False)

        self.show()

    def connect(self):
        port = self.com_port_box.currentText()
        if port != "":
            self.laser_controller = lc(self.rm, port)
            self.connect_button.setEnabled(False)
            self.disconnect_button.setEnabled(True)
            self.refresh_button.setEnabled(False)
            self.set_current_button.setEnabled(True)
            self.set_frequency_button.setEnabled(True)
            self.set_trigger_button.setEnabled(True)
            self.set_all_button.setEnabled(True)
        else:
            print('No resource available')

    def disconnect(self):
        self.laser_controller.__del__()
        self.connect_button.setEnabled(True)
        self.disconnect_button.setEnabled(False)
        self.refresh_button.setEnabled(True)
        self.set_current_button.setEnabled(False)
        self.set_frequency_button.setEnabled(False)
        self.set_trigger_button.setEnabled(False)
        self.set_all_button.setEnabled(False)

    def refresh_com_ports(self):
        ports = self.rm.list_resources()
        self.com_port_box.clear()
        self.com_port_box.addItems(ports)

    def set_current(self):
        curr_lim = 10400
        curr = self.current_input.text()
        if curr.isnumeric() and 0 <= int(curr) < curr_lim:
            self.laser_controller.current = int(curr)
        else:
            print("Invalid user entry. Enter an integer between 0 and {}".format(curr_lim))

    def set_repetition_frequency(self):
        freq_lim = 20000
        freq = self.repetition_freq_input.text()
        if freq.isnumeric() and 0 <= int(freq) < freq_lim:
            self.laser_controller.repetition_frequency = int(freq)
        else:
            print("Invalid user entry. Enter an integer between 1 and {}".format(freq_lim))

    def set_trigger(self):
        if self.trigger_box.currentText() == "Internal":
            external = False
            self.set_frequency_button.setEnabled(True) # allow frequency button
        else:
            external = True
            self.set_frequency_button.setEnabled(False)
        self.laser_controller.external_trigger = external

    def set_all(self):
        self.set_current()
        self.set_repetition_frequency()
        self.set_trigger()


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    mw = LaserController()
    sys.exit(app.exec())

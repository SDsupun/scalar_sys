import serial
import glob
import termios


class ReadScalar:

    def __init__(self):
        self.weight = 'no device'
        self.boudrate = 9600
        try:
            self.scalar = serial.Serial(glob.glob('/dev/ttyUSB*')[0], baudrate=self.boudrate, timeout=1)
            self.weight = 'device detected'
            return

        except IndexError:
            self.weight = 'no device'
            return

        except serial.serialutil.SerialException:
            self.weight = 'no device'
            return

    def set_scalar(self):
        self.weight = 'no device'
        try:
            self.scalar = serial.Serial(glob.glob('/dev/ttyUSB*')[0], baudrate=self.boudrate, timeout=1)
            self.weight = 'device detected'
            return

        except IndexError:
            self.weight = 'no device'
            return

        except serial.serialutil.SerialException:
            self.weight = 'no device'
            return

    def get_weight(self):
        try:
            self.scalar.reset_input_buffer()
            self.weight = self.scalar.readline().decode('ascii')
        except serial.SerialException:
            self.weight = 'no device'
        except AttributeError:
            self.weight = 'no device'
        except termios.error:
            self.weight = 'no device'
        return self.weight

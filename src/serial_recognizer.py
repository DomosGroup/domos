import serial
import peripherals


class UnknownPeripheralError(Exception):
    def __init__(self, model_code):
        super().__init__("cannot find peripheral named '{}'".format(model_code))


def recognize_serial(ser):
    ser.write(b"info\n")
    char = None
    read = b""
    while char != b'\n':
        char = ser.read(1)
        if char not in (b'?', b'#', b'\n', b'\x00'):
            read += char
        if char == b'\n':
            print(read)
            if read == b'start':
                ser.write(b"info\n")
            if not read.startswith(b'info'):
                read = b''
                char = b''
    _, model_code, firmware_version = tuple(read.split(b' '))  # first is "info"
    model_code = model_code.decode('utf-8')
    firmware_version = int(firmware_version)
    print(firmware_version, type(firmware_version))
    try:
        exec("from peripherals import {} as per".format(model_code), locals(), globals())
        return getattr(per, model_code)(ser, firmware_version)
    except ImportError:
        raise UnknownPeripheralError(model_code)


def shish():
    ser = serial.Serial('COM3', 9600)
    return recognize_serial(ser)

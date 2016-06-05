#    Copyright (C) 2016  Domos Group
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.


import serial
import serial.tools.list_ports
import threading

import time

DEFAULT_BAUDRATE = 9600
# DEFAULT_PORTS = [
#     'ttyACM0',
#     'ttyACM1',
#     'ttyACM2',
#     'ttyAMA0',
#     'ttyS0',
#     'serial1',
#     'ptmx',
#     'tty',
#     'tty1',
# ]

def get_ports():
    return [x[0] for x in serial.tools.list_ports.comports()]


DEFAULT_PORTS = get_ports()


def loop_start_listening():
    threads, serials, stop_event = start_listening()

    def listen_loop(threads, serials, stop_event):
        old_available_ports = get_ports()
        while not stop_event.is_set():
            if old_available_ports != get_ports():
                new_threads, new_serials, _ = start_listening(stop_event)
                for new_thread in new_threads:
                    if new_thread not in threads:
                        threads.append(new_thread)
                for new_serial in new_serials:
                    if new_serial not in serials:
                        serials.append(new_serial)
                old_available_ports = get_ports()

    thread = threading.Thread(target=listen_loop, args=(threads, serials, stop_event),
                              name='Main listening thread')
    thread.start()
    threads.append(thread)
    return threads, serials, stop_event


def start_listening(stop_event=None):
    if stop_event is None:
        stop_event = threading.Event()
    threads = []
    ports = []
    serials = []
    for port in get_ports():
        thread = threading.Thread(target=listen_port, args=(port, stop_event, serials),
                                  name='Thread listening on port {}'.format(port))
        thread.start()
        threads.append(thread)
        ports.append(port)
    return threads, serials, stop_event


def listen_port(port, stop_event, serials, baudrate=DEFAULT_BAUDRATE):
    while not stop_event.is_set():
        try:
            ser = serial.Serial(port, baudrate)
        except serial.SerialException as exc:
            continue
        serials.append(ser)
        print("Found somebody at {}".format(port))
        return ser



def test():
    print("--- TESTING MODULE 'ports_listener.py'")
    threads, serials, stop_event = start_listening()
    _threads, _serials, _stop_event = None, None, None
    while True:
        if _threads != threads or _serials != serials or _stop_event != stop_event:
            print(threads, serials, stop_event)
        _threads, _serials, _stop_event = threads.copy(), serials.copy(), stop_event
        if len(serials) > 0:
            stop_event.set()
            break


if __name__ == '__main__':
    test()

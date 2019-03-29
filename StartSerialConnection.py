import torch
from time import sleep
import serial
import sys
import os
import serial.tools.list_ports

def get_serial_port():
    if sys.platform.startswith('win'):
        # Windows platform get ports
        print("It's a windows!")
        print("Trying to get windows port automatically...")
        #ports = ['COM%s' % (i + 1) for i in range(256)]
        ports = list(serial.tools.list_ports.comports())
        return ports[0]

    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # Linux platform get ports
        print("It's a linux!")
        print("Trying to get linux port automatically...")
        ser_devs = [dev for dev in os.listdir('/dev') if dev.startswith('ttyAC')]
        if len(ser_devs) > 0:
            return '/dev/' + ser_devs[0]
        else:
            return None
    elif sys.platform.startswith('darwin'):
        # Mac platform get ports
        print("It's a mac!")
        print("Trying to get mac port automatically...")
        ports = list(serial.tools.list_ports.comports())
        for p in ports:
            print(p)

        arduinoPort = ports[0]
        arduinoPortName = "/dev/" + arduinoPort.name
        return arduinoPortName
    else:
        raise EnvironmentError('Error finding ports on your operating system')
        return


port = None
while port == None:
    port = get_serial_port()

ser = None
while not ser:
    ser = serial.Serial(port=port, baudrate=115200, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE,
                         stopbits=serial.STOPBITS_ONE, timeout=1)

print("Serial connected!")
#ser = serial.Serial(port, 115200)


while(1):
    serialLine = str(ser.readline())
    serialNumber = serialLine.split("'")[1].split("\\")[0]
    print(serialNumber)
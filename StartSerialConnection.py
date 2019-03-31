#import torch
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
        arduino_ports = [
            p.device
            for p in serial.tools.list_ports.comports()
            if 'Arduino' in p.description
        ]
        if not arduino_ports:
            raise IOError("No Arduino found")
        if len(arduino_ports) > 1:
            print('Multiple Arduinos found - using the first')
        return arduino_ports[0]

    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # Linux platform get ports
        print("It's a linux!")
        print("Trying to get linux port automatically...")
        ser_devs = [dev for dev in os.listdir('/dev') if dev.startswith('ttyAC')]
        if len(ser_devs) > 0:
            return '/dev/' + ser_devs[0]
        else:
            print("No ports found")
            return None

    elif sys.platform.startswith('darwin'):
        # Mac platform get ports
        print("It's a mac!")
        print("Trying to get mac port automatically...")
        ports = list(serial.tools.list_ports.comports())
        if len(ports) == 0:
            print("No ports found")
            return None
        else:
            for p in ports:
                print(p)

            arduinoPort = ports[0]
            arduinoPortName = "/dev/" + arduinoPort.name
            return arduinoPortName

    else:
        raise EnvironmentError('Error finding ports on your operating system')


port = None
while port is None:
    port = get_serial_port()

ser = None
while True:
    try:
        ser = serial.Serial(port=port, baudrate=115200, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE,
                            stopbits=serial.STOPBITS_ONE, timeout=1)
        if (ser):
            break
    except:
        pass

print("Serial connected!")
#ser = serial.Serial(port, 115200)

ser.close()
ser.open()

ser.flushInput()
ser.flushOutput()

while(1):
    serialLine = str(ser.readline())
    serialNumber = serialLine.split("'")[1].split("\\")[0]
    print(serialNumber)
def sendCommand(command, serialPort):
        '''
        This function reads the output of the Tensorflow classification ( which is
        a string called human_string) and uses it to send an integer command to
        the Arduino.
        
        It takes two inputs, the string and a serial port to write to.
        '''

        if(command == "left"):
            serialPort.write(b'0')
            print("Sent '0' to Arduino (left)")
        elif(command == "right"):
            serialPort.write(b'1')
            print("Sent '1' to Arduino (right)")
        elif(command == "up"):
            serialPort.write(b'2')
            print("Sent '2' to Arduino (up)")
        elif(command == "down"):
            serialPort.write(b'3')
            print("Sent '3' to Arduino (down)")
        elif(command == "two"):
            serialPort.write(b'4')
            print("Sent '5' to Arduino (square / two)")
        elif (command == "three"):
            serialPort.write(b'5')
            print("Sent '4' to Arduino (tri / three)")
        elif(command == "four"):
            serialPort.write(b'6')
            print("Sent '6' to Arduino (round / four)")
        elif(command == "one"):
            serialPort.write(b'7')
            print("Sent '7' to Arduino (cross / one)")
        elif(command == "stop"):
            serialPort.write(b'8')
            print("Sent '8' to Arduino (stop)")
        elif(command == "go"):
            serialPort.write(b'9')
            print("Sent '9' to Arduino (go)")
        else:
            serialPort.write(b'99')
            print("Command not recognized (_unknown_)")
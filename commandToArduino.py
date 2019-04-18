def sendCommand(command, serialPort):
        '''
        This function reads the output of the Tensorflow classification ( which is
        a string called human_string) and uses it to send an integer command to
        the Arduino.
        
        It takes two inputs, the string and a serial port to write to.
        '''

        if(command == "left"):
            serialPort.write(b'1')
            print("Sent '1' to Arduino (left)")
        elif(command == "right"):
            serialPort.write(b'2')
            print("Sent '2' to Arduino (right)")
        elif(command == "up"):
            serialPort.write(b'3')
            print("Sent '3' to Arduino (up)")
        elif(command == "down"):
            serialPort.write(b'4')
            print("Sent '4' to Arduino (down)")
        elif(command == "square"):
            serialPort.write(b'5')
            print("Sent '5' to Arduino (square)")
        elif (command == "tri"):
            serialPort.write(b'6')
            print("Sent '6' to Arduino (tri)")
        elif(command == "round"):
            serialPort.write(b'7')
            print("Sent '7' to Arduino (round)")
        elif(command == "cross"):
            serialPort.write(b'8')
            print("Sent '8' to Arduino (cross)")
        elif(command == "stop"):
            serialPort.write(b'9')
            print("Sent '9' to Arduino (stop)")
        else:
            serialPort.write(b'10')
            print("Command not recognized (_unknown_)")
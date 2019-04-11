import serial

arduinoSerial = serial.Serial('COM3', 9600)

print(arduinoSerial)

def commandToArduino(tensor):
    command = tensor
    while 1:
        '''
        All Variables in this while loop should be changed to match Tensorflow
        such that var = input() is instead a check for what Tensorflow found
        
        Tensorflow returns 3 human_string strings and accuracies for them. We want
        to write it such that the top accuracy string is chosen as a check variable for ifs
        '''

        var = input()
        print("You entered ", var)

        if(var == '1'): #if(human_string == "left")
            arduinoSerial.write(b'1')
            print("Sent '1' to Arduino (left)")
        elif(var == '2'): #if(human_string == "right")
            arduinoSerial.write(b'2')
            print("Sent '2' to Arduino (right)")
        elif(var == '3'): #if(human_string == "up")
            arduinoSerial.write(b'3')
            print("Sent '3' to Arduino (up)")
        elif(var == '4'): #if(human_string == "down")
            arduinoSerial.write(b'4')
            print("Sent '4' to Arduino (down)")
        elif(var == '5'): #if(human_string == "square")
            arduinoSerial.write(b'5')
            print("Sent '5' to Arduino (square)")
        elif (var == '6'): #if(human_string == "tri")
            arduinoSerial.write(b'6')
            print("Sent '6' to Arduino (tri)")
        elif(var == '7'): #if(human_string == "round")
            arduinoSerial.write(b'7')
            print("Sent '7' to Arduino (round)")
        elif(var == '8'): #if(human_string == "cross")
            arduinoSerial.write(b'8')
            print("Sent '8' to Arduino (cross)")
        elif(var == '9'): #if(human_string == "stop")
            arduinoSerial.write(b'9')
            print("Sent '9' to Arduino (stop)")
        else:
            # In all other cases than the mapped words
            arduinoSerial.write(b'10')
            print("Command not recognized (_unknown_)")
#import torch
import wave
from time import sleep
import serial
import sys
import os
import serial.tools.list_ports
import tensorflow as tf
import argparse
import sys
import numpy as np
import pyaudio
import threading
import collections
import commandToArduino

baudRate = 2000000

labels = "speech_commands_train/conv_labels.txt"
graph = "speech_commands_train/my_frozen_graph.pb"
wav = "samples/leftTest.wav"

testingWithArduino = False


#####################################################
####### Audio input variables
#####################################################

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 16000
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"

p = pyaudio.PyAudio()

# You can specify which microphone input device you want to use
micDeviceIndex = -1
RMSthreshold = 2000
voiceExtractTimeSeconds = 1
lookBackBufferLength = 10 #43 is a second of length
audioCutSplitChunks = 4

info = p.get_host_api_info_by_index(0)
numdevices = info.get('deviceCount')
for i in range(0, numdevices):
        if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
            print("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))
            if micDeviceIndex == -1:
                if p.get_device_info_by_host_api_device_index(0, i).get('name') == "default":
                    micDeviceIndex = i



stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK,
                input_device_index=micDeviceIndex)

if stream.is_active():
    print("* recording")
else:
    print("* microphone serial connection not started")


def threadFunction(bufferInclude):

    print(bufferInclude)
    listOfWavData = []
    for thing in bufferInclude:
        listOfWavData.append(thing)

    streamLocal = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK,
                    input_device_index=micDeviceIndex)

    for i in range(0, int(RATE / CHUNK * voiceExtractTimeSeconds)):
        data = streamLocal.read(CHUNK)
        listOfWavData.append(data)
        if np_audioop_rms(data, CHUNK) < RMSthreshold:
            break

    print("Made it past recording")

    WAVE_OUTPUT_FILENAME = "samples/TemporaryWavSamplesSaved/tempWav" + str(threading.current_thread().ident) + ".wav"

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(listOfWavData))
    wf.close()

    with open(WAVE_OUTPUT_FILENAME, 'rb') as wav_file:
        wav_data = wav_file.read()
    os.remove(WAVE_OUTPUT_FILENAME)

    with tf.Session() as session:
        labels_list = load_labels(labels)

        # load graph, which is stored in the default session
        load_graph(graph)

        run_graph(wav_data, labels_list)


def np_audioop_rms(data, width):

    #_checkParameters(data, width)
    if len(data) == 0: return None
    d = np.frombuffer(data, np.int16).astype(np.float)
    #print(d)
    rms = np.sqrt((d*d).sum()/len(d))
    return int(rms)





#################################################



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


def load_graph(filename):
    """Unpersists graph from file as default graph."""
    with tf.gfile.GFile(filename, 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        tf.import_graph_def(graph_def, name='')


def load_labels(filename):
    """Read in labels, one label per line."""
    return [line.rstrip() for line in tf.gfile.GFile(filename)]


def run_graph(wav_data, labels):
    input_layer_name = "wav_data:0"
    output_layer_name = "labels_softmax:0"
    num_top_predictions = 3

    """Runs the audio data through the graph and prints predictions."""
    with tf.Session() as sess:
        # Feed the audio data as input to the graph.
        #   predictions  will contain a two-dimensional array, where one
        #   dimension represents the input image count, and the other has
        #   predictions per class
        softmax_tensor = sess.graph.get_tensor_by_name(output_layer_name)


        #wav_data = tf.convert_to_tensor(wav_data, np.float16)
        predictions, = sess.run(softmax_tensor, {input_layer_name: wav_data})

        # Sort to show labels in order of confidence
        top_k = predictions.argsort()[-num_top_predictions:][::-1]
        for node_id in top_k:
            human_string = labels[node_id]
            score = predictions[node_id]
            print('%s (score = %.5f)' % (human_string, score))
            if testingWithArduino:
                if score > 0.5:
                    commandToArduino.sendCommand(human_string, ser) # Send command read (human_string) to arduino
            break


def main(args):
    bufferInclude = collections.deque(maxlen=lookBackBufferLength)
    takingDataCountdown = audioCutSplitChunks
    while 1:
        data = stream.read(CHUNK)
        bufferInclude.append(data)
        # print(data)
        if np_audioop_rms(data, CHUNK) < RMSthreshold and takingDataCountdown > 0:
            takingDataCountdown -= audioCutSplitChunks
        if np_audioop_rms(data, CHUNK) > RMSthreshold and takingDataCountdown == 0:
            takingDataCountdown = audioCutSplitChunks
            thread = threading.Thread(target=threadFunction, args=([bufferInclude]))
            thread.start()

if testingWithArduino:
    port = get_serial_port()
    ser = serial.Serial(port, baudRate)
tf.app.run(main=main)








"""
startedActuallyRecording = False
arrayStartBuffer = []
meanPoint = 450

startTime = time.perf_counter()
bufferLength = 0

if testingWithArduino:
    while(1):
        serialLine = str(ser.readline())
        serialNumber = serialLine.split("'")[1].split("\\")[0]

        if (len(arrayStartBuffer) < baudRate and startedActuallyRecording == False):
            arrayStartBuffer.append(serialNumber)
            realTime = time.perf_counter()
            if (realTime-startTime > 1):
                print(len(arrayStartBuffer)-bufferLength)
                bufferLength = len(arrayStartBuffer)
                startTime = realTime
        elif (startedActuallyRecording == False):
            meanPoint = int(np.mean(arrayStartBuffer))
            startedActuallyRecording = True
        else:
            displacement = serialNumber - meanPoint
            print(displacement)


        #print(serialNumber)

"""
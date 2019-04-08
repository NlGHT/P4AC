#import torch
from time import sleep
import serial
import sys
import os
import serial.tools.list_ports
import tensorflow as tf
import argparse
import sys
import numpy as np
import scipy.io.wavfile as scipywave
from tensorflow.contrib.framework.python.ops import audio_ops as contrib_audio
from pathlib import Path

testingWithArduino = False

labels = "speech_commands_train/conv_labels.txt"
graph = "speech_commands_train/my_frozen_graph.pb"
wav = "samples/leftTest.wav"


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



if testingWithArduino:
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
    ser = serial.Serial(port, 115200)

    ser.close()
    ser.open()

    ser.flushInput()
    ser.flushOutput()



def load_graph(filename):
    """Unpersists graph from file as default graph."""
    with tf.gfile.GFile(filename, 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        tf.import_graph_def(graph_def, name='')


def load_labels(filename):
    """Read in labels, one label per line."""
    return [line.rstrip() for line in tf.gfile.GFile(filename)]


def run_graph(wav_data, labels, threadNumber):
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
        wav_data = np.array(wav_data[1],dtype=np.int16)
        print(wav_data[100])
        tempWavPath = "samples/TemporaryWavSamplesSaved/waveTest" + str(threadNumber)

        scipywave.write(tempWavPath, 44100, wav_data)
        with open(tempWavPath, 'rb') as wav_file:
            wav_data = wav_file.read()
        os.remove(tempWavPath)


        #wav_data = tf.convert_to_tensor(wav_data, np.float16)
        predictions, = sess.run(softmax_tensor, {input_layer_name: wav_data})

        # Sort to show labels in order of confidence
        top_k = predictions.argsort()[-num_top_predictions:][::-1]
        for node_id in top_k:
            human_string = labels[node_id]
            score = predictions[node_id]
            print('%s (score = %.5f)' % (human_string, score))


def main(threadNumber):
    with tf.Session() as session:
        labels_list = load_labels(labels)

        # load graph, which is stored in the default session
        load_graph(graph)

        wav_data = scipywave.read("samples/leftTest.wav")

        run_graph(wav_data, labels_list, threadNumber[0])


threadNumber = 0

if not testingWithArduino:
    tf.app.run(main=main, argv=[threadNumber])


if testingWithArduino:
    while(1):
        serialLine = str(ser.readline())
        serialNumber = serialLine.split("'")[1].split("\\")[0]

        print(serialNumber)
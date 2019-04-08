import torch
from time import sleep
import serial
import sys
import os
import serial.tools.list_ports
import tensorflow as tf
import argparse
import sys

labels = "speech_commands_train/conv_labels.txt"
graph = "speech_commands_train/my_frozen_graph.pb"
wav = "samples/leftTest.wav"


def get_serial_port():
    if sys.platform.startswith('win'):
        # Windows platform get ports
        print("It's a windows!")
        print("Trying to get windows port automatically...")
        #ports = ['COM%s' % (i + 1) for i in range(256)]
        ports = list(serial.tools.list_ports.comports())
        if ports.count() == 0:
            print("No ports found")
            return None
        else:
            return ports[0]

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
        if ports.count() == 0:
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

"""
port = None
while port == None:
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
"""

print("Serial connected!")
#ser = serial.Serial(port, 115200)


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
        predictions, = sess.run(softmax_tensor, {input_layer_name: wav_data})

        # Sort to show labels in order of confidence
        top_k = predictions.argsort()[-num_top_predictions:][::-1]
        for node_id in top_k:
            human_string = labels[node_id]
            score = predictions[node_id]
            print('%s (score = %.5f)' % (human_string, score))


def main(_):

    with tf.Session() as session:
        labels_list = load_labels(labels)

        # load graph, which is stored in the default session
        load_graph(graph)

        with open(wav, 'rb') as wav_file:
            wav_data = wav_file.read()
            print(len(wav_data))

        run_graph(wav_data, labels_list)



tf.app.run(main=main, argv=None)

    #saver = tf.train.Saver()
    #saver.restore(session, "speech_commands_train/conv.ckpt-18000")



#while(1):
    #serialLine = str(ser.readline())
    #serialNumber = serialLine.split("'")[1].split("\\")[0]

    #print(serialNumber)
#!/usr/bin/env python
from flask import Flask, render_template, Response, redirect
from camera import Camera
import sys
import paho.mqtt.client as mqtt
import threading
import time


def on_connect(client, userdata, flags,rc):
    print('Connected with result {0}'.format(rc))

     
def on_message(client, userdata, msg):
    #client.publish(b"asdf",b"too")
    m = msg.payload.decode("utf-8")    
    print(m)
    
client = mqtt.Client()
client.connect('localhost',1883,60)
client.on_connect = on_connect
client.on_message = on_message


app = Flask(__name__)

@app.route('/')
def index():
   return render_template('index.html')

def gen(camera):
   while 1:
       frame = camera.get_frame()
       yield (b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

 

@app.route('/Open/')
def button_clicked():
    global client
    client.publish('Led','Open')
    return redirect('/')
   
@app.route('/Close/')
def button_clicked2():
    global client
    client.publish('Led','Close')
    return redirect('/')
   
@app.route('/video')
def video():
   return Response(gen(Camera()),
                   mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
   app.run(host='192.168.0.12', debug=True,threaded = True , port = 5000) #Host is your Localhost address

#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
from flask import Flask,redirect,render_template,url_for
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    #return redirect(url_for('index'))
    return render_template("index.html")

@app.route("/system_start/")
def system_start():
    command = ["python3", "light_cencer_relay_motor_time.py"]
    proc = subprocess.Popen(command) 
    print("カーテン自動開放システム起動")
    return render_template("index.html")

@app.route("/system_stop/")
def system_stop():
    subprocess.run(["./system_stop.sh"])
    print("カーテン自動開放システム停止")
    return render_template("index.html")

@app.route("/open/")
def open():
    GPIO.output(17,True)
    print("カーテン開放。自分で停止ボタンを押してください。")
    return render_template("index.html")

@app.route("/stop_open/")
def stop_open():
    GPIO.output(17,False)
    print("カーテン開放停止")
    return render_template("index.html")

if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(17,GPIO.OUT)
    app.run(port=8000, host='192.168.10.106', debug=True)

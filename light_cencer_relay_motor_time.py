#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import spidev
import RPi.GPIO as GPIO
from time import sleep
import datetime
now = datetime.datetime.now()

setTime = now.replace(hour=8, minute=0, second=0, microsecond=0)

V_REF = 3.29476 # 入力電圧
CHN = 0 # 接続チャンネル(SPI通信用)
LED = 27 # LED点灯用GPIO
relayPin = 17
count = 0

#LEDを光らせるためのGPIOを有効化、出力モードに設定
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED, GPIO.OUT)
GPIO.setup(relayPin, GPIO.OUT)

spi = spidev.SpiDev()
spi.open(0, 0) # 0：SPI0、0：CE0 SPIバスへアクセス
spi.max_speed_hz = 1000000 # 1MHz SPIのバージョンアップによりこの指定をしないと動かない

def get_voltage():
    dout = spi.xfer2([((0b1000+CHN)>>2)+0b100,((0b1000+CHN)&0b0011)<<6,0]) # Din(RasPi→MCP3208）を指定
    bit12 = ((dout[1]&0b1111) << 8) + dout[2] # Dout（MCP3208→RasPi）から12ビットを取り出す
    volts = round((bit12 * V_REF) / float(4095),4)  # 取得した値を電圧に変換する（12bitなので4095で割る）
    return volts # 電圧を返す

def destroy():
    GPIO.cleanup()

try:
    print('--- start program ---')
    while True:
        volts = get_voltage()
        print('volts= {:3.2f}'.format(volts))
        # 暗くなるとフォトレジスタの抵抗が増えるのでspiの電圧が下がる
        if volts > 1.0 and now > setTime: # 2 Volts以下なら点灯
        #if volts > 1.0: # 2 Volts以下なら点灯
            GPIO.output(relayPin, GPIO.HIGH) 
            sleep(1)
            count+=1
            print("count=" + str(count))
            if count == 10:
                sys.exit()
        else:
            GPIO.output(relayPin, GPIO.LOW)
            print("count=" + str(count))
            sleep(1)

except KeyboardInterrupt:
    destroy()
finally:
    spi.close()
    GPIO.cleanup()
    print('--- stop program ---')


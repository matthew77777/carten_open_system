#!/bin/sh

ps aux | grep light_cencer_relay_motor_time.py | grep -v grep | awk '{ print "kill -9", $2 }' | sh


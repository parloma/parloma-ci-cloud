#!/usr/bin/env python3
import os
import time

for i in range(41):
    os.system("echo {} > /sys/class/leds/led0/brightness".format(i%2))
    time.sleep(0.1)                
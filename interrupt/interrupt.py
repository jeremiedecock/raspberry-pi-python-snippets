#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Jérémie DECOCK (http://www.jdhp.org)

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# Dependencies (Raspbian):
#
#    aptitude install python3-rpi.gpio
#
# Pinout:
#
#     Model A, Model B rev.2:
#                  _ _
#        3.3V    -| V |-    5V
#   (i2c) SDA  2 -|   |-    5V
#   (i2c) SCL  3 -|   |-    GND
#              4 -|   |- 14 TXD (serial)
#         GND    -|   |- 15 RXD (serial)
#             17 -|   |- 18
#             27 -|   |-    GND
#             22 -|   |- 23
#        3.3V    -|   |- 24
#  (spi) MOSI 10 -|   |-    GND
#  (spi) MISO  9 -|   |- 25
#  (spi) SCKL 11 -|   |- 8
#         GND    -|   |- 7
#                  --- 
#
# The GPIO uses 3.3V for all inputs and outputs.
# Any pin with a number next to it can act as a GPIO pin.
#
# Special pins:
# - TXD, RXD = the serial interface
# - SDA, SCL = the I2C interface
# - MOSI, MISO, SCKL = the SPI interface
#
# Warning:
# - Do not put more than 3.3V on any GPIO pin.
# - Do not draw more than 3mA per output.
# - Do not draw more than a total of 50mA from the 3.3V supply pins.
# - Do not draw more than a total of 250mA from the 5V supply pins.

# Warning: you should execute this script as "root" to get the right to handle GPIO pins.

# Inspired by "Recipe 9.12" of the "Raspberry Pi Cookbook" by Simon Monk (ed. Oreilly)

# Read a button state on GPIO pin 22 with interrupts.
#
#    pin 22 ---/ --- GND pin
#            switch

import RPi.GPIO as gpio
import time

btn_pin = 22

def btn_callback(channel):
    """Our interrupt callback.
    
    The 'chennel' variable specifies the input that triggered the interrupt.
    """

    print("Button pressed (channel =", channel, ")")

def main():
    """Main function"""
    
    # gpio.setmode: set up numbering mode to use for channels.
    # - gpio.BOARD = use Raspberry Pi board numbers.
    # - gpio.BCM = use  Broadcom GPIO 00..nn numbers.
    gpio.setmode(gpio.BCM)

    # Setup pin 22 as input (in pull-up mode)
    gpio.setup(btn_pin, gpio.IN, pull_up_down=gpio.PUD_UP)

    # Define the interrupt
    # - gpio.FALLING = the callback function will only be called if the GPIO pin goes from high to low (button pressed)
    # - gpio.RISING = the callback function will only be called if the GPIO pin goes from low to high (button released)
    # - bouncetime = use an internal debounce routine using the specified time in milliseconds [optional]
    gpio.add_event_detect(btn_pin, gpio.FALLING, callback=btn_callback, bouncetime=5)
    #gpio.add_event_detect(btn_pin, gpio.FALLING, callback=btn_callback)               # Without debounce

    while True:
        print(".")
        time.sleep(0.1)   # Wait 0.1 second

if __name__ == '__main__':
    main()

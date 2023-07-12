# esp32 板载led灯
import uos
from machine import Pin
from micropython import const

_led_pin_2 = Pin(2, Pin.OUT, Pin.PULL_UP)
_led_pin_7 = Pin(7, Pin.OUT, Pin.PULL_UP)

current_board = const("ESP32S3")
board = uos.uname()[4]


def on_led():
    if current_board in board:
        _led_pin_7.value(1)
    else:
        _led_pin_2.value(1)


def off_led():
    if current_board in board:
        _led_pin_7.value(0)
    else:
        _led_pin_2.value(0)

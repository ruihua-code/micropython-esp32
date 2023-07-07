# esp32 板载led灯

from machine import Pin
_led_pin_2 = Pin(2, Pin.OUT)


def on_led():
    _led_pin_2.value(1)


def off_led():
    _led_pin_2.value(0)

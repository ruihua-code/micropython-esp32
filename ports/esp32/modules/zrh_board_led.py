# esp32 板载led灯

from machine import Pin
led_pin_2 = Pin(2, Pin.OUT)


def on_led():
    led_pin_2.value(1)


def off_led():
    led_pin_2.value(0)

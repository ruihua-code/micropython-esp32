from machine import Pin

_led_pin_15 = Pin(15, Pin.OUT, Pin.PULL_UP)


def do_led(value):
    if _led_pin_15.value() == value:
        return
    _led_pin_15.value(value)

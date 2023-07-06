from machine import Pin

led_pin_15 = Pin(15, Pin.OUT, Pin.PULL_UP)


def do_led(value):
    if led_pin_15.value() == value:
        return
    led_pin_15.value(value)

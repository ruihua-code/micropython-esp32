from machine import Pin

led_pin_15 = Pin(15, Pin.OUT)


def do_led(value):
    print(led_pin_15.value())
    if led_pin_15.value() == value:
        return
    led_pin_15.value(value)

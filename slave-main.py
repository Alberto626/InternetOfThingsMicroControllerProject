# Imports go at the top
from microbit import *
import radio

# Code in a 'while True:' loop repeats forever
radio.on()
radio.config(group=32, power=7)
display.show(Image('99999:'
                   '90000:'
                   '99999:'
                   '00009:'
                   '99999'))
while True:
    soundLevel = microphone.sound_level()
    radio.send(str(soundLevel))
    sleep(200)
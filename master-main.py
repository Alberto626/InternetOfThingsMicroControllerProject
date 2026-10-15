# Imports go at the top
from microbit import *
import radio

# Code in a 'while True:' loop repeats forever
radio.on()
uart.init(baudrate=115200)  # even though functions arent used, baudrate has to match with python script
while True:
    message = radio.receive()

    if message and int(message):  # NonEmpty string
        soundLevel = int(message)
        soundState = ""
        if soundLevel < 50:
            soundState = "quiet"
            display.show(Image('00000:'
                               '00000:'
                               '00000:'
                               '00000:'
                               '90000'))
            sleep(200)

        elif soundLevel < 100:
            soundState = "good"
            display.show(Image('00000:'
                               '00000:'
                               '00000:'
                               '09000:'
                               '99000'))
            sleep(200)
        elif soundLevel < 150:
            soundState = "careful"
            display.show(Image('00000:'
                               '00000:'
                               '00900:'
                               '09900:'
                               '99900'))
            sleep(200)
        elif soundLevel < 200:
            soundState = "warning"
            display.show(Image('00000:'
                               '00090:'
                               '00990:'
                               '09990:'
                               '99990'))
            print(soundState)
            sleep(1000)
        else:  # super loud
            soundState = "shutdown"
            display.show(Image('00009:'
                               '00099:'
                               '00999:'
                               '09999:'
                               '99999'))
            print(soundState)
            sleep(1000)

    if button_a.is_pressed():
        # uart.write("test")
        print("test")


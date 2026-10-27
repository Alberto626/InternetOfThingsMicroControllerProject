# Imports go at the top
from microbit import *
import radio

# Code in a 'while True:' loop repeats forever
radio.on()
radio.config(group=32, power=7)
uart.init(baudrate=115200)  # even though functions arent used, baudrate has to match with python script
soundLevelIncrement = 0;  # If you want to lower the threshold of each if statement, press the buttons
while True:
    message = radio.receive()

    if message and int(message):  # NonEmpty string
        soundLevel = int(message)
        soundState = ""
        if button_a.is_pressed and button_b.is_pressed():
            print("Both buttons are pressed")
            soundLevelIncrement = 0
            display.show(Image('00900:'
                               '09090:'
                               '90009:'
                               '09090:'
                               '00900'))
            sleep(1000)
        elif button_a.is_pressed():
            soundLevelIncrement -= 1
            print("button a is pressed")
            display.show(Image('00000:'
                               '00000:'
                               '99999:'
                               '00000:'
                               '00000'))
            sleep(1000)
        elif button_b.is_pressed():
            print("button b is pressed")
            soundLevelIncrement += 1
            display.show(Image('00900:'
                               '00900:'
                               '99999:'
                               '00900:'
                               '00900'))
            sleep(1000)

        if soundLevel < 50 + soundLevelIncrement:  # if you want to change the threshold press the buttons
            display.show(Image('00000:'
                               '00000:'
                               '00000:'
                               '00000:'
                               '90000'))

            sleep(200)

        elif soundLevel < 100 + soundLevelIncrement:
            display.show(Image('00000:'
                               '00000:'
                               '00000:'
                               '09000:'
                               '99000'))
            sleep(200)
        elif soundLevel < 150 + soundLevelIncrement:
            display.show(Image('00000:'
                               '00000:'
                               '00900:'
                               '09900:'
                               '99900'))
            sleep(200)
        elif soundLevel < 200 + soundLevelIncrement:
            soundState = "warning"
            display.show(Image('00000:'
                               '00090:'
                               '00990:'
                               '09990:'
                               '99990'))
            uart.write(soundState)
            sleep(200)
        else:  # super loud
            soundState = "shutdown"
            display.show(Image('00009:'
                               '00099:'
                               '00999:'
                               '09999:'
                               '99999'))
            uart.write(soundState)
            sleep(200)


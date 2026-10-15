import signal
import datetime
from sys import exit
import serial
import time
import psutil
import os
from win11toast import toast
PORT = "COM4" # TODO figure out how to set Port number
BAUD = 115200
game = "cs2.exe" # for laptop game is og 1.6
game_path = r"C:\Program Files (x86)\Steam\steamapps\common\Counter-Strike Global Offensive\game\bin\win64\cs2.exe"

def main():
    try:
        with serial.Serial(PORT, BAUD, timeout=1.0) as connection:
            time.sleep(2) #sleep for 2 seconds
            print(f"Connected to {PORT}")
            print("Waiting for sensor messages")
            while True:
                line = connection.readline().decode("utf-8",errors="replace").strip()
                if not line: #if line is empty
                    print("line is empty")
                    continue
                elif line == "quiet":
                    print("line is empty")
                elif line == "OpenCS":
                    if find_process(game) is None:# if we dont find cs
                        print('OPEN CS')# to do
                elif line == "careful":
                    print("line is empty")
                elif line == "warning": # ONLY FOR TESTING PURPOSES
                    print("line is empty")
                elif line == "shutdown":
                    print("line is empty");
    except serial.SerialException as e:
        print("Error opening serial port")

def find_process(message): #look for specific process in computer
    for process in psutil.process_iter():
        if process.name().startswith(message):
            return process
    return None #if we dont find anything

def run_at_day():
    while True:
        if datetime.now().hour > 20 or datetime.now().hour <6: #between 8pm and 6am
            print("Program only runs at night.")
            time.sleep(300)
def displayWindowsNotification():
    toast("test")
#run_at_day() #program will only run at night
displayWindowsNotification()
#gameProcess = find_process(game)
#os.kill(gameProcess.pid, signal.SIGTERM)
#print(gameProcess.pid)
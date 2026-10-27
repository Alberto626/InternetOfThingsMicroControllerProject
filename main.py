import re
import winreg
from pathlib import Path

import serial #serial communication
import time
import psutil #tracking processes

from typing_extensions import deprecated
from win11toast import toast #Windows notification feature
from serial.tools import list_ports #Find ports on windows

BAUD = 115200
SCRIPT_DIR = Path(__file__).resolve().parent#when running the project the file its running on is venv file, we need the path to the pythonProject folder


def main():
    try:
        with serial.Serial(PORT, BAUD, timeout=1.0) as connection:
            time.sleep(2) #sleep for 2 seconds, to let the program communicate to the port and contoller.
            print(f"Connected to {PORT}")
            print("Waiting for sensor messages")
            while True:
                line = connection.readline().decode("utf-8",errors="replace").strip()
                if not line: #if we receive no message
                    continue # dont do anything
                elif line == "warning": #State giving to us by the micro:bit controller
                    print("Warning detected")  # more for testing
                    if len(find_running_games()) > 0:#if any games that are running
                        display_windows_notification()

                elif line == "shutdown":
                    print("SHUTDOWN detected")
                    allRunningGames = find_running_games() #look for the games that are running,
                    if len(allRunningGames) > 0: #if our dictionary is not empty
                        for gameName, processes in allRunningGames.items() :#get all processes
                            close_game(processes) #close all processes
                print(line)
    except serial.SerialException as e:
        print("Error opening serial port")
@deprecated("different methods are used to shutdown")
def find_process(message): #look for specific process in computer
    for process in psutil.process_iter():#look through the entire list of everysingle process running on the computer
        if process.name().startswith(message):#if the process name matches what we are looking for
            return process #return the process
    return None #if we dont find anything, return the equivalent of null

def display_windows_notification():

    image = {
        "src": str(SCRIPT_DIR / "shh.jpg"),#Find the relative path of the image file.
        #'placement': 'hero' # maek the image large
    };
    toast("YOUR TOO LOUD",image =image)#,duration = 'long' )

def find_microbit_port():
    MICROBIT_VID = 0x0D28 #the manufacturer or company that built the usb device
    MICROBIT_PID = 0x0204 #the exact model id for micro:bit controller
    for port in list_ports.comports(): #Look at all possible ports
        if port.vid == MICROBIT_VID and port.pid == MICROBIT_PID: #which port matches our VID and PID
            return port.device  # e.g. "COM3"
    return None #if not detected return null

def get_steam_path():
    #Steam stores its install location under this registry key
    #HKey_current_user is the user of Windows, so if your name is Alberto on Lindsay on the computer, its your name
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Valve\Steam") as key:
        return Path(winreg.QueryValueEx(key, "SteamPath")[0])
    #return the Path that the registry gives us where Steam is installed

def get_library_folders(steam_path):
    vdf = steam_path / "steamapps" / "libraryfolders.vdf"
    text = vdf.read_text(encoding="utf-8")
    #read the path key and tell me where all the games installed can be stored at.
    paths = re.findall(r'"path"\s+"([^"]+)"', text)
    return [Path(p.replace("\\\\", "\\")) for p in paths]#replace any \\\\ and turn them into \\
    #The return portion is just in case there are multiple libraries


def get_installed_games():
    """Returns {game_name: install_folder_path}"""
    games = {}
    #find look at
    for library in get_library_folders(get_steam_path()):
        steamapps = library / "steamapps"
        #every installed game has a appmanifest_<id>.acf which holds meta data,
        for manifest in steamapps.glob("appmanifest_*.acf"):
            #make the text readable
            text = manifest.read_text(encoding="utf-8", errors="ignore")
            #search the games name,
            name = re.search(r'"name"\s+"([^"]+)"', text)
            #What is the name of the folder that the game is installed on
            installdir = re.search(r'"installdir"\s+"([^"]+)"', text)
            if name and installdir:
                games[name.group(1)] = steamapps / "common" / installdir.group(1)
    return games

def find_running_games():
    """Returns {game_name: [psutil.Process, ...]}"""
    games = get_installed_games()
    running = {}
    #iternate through all processes and get pid, name , and the exe file
    for proc in psutil.process_iter(["pid", "name", "exe"]):
        exe = proc.info["exe"]

        #sometimes the system will deny us access to progams, almost never games though
        if not exe:
            continue  # access denied or system process
        exe_path = Path(exe)

        #Now we check if the process matches what we have in installed games
        for name, folder in games.items():
            if folder in exe_path.parents:
                running.setdefault(name, []).append(proc)
    return running

def close_game(processes):
    for proc in processes:
        try:
            proc.terminate() #terminate the process gracefully, let it clean up first
        except psutil.NoSuchProcess:
            pass
    _, alive = psutil.wait_procs(processes, timeout=5)
    for proc in alive:#if any process is still alive
        proc.kill()  # forcefully kill if it ignored terminate

#display_windows_notification()
PORT = find_microbit_port()

main()


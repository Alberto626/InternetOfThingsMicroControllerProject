import re
import winreg
from pathlib import Path

import psutil  # pip install psutil

#THIS WAS FOR PURELY TESTING PURPOSES,DO NOT USE
def get_steam_path():
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Valve\Steam") as key:
        return Path(winreg.QueryValueEx(key, "SteamPath")[0])


def get_library_folders(steam_path):
    vdf = steam_path / "steamapps" / "libraryfolders.vdf"
    text = vdf.read_text(encoding="utf-8")
    paths = re.findall(r'"path"\s+"([^"]+)"', text)
    return [Path(p.replace("\\\\", "\\")) for p in paths]


def get_installed_games():
    """Returns {game_name: install_folder_path}"""
    games = {}
    for library in get_library_folders(get_steam_path()):
        steamapps = library / "steamapps"
        for manifest in steamapps.glob("appmanifest_*.acf"):
            text = manifest.read_text(encoding="utf-8", errors="ignore")
            name = re.search(r'"name"\s+"([^"]+)"', text)
            installdir = re.search(r'"installdir"\s+"([^"]+)"', text)
            if name and installdir:
                games[name.group(1)] = steamapps / "common" / installdir.group(1)
    return games
def find_running_games():
    """Returns {game_name: [psutil.Process, ...]}"""
    games = get_installed_games()
    running = {}
    for proc in psutil.process_iter(["pid", "name", "exe"]):
        exe = proc.info["exe"]
        if not exe:
            continue  # access denied or system process
        exe_path = Path(exe)
        for name, folder in games.items():
            if folder in exe_path.parents:
                running.setdefault(name, []).append(proc)
    return running
print(find_running_games())
for key, value in find_running_games().items():
    print(f"{key}: {value[0].pid}")
    print(isinstance(value[0].pid, (int, float)))

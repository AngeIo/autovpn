import os
import shutil
import glob
import sys
import sysconfig
import winreg
from win32com.client import Dispatch
import subprocess
import winshell
import requests
import ctypes

program_name = "autovpn"

current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)

def parent_dir_file_path(path):
    return os.path.join(parent_dir, path)

def get_reg(name,path):
    try:
        registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, path, 0,
                                       winreg.KEY_READ)
        value, regtype = winreg.QueryValueEx(registry_key, name)
        winreg.CloseKey(registry_key)
        return value
    except WindowsError:
        return None

# Remove autovpn.exe in the current directory
if os.path.exists(parent_dir_file_path(program_name + '.exe')):
    os.remove(parent_dir_file_path(program_name + '.exe'))
# Add your pyinstaller command here
os.system('pyinstaller --onefile --noconsole --icon "' + parent_dir_file_path('assets/icon.ico') + '" "' + parent_dir_file_path(program_name + '.py') + '"')
# Check if autovpn.exe exists in the dist folder
if os.path.exists(parent_dir_file_path('dist/' + program_name + '.exe')):
    # Move autovpn.exe from dist to the current folder
    shutil.move(parent_dir_file_path('dist/' + program_name + '.exe'), parent_dir)
    # Check if dist folder is empty
    if not os.listdir(parent_dir_file_path('dist')):
        # Remove the dist folder
        shutil.rmtree(parent_dir_file_path('dist'))
    else:
        print("The dist folder is not empty. Not deleting.")
else:
    print("autovpn.exe does not exist in the dist folder.")

# --- Shortcut creation to current user desktop ---
# Target of shortcut
target = parent_dir_file_path(program_name + '.exe')
# Name of link file
linkName = program_name + '.lnk'
# Read location of Windows desktop folder from registry
desktopFolder = os.path.normpath(get_reg('Desktop', r'Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders'))
# Path to location of link file
pathLink = os.path.join(desktopFolder, linkName)
shell = Dispatch('WScript.Shell')
shortcut = shell.CreateShortCut(pathLink)
shortcut.Targetpath = target
shortcut.WorkingDirectory = parent_dir
shortcut.IconLocation = parent_dir_file_path('assets/icon.ico')
shortcut.save()

# --- Shortcut creation to user taskbar (pin) ---
program_name_pttb = 'pttb.exe'
program_path_pttb = shutil.which(program_name_pttb)
if program_path_pttb is None:
    # The program is not installed, download it
    url = 'https://github.com/0x546F6D/pttb_-_Pin_To_TaskBar/releases/download/230124/pttb.exe'
    response = requests.get(url, allow_redirects=True)
    # Save the program to the current directory
    with open(program_name_pttb, 'wb') as f:
        f.write(response.content)
    print(f"{program_name_pttb} downloaded.")
else:
    print(f"{program_name_pttb} is already installed.")

# --- Create a shortcut to the taskbar ---
desktop = winshell.desktop()
pathLink = os.path.join(desktop, f"{program_name}.lnk")
target = os.path.join(parent_dir, f"{program_name}.exe")
icon = parent_dir_file_path('assets/icon.ico')
shell = Dispatch('WScript.Shell')
shortcut = shell.CreateShortcut(pathLink)
shortcut.TargetPath = target
shortcut.WorkingDirectory = parent_dir
shortcut.IconLocation = icon
shortcut.save()
# Run the program and pin it to the taskbar
command = [program_name_pttb, target]
subprocess.run(command, shell=True)

# --- Remove temp build files ---
# Remove .spec files
for spec_file in glob.glob(parent_dir_file_path('**/*.spec'), recursive=True):
    os.remove(spec_file)
# Remove build folder
if os.path.exists(parent_dir_file_path('build')):
    shutil.rmtree(parent_dir_file_path('build'))
# Remove __pycache__ folders
for pycache in glob.glob(parent_dir_file_path('**/__pycache__'), recursive=True):
    shutil.rmtree(pycache)
flag_autostart = False
answer = None
# Ask user if they want to add the script to Windows startup process
MessageBox = ctypes.windll.user32.MessageBoxW
# If the script is already in the Windows startup process, skip this step
startup_path = os.path.join(os.path.expanduser('~'), 'AppData', 'Roaming', 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
startup_pathLink = os.path.join(startup_path, f"{program_name}.lnk")
if os.path.exists(startup_pathLink):
    print("The script is already in the Windows startup process.")
    flag_autostart = True
if flag_autostart == False:
    answer = MessageBox(None, "Do you want to add the script to the Windows' startup process so it opens each time you log in?", program_name + ' - Autostart?', 0x4 | 0x30 | 0x1000) # Respectively: MB_YESNO | MB_ICONWARNING | MB_SYSTEMMODAL
if answer == 6 or flag_autostart == True:
    # Add script to Windows startup process
    icon = parent_dir_file_path('assets/icon.ico')
    shortcut_startup = shell.CreateShortcut(startup_pathLink)
    shortcut_startup.TargetPath = target
    shortcut_startup.WorkingDirectory = parent_dir
    shortcut_startup.IconLocation = icon
    shortcut_startup.save()
    if answer == 6:
        print('The script has been added to the Windows startup process!\n\nNext time you will restart your computer or log out and log in, the script will open automatically!')

sys.exit(0)

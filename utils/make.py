import os
import shutil
import glob
import sys
from win32com.client import Dispatch
import ctypes

program_name = "autovpn"

current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)

def parent_dir_file_path(path):
    return os.path.join(parent_dir, path)

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
# Details about MessageBoxW:
# https://learn.microsoft.com/fr-fr/windows/win32/api/winuser/nf-winuser-messageboxw
# https://stackoverflow.com/questions/2963263/how-can-i-create-a-simple-message-box-in-python
# https://stackoverflow.com/questions/76020424/how-to-display-the-blue-warning-message-box-of-windows-in-python
# https://stackoverflow.com/questions/27257018/python-messagebox-with-icons-using-ctypes-and-windll
if answer == 6 or flag_autostart == True:
    # Add script to Windows startup process
    icon = parent_dir_file_path('assets/icon.ico')
    shell = Dispatch('WScript.Shell')
    shortcut_startup = shell.CreateShortcut(startup_pathLink)
    shortcut_startup.TargetPath = target
    shortcut_startup.IconLocation = icon
    shortcut_startup.save()
    if answer == 6:
        print('The script has been added to the Windows startup process!\n\nNext time you will restart your computer or log out and log in, the script will open automatically!')
sys.exit(0)

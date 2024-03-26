import shutil
import time
import os
from urllib.request import urlretrieve
import hashlib
import sys
import patoolib
import ssl

os.system("")
ssl._create_default_https_context = ssl._create_unverified_context
extractedISOFolder = "extracted-MKW"
moddedISOFolder = "modded_mkw"
modFiles = "modded"
witLinuxDownload = "https://wit.wiimm.de/download/wit-v3.05a-r8638-x86_64.tar.gz"
witWindowsDownload = "https://wit.wiimm.de/download/wit-v3.05a-r8638-cygwin64.zip"
modDownload = "https://files.gamebanana.com/mods/my_2c6e9.7z"
witMD5 = "1d19d13665fa5eae951cdfa410bb6b65"
modMD5 = "dbc259dc2499b88822011055356821bf"
witWindowsMD5 = "665b07e519d58b88043cb085fde3e3af"
modFileCount = 736
copyPaths = ["/sound",
             "/sound/strm",
             "/Race",
             "/Race/Course",
             "/Race/Kart"]


class bcolors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def listfiles(PATH):
    for root, folders, files in os.walk(PATH):
        for filename in folders + files:
            yield os.path.join(root, filename)


def fileCount(PATH):
    return sum(os.path.isfile(os.path.join(PATH, f)) for f in os.listdir(PATH))


def checkMd5(FILE, MD5):
    print(f"Checking MD5 to verify file {bcolors.BLUE}{FILE}{bcolors.ENDC}...")
    if hashlib.md5(open(FILE, 'rb').read()).hexdigest() != MD5:
        print(f"{bcolors.RED}MD5 does not match{bcolors.ENDC}")
        return False
    else:
        print(f"{bcolors.GREEN}MD5 does match{bcolors.ENDC}")
        return True


def download(URL, PATH, MD5):
    for x in range(3):
        if not os.path.exists(PATH):
            print(f"Downloading {bcolors.BLUE}" + URL + f"{bcolors.ENDC} to {bcolors.BLUE}" + PATH + bcolors.ENDC)
            urlretrieve(URL, PATH)
        else:
            if not checkMd5(PATH, MD5):
                print(f"{bcolors.RED}MD5 differs, redownloading{bcolors.ENDC}")
                print(f"Downloading {bcolors.BLUE}" + URL + f"{bcolors.ENDC} to {bcolors.BLUE}" + PATH + bcolors.ENDC)
                urlretrieve(URL, PATH)
            else:
                break
        time.sleep(1)


# Functions and variables ^^^^^

print(f"{bcolors.WARNING}WARNING!!\nThis will install the WIT binary for extracting and combining your mario kart "
      f"iso.\nYou can simply just delete this file once youre done\nThis will also download the mods from "
      f"gamebanana\nThe mod is 400Mb and will take a bit of time.\nBoth of these files will be in the directory where "
      f"this script is\nIf you do not want to continue please press Ctrl+C to cancel the script\nOtherwise, "
      f"press enter :){bcolors.ENDC}")
input()

while True:
    isoPath = input("\nPlease type the path of your Mario Kart ISO \nfor easy use just place the iso directly next to"
                    " this file \nand write the filename (e.g, mariokart.iso)\n\n")
    if not os.path.exists(isoPath):
        print(f"{bcolors.RED}File doesnt seem to exist. \nMake sure you typed the file path correctly.{bcolors.ENDC}")
    else:
        break


# Download WIT for linux by checking platform
if sys.platform.startswith('linux'):
    # Linux code

    # Check if WIT zip file exists
    if not os.path.exists("wit.tar.gz"):

        print("\nDownloading wit for Linux\n")
        download(witLinuxDownload, "wit.tar.gz", witMD5)

        # Double check incase 3 download attempts don't work for some reason
        print(f"{bcolors.WARNING}Double checking for sure...{bcolors.ENDC}")
        if not checkMd5("wit.tar.gz", witMD5):
            print(
                f"{bcolors.RED}Sorry the download didnt seem to work. \nplease make sure youre using the latest version "
                f"of this script.\nor create an issue at github {bcolors.ENDC}")
            quit()
    else:
        print("WIT is downloaded, not downloading again...")

        # Check if executable is extracted, extract it if not
    if not os.path.exists("wit"):
        print(f"Extracting archive {bcolors.BLUE}wit.tar.gz{bcolors.ENDC} to {bcolors.BLUE}{os.getcwd()}{bcolors.ENDC}")
        patoolib.extract_archive("wit.tar.gz", outdir=f"{os.getcwd()}/witdir")
    else:
        print("Executable exists, not extracting...")

    # End of Linux code

# Download WIT for Windows
elif sys.platform.startswith('win32'):
    # Windows code
    print("Downloading wit for Windows")

    download(witWindowsDownload, "wit.zip", witWindowsMD5)

    if not checkMd5("wit.zip", witWindowsMD5):
        print(f"{bcolors.RED}Sorry the download didnt seem to work. \nplease make sure youre using the latest version "
              f"of this script.\nor create an issue at github {bcolors.ENDC}")
        quit()

    if not os.path.exists("witdir"):
        print(f"Extracting archive {bcolors.BLUE}wit.zip{bcolors.ENDC} to {bcolors.BLUE}{os.getcwd()}{bcolors.ENDC}")
        patoolib.extract_archive("wit.zip", outdir=f"{os.getcwd()}\\witdir")
    else:
        print("Executable exists, not extracting...")

    # End of Windows code


if not os.path.exists(modFiles):
    download(modDownload, "mods.7z", modMD5)
    patoolib.extract_archive("mods.7z", outdir=f"{os.getcwd()}/{modFiles}")
else:
    if fileCount(modFiles) != 736:

        download(modDownload, "mods.7z", modMD5)
        patoolib.extract_archive("mods.7z", outdir=f"{os.getcwd()}/{modFiles}")

    else:
        print("Mods are already downloaded, proceeding")

# Extract ISO in linux and windows, not sure this difference is worth the check for linux or windows but eh. it works
if sys.platform.startswith('linux'):

    # Check if ISO folder is already extracted, if not extracts it
    if not os.path.exists(extractedISOFolder):

        print(f"Extracting ISO ({isoPath}) to {extractedISOFolder}")
        os.system(f"witdir/wit-v3.05a-r8638-x86_64/bin/wit extract {isoPath} --dest={extractedISOFolder}")

    else:
        print(f"File path {extractedISOFolder} already exists. try removing it if it doesnt work.\n")

# check for windows and do windows stuff AAAAAAAAAAHHHHHHHHHHHHHHHHHHHHHHHHHHH
elif sys.platform.startswith('win32'):

    # Check if ISO folder is already extracted, if not extracts it
    if not os.path.exists(extractedISOFolder):

        print(f"Extracting ISO ({isoPath}) to {extractedISOFolder}")
        os.system(f"witdir\\wit-v3.05a-r8638-cygwin64\\bin\\wit.exe  extract {isoPath} --dest={extractedISOFolder}")

    else:
        print(f"File path {extractedISOFolder} already exists. try removing it if it doesnt work.\n")

# Create backup of extracted ISO folder since extracting takes a while.
shutil.copytree(extractedISOFolder, moddedISOFolder, dirs_exist_ok=True)

# Generate list of files to KEEP
try:
    os.remove("keepList.txt")
except OSError:
    pass

for filename in listfiles(moddedISOFolder):
    with open("keepList.txt", "a") as keepList:
        keepList.write(filename + "\n")

# Create list object including files to keep via keeplist.txt
listKeep = open("keepList.txt").read().splitlines()

# copy mod files to every path listed in the copyPaths array
for files in copyPaths:
    print(files)
    shutil.copytree(modFiles, f"{moddedISOFolder}/DATA/files/{files}", dirs_exist_ok=True)

# delete files that dont match the keep list
for filename in listfiles(moddedISOFolder):
    print(filename)
    if filename not in listKeep:
        try:
            os.remove(filename)
        except OSError as error:
            print("Cannot delete directory")

# Create ISO file woot woot!
if sys.platform.startswith('linux'):

    os.system(f"witdir/wit-v3.05a-r8638-x86_64/bin/wit copy {moddedISOFolder} modded-{isoPath}.iso")
# check for windows and do windows stuff AAAAAAAAAAHHHHHHHHHHHHHHHHHHHHHHHHHHH
elif sys.platform.startswith('win32'):

    os.system(f"witdir\\wit-v3.05a-r8638-cygwin64\\bin\\wit.exe  copy {moddedISOFolder} modded-{isoPath}.iso")

print(f"Hopefully that worked, if it didnt let me know in a github issue\nhttps://github.com/accuwau/MKWHD-Installer\nOtherwise you should be able to delete everything but\n{isoPath} and modded-{isoPath}")
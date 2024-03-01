#!/bin/bash

input_folder=mkw
output_folder=modded_mkw
mods_directory=modded
wit_download="https://wit.wiimm.de/download/wit-v3.05a-r8638-x86_64.tar.gz"
mod_download="https://files.gamebanana.com/mods/my_2c6e9.7z"
RED='\033[0;31m'
NC='\033[0m'
GREEN='\033[0;32m'
clear


echo -e "${RED}WARNING!!\n${NC}This will install the WIT binary for extracting and combining your mario kart iso.\nYou can simply just delete this file once youre done\nThis will also download the mods from gamebanana\nThe mod is 400Mb and will take a bit of time.\nBoth of these files will be in the directory where this script is\nIf you do not want to continue please press Ctrl+C twice\nOtherwise, press enter :)"
read
#Download WIT to unpack and then repack the iso

if [ -z $(ls wit.tar.gz) ]; then
    curl --output wit.tar.gz $wit_download
fi
tar -xvf wit.tar.gz --strip-components=3 $(tar -tzf wit.tar.gz | grep bin/wit) #Extract the "wit" binary from the archive without any other folders

#End of WIT Download

#Download mod files and unzip them to the mods directory

mkdir $mods_directory
if [ -z $(ls mods.7z) ]; then
    curl --output mods.7z $mod_download
fi

if [ $(ls $mods_directory/ | wc -l) != 736 ]; then
    7za e -y mods.7z -o$mods_directory
fi

#Ask user for mariokart iso

echo -e '\n\nPlease type the path of your Mario Kart ISO \nfor easy use just place the iso directly next to this file \nand write the filename (e.g, mariokart.iso)\n\n'
read isopath 2>/dev/null
echo -e "\n\nSelected file: $isopath"

#A ton of making sure the user doesnt fuck up the path or name

if [ ! -f "$isopath" ]; then
    echo -e "${RED}File does not exist. \n${NC}Please make sure youve typed the path correctly"
    exit
else
    echo -e "${GREEN}File \"$isopath\" exists\ncontinuing${NC}"
fi
if [[ ${isopath,,} != *.iso ]]; then
    echo To make sure this script works correctly please make sure the file ends with .iso
    exit
fi

if [ $(find "$input_folder" | wc -l ) != 2163 ]; then
    echo Extracting ISO
    wit extract $isopath --dest=$input_folder/
else
    echo Not extracting, seems to be already extracted at "$input_folder"
fi

echo Copying extraction to "$output_folder" for working directory
cp -r $input_folder $output_folder

echo Creating file reference list
find $output_folder > nodeletelist.txt

echo Copying modded files to working directory
cp $mods_directory/* $output_folder/DATA/files/sound
cp $mods_directory/* $output_folder/DATA/files/sound/strm
cp $mods_directory/* $output_folder/DATA/files/Race
cp $mods_directory/* $output_folder/DATA/files/Race/Course
cp $mods_directory/* $output_folder/DATA/files/Race/Kart

echo Deleting unneccesary files
find $output_folder | grep -v -x -f nodeletelist.txt | xargs -d "\n" -P 0 rm -f

echo Creating modded ISO
wit copy $output_folder modded.iso

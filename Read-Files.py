import os
from os import path
import time
import datetime
import shutil
import zipfile
from zipfile import ZipFile

print ("This script lists all the contents of the current folder and calculates the total size of the folder in bytes.\n")

print ("If you have already run the script, please remember to delete the folder it creates in order to run the script again.\n")

file_path = os.getcwd()
os.mkdir("results")
Total_size = 0

Listing_Files = open ("results/Files_Contents.txt", "a")
Listing_Files.write("The contents of the current folder are:\n")
Listing_Files.write("---------------------------------------\n")

items = list(os.listdir())
for i in items:
    if path.isfile(i):
        Listing_Files = open ("results/Files_Contents.txt", "a")
        Listing_Files.write(i + "\n")
        file_size = os.path.getsize(file_path)
        Total_size = Total_size + file_size

Listing_Files = open ("results/Files_Contents.txt", "a")
Listing_Files.write("\n")
Listing_Files.write("The total size of the previous files is: " + str(Total_size) + " bytes")
Listing_Files.close()

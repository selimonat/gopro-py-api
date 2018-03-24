#!/home/pi/miniconda3/bin/python3
from goprocam import constants;
from goprocam import GoProCamera;
import time
import subprocess
import os

gpCam = GoProCamera.GoPro(constants.auth);
gpCam.take_photo(1)
time.sleep(2)
gpCam.downloadLastMedia(custom_filename="/home/pi/getvisuals_log/")
print(os.getcwd())
subprocess.Popen(["/home/pi/code/shell/bin/SendLastPic.sh",os.getcwd(), "onatselim@gmail.com"])

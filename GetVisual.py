#!/home/pi/miniconda3/bin/python3
from goprocam import constants;
from goprocam import GoProCamera;
import time
import subprocess

gpCam = GoProCamera.GoPro(constants.auth);
gpCam.take_photo(1)
time.sleep(2)
gpCam.downloadLastMedia() 
subprocess.Popen(["/home/pi/code/shell/bin/SendLastPic.sh", "onatselim@gmail.com"])

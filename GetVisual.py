#!/home/pi/miniconda3/envs/py36/bin/python
from goprocam import constants;
from goprocam import GoProCamera;
import time
import subprocess
import os
import sys

def main():
	sys.path.append(os.path.abspath("/home/pi/code/python/face_recognition/examples/"))
	from find_faces import facefuck
	
	gpCam = GoProCamera.GoPro(constants.auth)
	gpCam.take_photo(1)
	time.sleep(2)
	save_path  = "/home/pi/getvisuals_log/"
	filename   = save_path + str(round(time.time())) + ".jpg"
	gpCam.downloadLastMedia(custom_filename=filename)
	
	
	print("resizing image to 50%")
	subprocess.call(["/usr/bin/convert {} -resize 25% {}".format(filename,filename)],shell=True)
	print("detecting faces in the image with facefuck")
	facefuck(filename)
	print("sending results as an email")
	subprocess.Popen(["/home/pi/code/shell/bin/SendLastPic.sh","/home/pi/getvisuals_log/","'Email sent by GetVisual.py'","Visual from your home", "onatselim@gmail.com"])


if __name__ == "__main__":
    main()
    sys.exit(0)
    

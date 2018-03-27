#!/home/pi/miniconda3/envs/py36/bin/python
from goprocam import constants;
from goprocam import GoProCamera;
import time
import subprocess
import os
import cv2
import numpy as np
import sys

import logging
logging.basicConfig(filename='/home/pi/motion_detection.log',level=logging.DEBUG,format='%(message)s')


def main():
	#open camera and change photo mode to smallest size
	gpCam = GoProCamera.GoPro(constants.auth)
	gpCam.sendCamera(constants.Hero3Commands.PHOTO_RESOLUTION,constants.Hero3Commands.PhotoResolution.PR5MP_W)
	
	save_path = "/home/pi/motion_detection/%s.jpg"
	tmp_path  = "/tmp/%s.jpg"
	
	filename = [None];
	for i in [0, 1]:
		filename.append(tmp_path % (i))
		print("Taking photo %d called %s" % (i, filename[-1]))
		gpCam.take_photo()
		time.sleep(2)
		print("Downloading photo %d" % i)
		gpCam.downloadLastMedia(custom_filename=str(filename[-1]))
		print("Reading photo %d" % i)
		img = np.float32(cv2.imread(filename[-1],cv2.IMREAD_GRAYSCALE))
		if i == 0:
			out = img
		else:
			out = out - img
		time.sleep(10)
	
	print("Computing motion power")
	out = abs(out);
	print("Smoothing motion power")
	out = cv2.GaussianBlur(out,(61,61),25)
	#out = out/np.amax(out)
	#out = out*255
	print("Saving diff image")
	filename.append(save_path % (str(round(time.time()))))
	cv2.imwrite(filename[-1],np.uint8(out),[int(cv2.IMWRITE_JPEG_QUALITY), 10])
	
	motion_power = np.mean(out)
	print("Motion Value: %s" % (motion_power))
    
	out = str(motion_power) + " " + str(time.strftime("%a %d %b %H:%M:%S CET %Y")) + " " + str(round(time.time()))
	
	logging.info(out)
	print("Montage collected data")
	cmd = "montage %s %s %s -geometry +1+3 %s" % (filename[1],filename[2],filename[3],filename[3])
	print(cmd)

	#print("sending results as an email")
	subprocess.Popen(["/home/pi/code/shell/bin/SendLastPic.sh","/home/pi/motion_detection/","Motion value: " + str(motion_power),"Motion Detection Report","onatselim@gmail.com"])    
	return motion_power

if __name__ == "__main__":
	main()
	sys.exit(0)

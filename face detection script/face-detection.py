# imports 
import serial
import os
import cv2
import sys
import picamera
import subprocess
import sched, time

# global vars
scriptDir = "/home/pi/fhp/io/"

imageFaceDetectionPath = scriptDir + "image-processed.jpg"
imagePath = scriptDir + "image.jpg"
cascPath = scriptDir + "haarcascade.xml"

refreshTime = 0.5
resolution = ( 320, 240 )
camera = picamera.PiCamera()
camera.resolution = resolution
camera.hflip = True;
faceCascade = cv2.CascadeClassifier( cascPath )

serial = serial.Serial('/dev/ttyACM0', 9600)


# defs
def faceDetection () :
	camera.capture( imagePath )

	# Read the image
	image = cv2.imread( imagePath )
	gray = cv2.cvtColor( image, cv2.COLOR_BGR2GRAY )

	# Detect faces in the image
	faces = faceCascade.detectMultiScale (
	    gray,
	    scaleFactor = 1.1,
	    minNeighbors = 5,
	    minSize = ( 30, 30 ),
	    flags = cv2.cv.CV_HAAR_SCALE_IMAGE
	)

	for ( x, y, w, h ) in faces:
		centerX = x + ( w / 2 )
		centerY = y + ( h / 2 )

		print "Found face at: {0}, {0}".format( centerX, centerY )
		serial.write( "{0}, {0}".format( centerX, centerY ) );

		cv2.rectangle( image, ( x, y ), ( x + w, y + h ), ( 0, 255, 0), 3 )
		cv2.imwrite( imageFaceDetectionPath, image )

		break
  	
  	# recall fn
  	interval.enter( refreshTime, 1, faceDetection, () )


# init interval
interval = sched.scheduler( time.time, time.sleep )
interval.enter( refreshTime, 1, faceDetection, () )
interval.run()
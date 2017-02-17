
from picamera import PiCamera
from time import sleep

camera = PiCamera()

camera.start_preview()
sleep(30)
camera.capture('./capturedImage/image.jpg')
camera.stop_preview()

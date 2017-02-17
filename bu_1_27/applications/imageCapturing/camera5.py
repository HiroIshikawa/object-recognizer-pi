from picamera import PiCamera
from time import sleep

camera = PiCamera()

for i in range(5):
    camera.start_preview()
    sleep(1)
    camera.capture('./capturedImage5/'+str(i)+'image.jpg')
    camera.stop_preview()

#opens up a webcam feed so you can then test your classifer in real time
#using detectMultiScale
from sys import argv
import cv2
import numpy as np
import time
import threading

from picamera.array import PiRGBArray
from picamera import PiCamera

obj_w = int(argv[1])
obj_h = int(argv[2])
scale_factor = float(argv[3])
min_neighs = int(argv[4])
# win_w = int(argv[5])
win_w = 320
# win_h = int(argv[6])
win_h = 240

def region_of_interest(img, vertices):
    """
    Applies an image mask.
    
    Only keeps the region of the image defined by the polygon
    formed from `vertices`. The rest of the image is set to black.
    """
    
    #defining a blank mask to start with
    mask = np.zeros_like(img)   
    
    #defining a 3 channel or 1 channel color to fill the mask with depending on the input image
    if len(img.shape) > 2:
        channel_count = img.shape[2]  # i.e. 3 or 4 depending on your image
        ignore_mask_color = (255,) * channel_count
    else:
        ignore_mask_color = 255
        
    #filling pixels inside the polygon defined by "vertices" with the fill color    
    cv2.fillPoly(mask, vertices, ignore_mask_color)
    
    #returning the image only where mask pixels are nonzero
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image

def detect(img):
    """
    Detects objects that matches with cascade classifiers.

    The regions of target object detected get covered by 
    rectangles. Each rect data contains: (x1, y1, x2, y2)
    """
# The version for the multiple cascades
# def detect(cascade_list, img):
    # # Read width and height of a cascade from cascade.xml
    # for cascade in enumarate(cascade_list):
    # for cascade in enumerate(glob.iglob('./cascades/*.xml')):
    #   root = xml.etree.ElementTree.parse(cascade).getroot()
    #   width = root[0][3].text
    #   height = root[0][2].text
    #   cur_rects = cascade.detectMultiScale(img, 1.1, 1, cv2.cv.CV_HAAR_SCALE_IMAGE, (width,height))
    #   for rect in cur_rects:
    #       total_rects.append(rect)
    #   total_rects.append(cur_rects[0])
    cascade = cv2.CascadeClassifier("cascade.xml")
    rects = cascade.detectMultiScale(img, scale_factor, min_neighs, cv2.CASCADE_SCALE_IMAGE, (obj_w,obj_h))

    if len(rects) == 0:
        return [], img
    rects[:, 2:] += rects[:, :2]
    return rects, img

def box(rects, img):
    """
    Draws box around the detected objects.

    The color and thickness of the line of box 
    can be changed with the cv2.rectangle arguments.
    """
    for x1, y1, x2, y2 in rects:
        cv2.rectangle(img, (x1, y1), (x2, y2), (127, 255, 0), 2)
    return img
    # cv2.imwrite('one.jpg', img);

def centering_img(img):
    """
    Calculate the center of image in (x,y).
    
    """
    height, width, channels = img.shape
    center_x = width/2
    center_y = height/2
    # print('center of image, x: '+str(center_x))
    # print('center of image, y: '+str(center_y))
    return (center_x, center_y)

def sizing_box(rect):
    """
    Calculate the size of box.
    
    """
    box_width = abs(rect[0] - rect[2])
    box_height = abs(rect[1] - rect[3])
    # print('width of box: '+str(box_width))
    # print('height of box: '+str(box_height))
    return (box_width, box_height)

def centering_box(rect):
    """
    Calculate the (x,y) of the center of a box in the iamge.

    """
    box_x = abs(rect[0] - rect[2])/2 + rect[0]
    box_y = abs(rect[1] - rect[3])/2 + rect[1]
    # print('x of object: '+str(box_x))
    # print('y of object: '+str(box_y))
    return (box_x, box_y)

def pos_from_center(img_center, box_center):
    """
    Calcualte the relative position of the object

    
    """
    box_rel_x = box_center[0]-img_center[0]
    box_rel_y = box_center[1]-img_center[1]
    # print('position of box to x: '+str(box_rel_x))
    # print('position of box to y: '+str(box_rel_y))
    return (box_rel_x, box_rel_y)

def mean(l):
    if len(l)==0:
        return 0.0
    return sum(l)/len(l)

def navigate(candidates):
    threading.Timer(0.5, navigate, args=[candidates]).start()
    # avg_pos = reduce(lambda x, y: x + y, candidates) / len(candidates)
    avg_pos = mean(candidates)
    candidates[:] = []
    if (avg_pos > 0):
        print("Turn Right: Rotate "+str(avg_pos)+" units")
    elif (avg_pos < 0):
        print("Turn Left: Rorate "+str(avg_pos)+" units")
    else:
        print("Go Straight")
    # print("Navigation: "+str(avg_pos)+" units")
    # return True

def record(recording):
    threading.Timer(1, record, args=[recording]).start()
    cv2.imwrite("./recording/record.jpg",recording[0])

# Start capturing
# cap = cv2.VideoCapture(0)
# cap.set(3,win_w)
# cap.set(4,win_h)


# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (win_w, win_h)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(win_w, win_h))

# allow the camera to warmup
time.sleep(0.1)

# initialize the nvagation system for different position
candidates = []
navigate(candidates)

# numpy array to temporaly store the current working image
# this used to recording some images while processing
# recording = []
# ret, init_image = cap.read()
# recording.append(init_image)
# record(recording)

#recording = []
#with PiCamera.array.PiRGBArray(camera) as stream:
#camera.capture(rawCapture, format='bgr')
    # At this point the image is available as stream.array
#    init_image = stream.array
#print(init_image)
#recording.append(init_image)
#record(recording)

recording = []
init_rawCapture = PiRGBArray(camera, size=(win_w, win_h))
recording.append(init_rawCapture.array)
record(recording)

# while(True):
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # grab the raw NumPy array representing the image, then initialize the timestamp
    # and occupied/unoccupied text
    img = frame.array
    # ret, img = cap.read()
    imshape = img.shape
    vertices = np.array([[(0,imshape[0]),(0,int(imshape[0]/2)), 
        (int(imshape[1]),int(imshape[0]/2)), (imshape[1],imshape[0])]], dtype=np.int32)
#    cv2.imshow("frame1", img)
    img = region_of_interest(img, vertices)

    rects, img = detect(img)
    img = box(rects, img)

    flag = False

    # Get the coordinate of the center of the image
    img_center = centering_img(img)

    # Get the stats of the each box
    num_boxes = len(rects)
    boxes = []
    for k in range(num_boxes):
        boxes.append({'box_id':0,'box_size': (0,0),'box_center':(0,0),'box_to_center':(0,0)})

    for i, rect in enumerate(rects):
        # Record box id
        boxes[i]['box_id'] = i
        # Get the size of the box
        box_size = sizing_box(rect)
        boxes[i]['box_size'] = box_size
        # Get the coordinate of the center of box
        box_center = centering_box(rect)
        boxes[i]['box_center'] = box_center
        # Get the relative positon of the box to the center of image
        box_to_center = pos_from_center(img_center, box_center)
        boxes[i]['box_to_center'] = box_to_center

    # for box in boxes:
    #     print(box)
    # for each box, find the best one to approach 
    if (boxes):
        # elminate the boxes that above the horizon


        # find the box having the maximum size
        maxSizeItem = max(boxes, key=lambda x:x['box_size'][0]*x['box_size'][1])

        # if (maxSizeItem['box_to_center'][0] > 0):
        #     # print("Turn Right: Rotate "+str(maxSizeItem['box_to_center'][0])+" units")
        # elif (maxSizeItem['box_to_center'][0] < 0):
        #     # print("Turn Left: Rorate "+str(maxSizeItem['box_to_center'][0])+" units")
        # else:
        #     # print("Go Straight")
        
        # print("The item which has max size: "+str(maxSizeItem))

        candidates.append(maxSizeItem['box_to_center'][0])

    recording[0] = img

    rawCapture.truncate(0)

 #   cv2.imshow("frame", img)
    if(cv2.waitKey(1) & 0xFF == ord('q')):
	   break

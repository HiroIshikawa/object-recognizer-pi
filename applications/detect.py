import cv2
from preprocess import *
from measure import *

# def detect(img, scale_factor, min_neighs, obj_w, obj_h):
def detect(img, cas_params):
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
    # rects = cascade.detectMultiScale(img, scale_factor, min_neighs, cv2.CASCADE_SCALE_IMAGE, (obj_w,obj_h))
    rects = cascade.detectMultiScale(img, cas_params[0], cas_params[1], cv2.CASCADE_SCALE_IMAGE, (cas_params[2],cas_params[3]))

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

def wc_detection_system(cap,cas_params):
    print("In Auto Detection System for Webcamera..")
    while(True):
        ret, raw_img = cap.read()
        imshape = raw_img.shape
        vertices = np.array([[(0,imshape[0]),(0,int(imshape[0]/2)), 
            (int(imshape[1]),int(imshape[0]/2)), (imshape[1],imshape[0])]], dtype=np.int32)
        processed_img = region_of_interest(raw_img, vertices)
        rects, detected_img = detect(processed_img, cas_params)
        g.img = box(rects, detected_img)
        measure(raw_img, rects)

def pi_detection_system(camera,rawCapture,cas_params):
    print("In Auto Detction System for PiCamera...")
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        flag = False
        raw_img = frame.array
        # cv2.imshow("Raw", img)
        # img = preprocess(img)
        # cv2.imshow("Preprocessed", img)
        rects, detected_img = detect(raw_img, cas_params)
        g.img = box(rects, detected_img)
    #    cv2.imshow("Cascaded", img)
        measure(raw_img, rects)

        # if there's no rects found, look around
        # if not rects:
        #     look_around() 
            # Check time elapsed, if over 10 sec, invoke spiral search
            # if (time.time()-start) > 10:
            #     spiral_search()

        rawCapture.truncate(0)
        if(cv2.waitKey(1) & 0xFF == ord('q')):
           break

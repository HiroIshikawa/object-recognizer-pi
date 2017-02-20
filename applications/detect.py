import cv2

def detect(img, scale_factor, min_neighs, obj_w, obj_h):
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
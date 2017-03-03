def centering_img(img):
    """Calculate the center of image in (x,y)."""
    height, width, channels = img.shape
    center_x = width/2
    center_y = height/2
    # print('center of image, x: '+str(center_x))
    # print('center of image, y: '+str(center_y))
    return (center_x, center_y)

def sizing_box(rect):
    """Calculate the size of box."""
    box_width = abs(rect[0] - rect[2])
    box_height = abs(rect[1] - rect[3])
    # print('width of box: '+str(box_width))
    # print('height of box: '+str(box_height))
    return (box_width, box_height)

def centering_box(rect):
    """Calculate the (x,y) of the center of a box in the iamge."""
    box_x = abs(rect[0] - rect[2])/2 + rect[0]
    box_y = abs(rect[1] - rect[3])/2 + rect[1]
    # print('x of object: '+str(box_x))
    # print('y of object: '+str(box_y))
    return (box_x, box_y)

def pos_from_center(img_center, box_center):
    """Calcualte the relative position of the object"""
    box_rel_x = box_center[0]-img_center[0]
    box_rel_y = box_center[1]-img_center[1]
    # print('position of box to x: '+str(box_rel_x))
    # print('position of box to y: '+str(box_rel_y))
    return (box_rel_x, box_rel_y)

def measure(img, rects, candidates):
    """
    Measure the object location.

    Put an object with maximam size detected in a
    video frame (since cascade may detect more than
    one) into candidate list, which is examined
    regularly to initiate a command to arduino.
    """
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

    if (boxes):
        # find the box having the maximum size
        maxSizeItem = max(boxes, key=lambda x:x['box_size'][0]*x['box_size'][1])
        candidates.append(maxSizeItem['box_to_center'][0])

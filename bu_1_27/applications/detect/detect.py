import cv2
import glob
import sys
import xml.etree.ElementTree


# Get user supplied values
# Testing purpose
# imagePath = sys.argv[1]
# cascPath = sys.argv[2]

# cascades folder should contain the all cascade applied

# 5 Cascades
# 1. Straight up (20x40) ### Test Case
# 2. Laying down parallel (40x20)
# 3. Laying down 45 deg (40x40)
# 4. laying down 0 deg (20x30)
# 5. laying down 180 deg (20x30)

# Voting strategy to find a optimal box to approach
# 1. the bigger box -> the clooser
# 2. the more box in one area -> higher possibility of object
# 3. smaller relative range to the center -> less roration required

# Take an image every n seconds
# Analyse the image to position objects
# If found, stop taking images until finishing approaching to object procedure
# Pick an object to approach in the objects detected in the voting strategy
# (Can we machine learn this process?? : deifne "states, action, rewards, and policy")
# Send relative units to rotate to controller unit
# Should have mechanical strategy to avoid stuck in a situation
# * after n attempts, should conduct random walk
# Get back signal of completion of approach attempt
# Loop over taking an image

# We should setup min/max thresholds of box size 
# to register it as a candidate of the voting process

# False negatives <- random walk
# False positives <- cap, averaging multiple images
# *** solution should largely done by making the cascade better though
# *** mastering cascade training

# Helping the robot to navigate to things?
# "Trasing mode": given a particular object, it start follows the particular signiture
# (We should not pick up gaverage from ground)

# Detect objects maching with a given cascade
def detect(cascade, img):
# def detect(cascade_list, img):
	# # Read width and height of a cascade from cascade.xml
	# for cascade in enumarate(cascade_list):
	# for cascade in enumerate(glob.iglob('./cascades/*.xml')):
	#	root = xml.etree.ElementTree.parse(cascade).getroot()
	#	width = root[0][3].text
	#	height = root[0][2].text
	#	cur_rects = cascade.detectMultiScale(img, 1.1, 1, cv2.cv.CV_HAAR_SCALE_IMAGE, (width,height))
	#	for rect in cur_rects:
	#		total_rects.append(rect)
	#	total_rects.append(cur_rects[0])
    rects = cascade.detectMultiScale(img, 1.1, 1, cv2.CASCADE_SCALE_IMAGE, (20,40))

    if len(rects) == 0:
    	print("Could'nt find any")
        return [], img
    rects[:, 2:] += rects[:, :2]
    # total_rects[:, 2:] += total_rects[:, :2]
    # print(rects)
    # print(total_rects)
    return rects, img
    # return total_rects, img

# Draw box around each object dected
def boxing(rects, key, img):
    for x1, y1, x2, y2 in rects:
        cv2.rectangle(img, (x1, y1), (x2, y2), (127, 255, 0), 2)
    cv2.imwrite('labeled/'+str(key)+'.jpg', img);

# Get the center of image
def centering_img(img):
	height, width, channels = img.shape
	center_x = width/2
	center_y = height/2
	# print('center of image, x: '+str(center_x))
	# print('center of image, y: '+str(center_y))
	return (center_x, center_y)

# Get the size of a box
def sizing_box(rect):
	box_width = abs(rect[0] - rect[2])
	box_height = abs(rect[1] - rect[3])
	# print('width of box: '+str(box_width))
	# print('height of box: '+str(box_height))
	return (box_width, box_height)

# Get the coordinate of the center of a box in the image
def centering_box(rect):
	box_x = abs(rect[0] - rect[2])/2 + rect[0]
	box_y = abs(rect[1] - rect[3])/2 + rect[1]
	# print('x of object: '+str(box_x))
	# print('y of object: '+str(box_y))
	return (box_x, box_y)

# Get the relative postion of the box to the center of the image
def pos_from_center(img_center, box_center):
	box_rel_x = box_center[0]-img_center[0]
	box_rel_y = box_center[1]-img_center[1]
	# print('position of box to x: '+str(box_rel_x))
	# print('position of box to y: '+str(box_rel_y))
	return (box_rel_x, box_rel_y)

# Normalize the relative position to the size

# Create the haar cascade
# temporal
cascPath = 'cascades/cascade.xml' #temporal implementation for test
cascade = cv2.CascadeClassifier(cascPath)

# for imagePath
for (i, imagePath) in enumerate(glob.iglob('feeds/*.jpg')):
	print(str(i)+'.jpg')

	# Read the image
	image = cv2.imread(imagePath)

	# Detect objects matching with given cascade
	rects, img = detect(cascade, image)

	# Box around detected object
	boxing(rects, i, img)

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

	for box in boxes:
		print(box)

	# Voting
	# Weights for each property
	# Normalize each points first and multiply pre-weights

	# The optimal box and its relative x-coordinate to approach

	print('')

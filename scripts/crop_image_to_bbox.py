## crop screenshot
from PIL import Image
import cv2
import numpy as np

def crop_image(image_path):
	img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

	white = [255, 255, 255, 255]
	transparent = [0, 0, 0, 0]
	height = len(img)
	width = len(img[0])

	##find lower-left corner
	lower_left = []
	for i in range(height-1, -1, -1):
	  for j in range(0, width):
	    
	    if np.array_equal(img[i][j], white):
	      lower_left = [i, j]
	      break
	  if len(lower_left) is not 0:
	    break

	##find upper_right corner
	lower_right = []
	for i in range(height-1, -1, -1):
	  for j in range(width-1, -1, -1):
	    if np.array_equal(img[i][j], white):
	      lower_right = [i, j]
	      break
	  if len(lower_right) is not 0:
	    break

	##arbitrary number - approximately 13 pixels away from the first white point we find from the bottom left 
	box_height = 0;
	box_width = lower_right[1] - lower_left[1]

	upper_right = []
	for i in range(lower_right[0], -1, -1):
	  if np.array_equal(img[i][lower_right[1]], transparent):
	    upper_right = [i+1, lower_right[1]]
	    break

	upper_left = [upper_right[0], lower_left[1]]

	cropped_image = img[upper_left[0]:lower_left[0], upper_left[1]:upper_right[1], :]

	im = Image.fromarray(cropped_image)
 	im.save('cropped.png')
import numpy as np
import matplotlib.pyplot as plt
import cv2
from utils import *
import pytesseract

# Image
img_path = 'imgs/1.jpg'
img_original = cv2.imread(img_path)[:, :, ::-1]
width, height = 450, 450
img = cv2.resize(img_original, (width, height))

# Image preprocessing
img_threshold = pre_processing1(img)
plt.figure(), plt.imshow(img_threshold, cmap='gray')

# Contours
contours, img_contours = all_contours(img_threshold, img)  # all contours
sudoku_contour, points = right_contour_(contours)  # sudoku contour
img_sudoku_contours = img.copy()
img_points = img.copy()
cv2.drawContours(img_sudoku_contours, sudoku_contour, -1, 255, 2)
cv2.drawContours(img_points, points, -1, 255, 15)

# Visualization
img_stack_contours = np.hstack((img, img_contours, img_sudoku_contours, img_points))
plt.figure(), plt.imshow(img_stack_contours)

# WarpPerspective
pts1 = np.float32(reorder_points(points))
pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
matrix = cv2.getPerspectiveTransform(pts1, pts2)
img_warp = cv2.warpPerspective(img, matrix, (width, height))
img_warp_gray = cv2.cvtColor(img_warp, cv2.COLOR_RGB2GRAY)
plt.figure(), plt.imshow(img_warp)
plt.figure(), plt.imshow(img_warp_gray, cmap='gray')

# Split numbers
numbers_box = split_box_numbers(img_warp_gray)

#!/usr/bin/python3

import sys
import cv2

from geo import *

def load_img(filename):
	return cv2.imread(filename, 0)

def show_img(img):
	cv2.imshow("image", img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()


def create_tri(img, output_width, output_height, layer = 4, thickness = 2):
	height = img.shape[0]
	width = img.shape[1]
	
	v1 = []
	v2 = []

	geometry = GEO()
	# top
	for i in range(height):
		v1 = []
		v2 = []
		for j in range(width):
			v1.append((j * output_width / width, 
				i * output_height / height, 
				(255 - img[i, j]) * layer / 255 + thickness))
			v2.append((j * output_width / width, 
				(i+1) * output_height / height, 
				(255 - img[i, j]) * layer / 255 + thickness))
		geometry.quad(v1, v2)
	
	# side width
	v1 = []
	v2 = []
	for i in range(width):
	  v1.append((i * output_width / width, 
		0 * output_height / height, 
		(255 - img[0, i]) * layer / 255 + thickness))
	  v2.append((i * output_width / width, 
		0 * output_height / height, 
		0))
	geometry.quad(v1, v2)

	v1 = []
	v2 = []
	for i in range(width):
	  v1.append((i * output_width / width, 
		(height-1) * output_height / height, 
		(255 - img[height-1, i]) * layer / 255 + thickness))
	  v2.append((i * output_width / width, 
		(height-1) * output_height / height, 
		0))
	geometry.quad(v1, v2)

	# side height
	v1 = []
	v2 = []
	for i in range(height):
	  v1.append((0 * output_width / width, 
		i * output_height / height, 
		(255 - img[i, 0]) * layer / 255 + thickness))
	  v2.append((0 * output_width / width, 
		i * output_height / height, 
		0))
	geometry.quad(v1, v2)

	v1 = []
	v2 = []
	for i in range(height):
	  v1.append(((width-1) * output_width / width, 
		i * output_height / height, 
		(255 - img[i, width-1]) * layer / 255 + thickness))
	  v2.append(((width-1) * output_width / width, 
		i * output_height / height, 
		0))
	geometry.quad(v1, v2)

	# bottom
	v1 = []
	v2 = []
	v1.append((0 * output_width / width, 0 * output_height / height, 0))
	v2.append((0 * output_width / width, (height-1) * output_height / height, 0))
	v1.append(((width-1) * output_width / width, 0 * output_height / height, 0))
	v2.append(((width-1) * output_width / width, (height-1) * output_height / height, 0))
	geometry.quad(v1, v2)

	return geometry

def save_xyz(points, filename = 'litophane.xyz'):
	with open(filename, 'w') as fd:
		for p in points:
			fd.write(' '.join([str(p[0]), str(p[1]), str(p[2])]) + '\n')

def resize_img(img, width, height):
	return cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)

if __name__ == '__main__':
	l = len(sys.argv)

	filename = 'tencent.png'
	if l == 1:
		print ("Usage: python3 main.py [filename] [width] [height]")
	else:
		filename = sys.argv[1]

	img = load_img(filename)
	original_width = img.shape[1]
	original_height = img.shape[0]

	scale_width = int(sys.argv[2] if l >= 3 else original_width)
	scale_height = int(sys.argv[3] if l >= 4 else (original_height * scale_width / original_width))

	img = resize_img(img, scale_width, scale_height)
	show_img(img)

	geometry = create_tri(img, scale_width, scale_height)
	print (geometry)
	
	geometry.save_stl('litophane.stl')

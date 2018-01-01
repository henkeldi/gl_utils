# -*- coding: utf-8 -*-

import numpy as np

from OpenGL.GL import *


def build_image(path):
	import cv2
	img = cv2.imread(path)
	img = np.flipud(img)
	img = np.ascontiguousarray(img)
	return img


def build_texture_from_image(img):
	from texture import Texture
	height, width = img.shape[:2]
	tex = Texture(GL_TEXTURE_2D, 1, GL_RGB8, width, height)

	tex.sub_image(0, 0, 0, width, height, GL_BGR, GL_UNSIGNED_BYTE, img)	
	return tex


def build_texture(path):
	img = build_image(path)
	return build_texture_from_image(img)


def build_textures(paths):
	if not isinstance(paths, list):
		paths = [paths]
	return (build_texture(path) for path in paths)


def build_texture_buffer(*textures):
	from buffer import Buffer
	handles = [t.make_resident() for t in textures]
	return Buffer( np.array(handles, dtype=np.uint64) )


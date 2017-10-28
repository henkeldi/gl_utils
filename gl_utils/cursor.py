# -*- coding: utf-8 -*-

import numpy as np
from PIL import Image

import cyglfw3 as glfw

def create_cursor_from_pixels(pixels, W, H):
    image = glfw.Image()
    im = 255*np.ones( (H,W,4), dtype=np.uint8)
    im[:,:,:pixels.shape[2]] = pixels
    image.pixels = im
    return glfw.CreateCursor(image, W/2, H/2)
	
def create_cursor(icon_path, W, H):
    pixels = Image.open(icon_path)
    pixels = np.array(pixels.resize((W, H), Image.ANTIALIAS))
    return create_cursor_from_pixels(pixels, W, H)
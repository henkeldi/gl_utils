# -*- coding: utf-8 -*-
import numpy as np

from OpenGL.GL import *
from OpenGL.GL.NV.bindless_texture import *

class Texture(object):


    def __init__(self, target, levels, internalformat, width, height):
        self._id = np.empty(1, dtype=np.uint32)
        glCreateTextures(target, len(self._id), self._id)
        glTextureStorage2D(self._id, levels, internalformat, width, height)


    def set_filter(self, min_filter, mag_filter):
        glTextureParameteri(self._id, GL_TEXTURE_MIN_FILTER, min_filter)
        glTextureParameteri(self._id, GL_TEXTURE_MAG_FILTER, mag_filter)


    def set_wrap(self, wrap_s, wrap_t=None, wrap_r=None):
        glTextureParameteri(self._id, GL_TEXTURE_WRAP_S, wrap_s)
        if wrap_t != None:
            glTextureParameteri(self._id, GL_TEXTURE_WRAP_T, wrap_t)
        if wrap_r != None:
            glTextureParameteri(self._id, GL_TEXTURE_WRAP_R, wrap_r)


    def sub_image(self, level, 
        xoffset, yoffset, 
        width, height,
        data_format, data_type, pixels):

        glTextureSubImage2D(self._id, level,
            xoffset, yoffset, 
            width, height, 
            data_format, data_type, pixels)


    def generate_mipmap(self):
        glGenerateTextureMipmap(self._id)


    def make_resident(self):
        self._handle = glGetTextureHandleNV(self._id[0])
        glMakeTextureHandleResidentNV(self._handle)
        return self._handle


    def make_nonresident(self):
        if hasattr(self, '_handle'):
            glMakeTextureHandleNonResidentNV(self._handle)


    def delete(self):
        self.make_nonresident()
        glDeleteTextures(1, self._id)


    @property
    def id(self):
        return self._id[0]



class Texture1D(Texture):


    def __init__(self, levels, internalformat, width):
        self._id = np.empty(1, dtype=np.uint32)
        glCreateTextures(GL_TEXTURE_1D, len(self._id), self._id)
        glTextureStorage1D(self._id, levels, internalformat, width)


    def sub_image(self, level, 
        xoffset, width, 
        data_format, data_type, pixels):
        
        glTextureSubImage1D(
            self._id,
            level,
            xoffset, width,
            data_format, data_type, pixels
        )



class Texture3D(Texture):


    def __init__(self, target, levels, internalformat, width, height, depth):
        self._id = np.empty(1, dtype=np.uint32)
        glCreateTextures(target, len(self._id), self._id)
        glTextureStorage3D(self._id, levels, internalformat, width, height, depth)


    def sub_image(self, level, 
        xoffset, yoffset, zoffset, 
        width, height, depth,
        data_format, data_type, pixels):
        
        glTextureSubImage3D(self._id, level, 
            xoffset, yoffset, zoffset,
            width, height, depth, 
            data_format, data_type, pixels
        )


class TextureMultisample(Texture):



    def __init__(self, samples, internalformat, width, height, fixedsamplelocations):
        self._id = np.empty(1, dtype=np.uint32)
        glCreateTextures(GL_TEXTURE_2D_MULTISAMPLE, len(self._id), self._id)
        glTextureStorage2DMultisample(self._id, samples, internalformat, width, height, fixedsamplelocations)



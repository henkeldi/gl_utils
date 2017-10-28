# -*- coding: utf-8 -*-
import numpy as np

from OpenGL.GL import *

class Renderbuffer(object):

    def __init__(self, internalformat, width, height):
        self._id = np.empty(1, dtype=np.uint32)
        glCreateRenderbuffers(len(self._id), self._id)
        glNamedRenderbufferStorage(self._id, internalformat, width, height)


    def delete(self):
        glDeleteRenderbuffers(1, self._id)


    @property
    def id(self):
        return self._id[0]


class RenderbufferMultisample(Renderbuffer):


    def __init__(self, samples, internalformat, width, height):
        self._id = np.empty(1, dtype=np.uint32)
        glCreateRenderbuffers(len(self._id), self._id)
        glNamedRenderbufferStorageMultisample(self._id, samples, internalformat, width, height)

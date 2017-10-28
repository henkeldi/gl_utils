# -*- coding: utf-8 -*-

import numpy as np

from OpenGL.GL import *

class Buffer(object):


    def __init__(self, data, flags=0):
        self._id = np.empty(1, dtype=np.uint32)
        glCreateBuffers(len(self._id), self._id)
        self._size = data.nbytes
        glNamedBufferStorage(self._id, self._size, data, flags)


    def bind(self, target):
        glBindBuffer(target, self._id)


    def bind_range(self, target, index, offset=0, size=None):
        size = self._size if size == None else size
        glBindBufferRange(target, index, self._id, offset, size)


    def map_range(self, offset, length, access):
        ptr = glMapNamedBufferRange(
            self._id,
            offset,
            length,
            access
        )
        return ptr


    def sub_data(self, offset, nbytes, data):
        glNamedBufferSubData(self._id, offset, nbytes, data)


    def delete(self):
        glDeleteBuffers(self._id, 1)


    @property
    def id(self):
        return self._id
# -*- coding: utf-8 -*-
import numpy as np

from OpenGL.GL import *


class VAO(object):


    def __init__(self, vbo_attrib, ebo=None):
        self._id = np.empty(1, dtype=np.uint32)
        glCreateVertexArrays(len(self._id), self._id)

        for i, ((vbo, offset, stride), attribs) in enumerate(vbo_attrib.iteritems()):
            for attribindex, size, attribtype, normalized, relativeoffset in attribs:
                glVertexArrayAttribFormat(self._id, attribindex, size, attribtype, normalized, relativeoffset)
                glVertexArrayAttribBinding(self._id, attribindex, i)
                glEnableVertexArrayAttrib(self._id, attribindex)
            glVertexArrayVertexBuffer(self._id, i, vbo.id, offset, stride)
        
        if ebo != None:
            glVertexArrayElementBuffer(self._id, ebo.id)


    def bind(self):
        glBindVertexArray(self._id)
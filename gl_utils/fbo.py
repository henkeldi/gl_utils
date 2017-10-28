# -*- coding: utf-8 -*-
import numpy as np

from OpenGL.GL import *

from texture import Texture
from renderbuffer import Renderbuffer

class Framebuffer(object):


    def __init__(self, attachements):
        self._id = np.empty(1, dtype=np.uint32)
        glCreateFramebuffers(len(self._id), self._id)
        for k in attachements.keys():
            attachement = attachements[k]
            if issubclass(attachement.__class__, Renderbuffer):
                glNamedFramebufferRenderbuffer(self._id, k, GL_RENDERBUFFER, attachement.id)
            elif issubclass(attachement.__class__, Texture):
                glNamedFramebufferTexture(self._id, k, attachement.id, 0)
            else:
                raise ValueError('Unknown frambuffer attachement class: {}'.format(attachement))

        if glCheckNamedFramebufferStatus(self._id, GL_FRAMEBUFFER) != GL_FRAMEBUFFER_COMPLETE:
            raise RuntimeError('Framebuffer not complete.')
        self.__attachements = attachements


    def bind(self):
        glBindFramebuffer(GL_FRAMEBUFFER, self._id)


    def delete(self):
        glDeleteFramebuffers(1, self._id)
        for k in self.__attachements.keys():
            self.__attachements[k].delete()


    @property
    def id(self):
        return self._id[0]
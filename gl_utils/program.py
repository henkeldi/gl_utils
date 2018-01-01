# -*- coding: utf-8 -*-
import os
import logging as log

from OpenGL.GL import *

class Program(object):

    shader_type_lookup =\
    {
        'vs': GL_VERTEX_SHADER,
        'tcs': GL_TESS_CONTROL_SHADER, 
        'tes': GL_TESS_EVALUATION_SHADER, 
        'gs' : GL_GEOMETRY_SHADER, 
        'frag': GL_FRAGMENT_SHADER, 
        'cs': GL_COMPUTE_SHADER
    }

    shader_folder = None


    def __init__(self, *shader_paths):
        self._shader_paths = shader_paths


    def compile_and_use(self):
        self.compile()
        self.use()


    def compile(self):
        self.__program = glCreateProgram()
        shaders = []
        for path in self._shader_paths:
            if Program.shader_folder != None:
                path = os.path.join(Program.shader_folder, path)
            shader = Program.__create_shader__(path)
            glAttachShader(self.__program, shader)
            shaders.append(shader)

        glLinkProgram(self.__program)
        if not glGetProgramiv(self.__program, GL_LINK_STATUS):
            log.error('\033[31m'+glGetProgramInfoLog(self.__program)+'\033[39m')
            raise RuntimeError('Shader linking failed')
        else:
            log.debug('Shader linked.')

        for shader in shaders:
            glDeleteShader(shader)


    @staticmethod
    def __create_shader__(path):
        suffix = path[path.rindex('.')+1:]
        shader_type = Program.shader_type_lookup[suffix]
        shader = glCreateShader(shader_type)
        with open(path, 'r') as f:
            code = f.read()
            glShaderSource(shader, code)
        glCompileShader(shader)
        if not glGetShaderiv(shader, GL_COMPILE_STATUS):
            log.error('\033[31m'+glGetShaderInfoLog(shader)+'\033[39m')
            raise RuntimeError('[\033[32m{}\033[39m]: Shader compilation failed!'.format(path) )
        else:
            log.debug('Shader compiled (%s).', path)
        return shader


    def delete(self):
        glDeleteProgram(self.__program)


    def use(self):
        glUseProgram(self.__program)


    @property
    def id(self):
        return self.__program


class InteractiveProgram(Program):

    def __init__(self, *shader_paths):
        self._shader_paths = shader_paths
        self.init()
        super(InteractiveProgram, self).__init__(*shader_paths)

    def update(self):
        if any([os.stat(p)[8] != t for p, t in zip(self._full_shader_paths, self._shader_last_modified_timestamp)]):
            self.init()
            try:
                self.compile_and_use()
                self.delete()
            except RuntimeError as e:
                pass
            print 'Recompiled shader!'

    def init(self):
        self._full_shader_paths = []
        self._shader_last_modified_timestamp = []
        for path in self._shader_paths:
            if Program.shader_folder != None:
                path = os.path.join(Program.shader_folder, path)
            self._shader_last_modified_timestamp.append( os.stat(path)[8] )
            self._full_shader_paths.append(path)       
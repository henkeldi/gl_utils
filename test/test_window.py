# -*- coding: utf-8 -*-

import numpy as np

import cyglfw3 as glfw
from OpenGL.GL import *

import gl_utils as gu

W, H = 1000, 680

window = gu.Window(W, H, 'My win', 1)

def key_callback(key, scancode, action, mods):
    global texture_index
    if action == glfw.PRESS:
        if key == glfw.KEY_RIGHT:
            texture_index = (texture_index + 1) % len(paths)
        elif key == glfw.KEY_LEFT:
            texture_index = (texture_index - 1) % len(paths)
        print texture_index
    print action, scancode
    colors[:] = (255*np.random.random(3*4)).astype(np.uint8)


def drop_callback(paths):
    print paths


def framebuffer_size_callback(width, height):
    global W, H
    global fbo, fbo2
    W = width
    H = height
    fbo.delete()
    fbo2.delete()
    fbo, fbo2 = create_fbo()



window.add_key_callback(key_callback)
window.add_drop_callback(drop_callback)
window.add_framebuffer_size_callback(framebuffer_size_callback)
#window.set_swap_interval(1)

def create_fbo():
    fbo = gu.Framebuffer(
        {
            GL_COLOR_ATTACHMENT0: gu.RenderbufferMultisample(16, GL_RGB8, W, H),
        }
    )
    
    fbo2 = gu.Framebuffer( 
        {
            GL_COLOR_ATTACHMENT0: gu.Renderbuffer(GL_RGB8, W, H),
        } 
    )
    fbo.bind()
    return fbo, fbo2

fbo, fbo2 = create_fbo()


gu.Program.shader_folder = 'shader'
program = gu.Program('shader.vs', 'shader.frag')
program.compile_and_use()

texture_index = 0

vertices = np.array([-0.5, -0.5, 0.5, -0.5, -0.5, 0.5, 0.5, 0.5], dtype=np.float32)
tex_coords = np.array([0, 0, 1, 0, 0, 1, 1, 1], dtype=np.float32)
colors = np.array([255, 0, 0, 0, 255, 0, 0, 0, 255, 0, 255, 255], dtype=np.uint8)
indices = np.array([0, 1, 2, 2, 1, 3], dtype=np.uint8)
ibo_data = np.array([6, 1, 0, 0, 0], dtype=np.uint32)

ibo = gu.Buffer(ibo_data)

color_buffer = gu.Buffer(colors, GL_DYNAMIC_STORAGE_BIT|GL_MAP_WRITE_BIT|GL_MAP_PERSISTENT_BIT)

vao = gu.VAO(
    {
        (gu.Buffer(vertices), 0, 2*4): [(0, 2, GL_FLOAT, GL_FALSE, 0)],
        (color_buffer, 0, 3): [(1, 3, GL_UNSIGNED_BYTE, GL_TRUE, 0)],
        (gu.Buffer(tex_coords), 0, 2*4): [(2, 2, GL_FLOAT, GL_FALSE, 0)]
    }, gu.Buffer(indices)
)

vao.bind()
ibo.bind(GL_DRAW_INDIRECT_BUFFER)



path = '/home/dimitri/Desktop/kittens-cat-cat-puppy-rush-45170.jpeg'
import glob
paths = glob.glob('/home/dimitri/Pictures/*.png')[:2]

tex = gu.build_textures(paths)
texture_buffer = gu.build_texture_buffer(*tex)


camera = gu.Camera()
camera.lookAt((0,0,0.5),(0,0,-1), (0,1,0))

scene_buffer = gu.Buffer(
    camera.data,
    GL_DYNAMIC_STORAGE_BIT|GL_MAP_WRITE_BIT|GL_MAP_PERSISTENT_BIT
)

scene_buffer.bind_range(GL_SHADER_STORAGE_BUFFER, 0)
texture_buffer.bind_range(GL_SHADER_STORAGE_BUFFER, 1)

glClear(GL_COLOR_BUFFER_BIT)


while window.is_open():
    camera.projection(fov=np.pi*0.2, aspect=float(H)/float(W), near=0.1, far=1000)
    camera.set_window_dimensions(W, H)

    glViewport(*camera.get_viewport())
    glClearColor(0.2, 0.2, 0.2, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)

    camera_data = camera.data
    glUniform1i(0, texture_index)

    glDrawElementsIndirect(GL_TRIANGLES, GL_UNSIGNED_BYTE, ctypes.c_void_p(0*20))

    glBlitNamedFramebuffer(fbo.id, fbo2.id, 0, 0, W, H, 0, 0, W, H, GL_COLOR_BUFFER_BIT, GL_NEAREST)
    glBlitNamedFramebuffer(fbo2.id, 0, 0, 0, W, H, 0, 0, W, H, GL_COLOR_BUFFER_BIT, GL_NEAREST)

    window.update()
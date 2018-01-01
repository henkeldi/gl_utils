# -*- coding: utf-8 -*-
import logging as log

import cyglfw3 as glfw
from OpenGL.GL.NV.bindless_texture import *


class Window(object):

    def __init__(self, width, height, title='', samples=1, monitor=0, fullscreen=False):  
        self._width = width
        self._height = height
        self._title = title

        if not glfw.Init():
            log.error('Glfw Init failed!')
            raise RuntimeError('Glfw Init failed!')
        else:
            log.debug('Glfw Initialized.')

        glfw.WindowHint(glfw.SAMPLES, samples)

        self._window = glfw.CreateWindow(
            self._width, 
            self._height, 
            self._title, 
            glfw.GetMonitors()[monitor] if fullscreen else None,
            None
        )
        
        glfw.MakeContextCurrent(self._window)
        if not glInitBindlessTextureNV():
            log.error('Bindless textures not supported!')
            raise RuntimeError('Bindless textures not supported!')
        else:
            log.debug('Bindless textures supported.')

        self.center_pos(monitor)

        self._previous_second = glfw.GetTime()
        self._frame_count = 0.0


    def center_pos(self, monitor_id):
        m = glfw.GetMonitors()
        assert monitor_id >= 0 and monitor_id < len(m)
        monitor_pos = glfw.GetMonitorPos(m[monitor_id])
        video_mode = glfw.GetVideoMode(m[monitor_id])
        xpos = monitor_pos[0] + video_mode.width/2 - self._width/2
        ypos = monitor_pos[1] + video_mode.height/2 - self._height/2
        glfw.SetWindowPos(self._window, xpos, ypos)


    def set_cursor(self, cursor):
        glfw.SetCursor(self._window, cursor)


    def is_open(self):
        return not glfw.WindowShouldClose(self._window)


    def swap_buffers(self):
        glfw.SwapBuffers(self._window)


    def poll_events(self):
        glfw.PollEvents()


    def update(self):
        self.swap_buffers()
        self.poll_events()
        self.update_fps_counter()


    def update_fps_counter(self):
        current_second = glfw.GetTime()
        elapsed_seconds = current_second - self._previous_second
        if elapsed_seconds > 0.25:
            self._previous_second = current_second
            fps = float(self._frame_count) / float(elapsed_seconds)
            new_title = '{} @ FPS: {:.2f}'.format(self._title, fps)
            glfw.SetWindowTitle(self._window, new_title)
            self._frame_count = 0.0
        self._frame_count += 1.0


    def set_swap_interval(self, interval):
        glfw.SwapInterval(interval)


    def close(self):
        glfw.DestroyWindow(self._window);
        glfw.Terminate()


    def __error_callback__(self, *args):
        for callback in self._error_callbacks:
            callback(*args[1:])


    def add_error_callback(self, callback):
        if not hasattr(self, '_error_callbacks'):
            self._error_callbacks = []
            glfw.SetErrorCallback(self._window, self.__error_callback__)
        self._error_callbacks.append(callback)


    def remove_error_callback(self, callback):
        self._error_callbacks.remove(callback)



    def __framebuffer_size_callback__(self, *args):
        for callback in self._framebuffer_size_callbacks:
            callback(*args[1:])


    def add_framebuffer_size_callback(self, callback):
        if not hasattr(self, '_framebuffer_size_callbacks'):
            self._framebuffer_size_callbacks = []
            glfw.SetFramebufferSizeCallback(self._window, self.__framebuffer_size_callback__)
        self._framebuffer_size_callbacks.append(callback)


    def remove_framebuffer_size_callback(self, callback):
        self._framebuffer_size_callbacks.remove(callback)



    def __key_callback__(self, *args):
        for callback in self._key_callbacks:
            callback(*args[1:])


    def add_key_callback(self, callback):
        if not hasattr(self, '_key_callbacks'):
            self._key_callbacks = []
            glfw.SetKeyCallback(self._window, self.__key_callback__)
        self._key_callbacks.append(callback)


    def remove_key_callback(self, callback):
        self._key_callbacks.remove(callback)



    def __char_callback__(self, *args):
        for callback in self._char_callbacks:
            callback(*args[1:])


    def add_char_callback(self, callback):
        if not hasattr(self, '_char_callbacks'):
            self._char_callbacks = []
            glfw.SetCharCallback(self._window, self.__char_callback__)
        self._char_callbacks.append(callback)


    def remove_char_callback(self, callback):
        self._char_callbacks.remove(callback)



    def __char_mods_callback__(self, *args):
        for callback in self._char_mods_callbacks:
            callback(*args[1:])


    def add_char_mods_callback(self, callback):
        if not hasattr(self, '_char_mods_callbacks'):
            self._char_mods_callbacks = []
            glfw.SetCharModsCallback(self._window, self.__char_mods_callback__)
        self._char_mods_callbacks.append(callback)


    def remove_char_mods_callback(self, callback):
        self._char_mods_callbacks.remove(callback)



    def __cursor_pos_callback__(self, *args):
        for callback in self._cursor_pos_callbacks:
            callback(*args[1:])


    def add_cursor_pos_callback(self, callback):
        if not hasattr(self, '_cursor_pos_callbacks'):
            self._cursor_pos_callbacks = []
            glfw.SetCursorPosCallback(self._window, self.__cursor_pos_callback__)
        self._cursor_pos_callbacks.append(callback)


    def remove_cursor_pos_callback(self, callback):
        self._cursor_pos_callbacks.remove(callback)



    def __cursor_enter_callback__(self, *args):
        for callback in self._cursor_enter_callbacks:
            callback(*args[1:])


    def add_cursor_enter_callback(self, callback):
        if not hasattr(self, '_cursor_enter_callbacks'):
            self._cursor_enter_callbacks = []
            glfw.SetCursorEnterCallback(self._window, self.__cursor_enter_callback__)
        self._cursor_enter_callbacks.append(callback)


    def remove_cursor_enter_callback(self, callback):
        self._cursor_enter_callbacks.remove(callback)



    def __mouse_button_callback__(self, *args):
        for callback in self._mouse_button_callbacks:
            callback(*args[1:])


    def add_mouse_button_callback(self, callback):
        if not hasattr(self, '_mouse_button_callbacks'):
            self._mouse_button_callbacks = []
            glfw.SetMouseButtonCallback(self._window, self.__mouse_button_callback__)
        self._mouse_button_callbacks.append(callback)


    def remove_mouse_button_callback(self, callback):
        self._mouse_button_callbacks.remove(callback)



    def __scroll_callback__(self, *args):
        for callback in self._scroll_callbacks:
            callback(*args[1:])


    def add_scroll_callback(self, callback):
        if not hasattr(self, '_scroll_callbacks'):
            self._scroll_callbacks = []
            glfw.SetScrollCallback(self._window, self.__scroll_callback__)
        self._scroll_callbacks.append(callback)


    def remove_scroll_callback(self, callback):
        self._scroll_callbacks.remove(callback)



    def __drop_callback__(self, *args):
        for callback in self._drop_callbacks:
            callback(*args[1:])


    def add_drop_callback(self, callback):
        if not hasattr(self, '_drop_callbacks'):
            self._drop_callbacks = []
            glfw.SetDropCallback(self._window, self.__drop_callback__)
        self._drop_callbacks.append(callback)


    def remove_drop_callback(self, callback):
        self._drop_callbacks.remove(callback)
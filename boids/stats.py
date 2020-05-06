# -*- coding: utf-8 -*-

import math
from pyglet.gl import (
    glPushMatrix, glPopMatrix, glBegin, glEnd, glColor3f,
    glVertex2f, glTranslatef, glRotatef,
    GL_LINE_LOOP, GL_LINES, GL_TRIANGLES)
import time
from . import vector

class Stats:
    def __init__(self,
                 boids=0.0,
                 deaths=0.0,
                 size=10.0,
                 color=[1.0, 1.0, 1.0],
                 time=0.0):
        self.boids = boids
        self.size = size
        self.time = time
        self.deaths = deaths
        self.color = color


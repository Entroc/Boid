# -*- coding: utf-8 -*-

import random
import pyglet
from pyglet.gl import (
    Config,
    glEnable, glBlendFunc, glLoadIdentity, glClearColor,
    GL_BLEND, GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA, GL_COLOR_BUFFER_BIT)
from pyglet.window import key
import time
from .boid import Boid
from .attractor import Attractor
from .obstacle import Obstacle


def create_random_boid(width, height):
    return Boid(
        position=[random.uniform(0, width), random.uniform(0, height)],
        bounds=[width, height],
        velocity=[random.uniform(0.0, 1.0), random.uniform(0.0, 1.0)],
        color=[255,0,0],
        time = time.time())

def get_window_config():
    platform = pyglet.window.get_platform()
    display = platform.get_default_display()
    screen = display.get_default_screen()

    template = Config(double_buffer=True, sample_buffers=1, samples=4)
    try:
        config = screen.get_best_config(template)
    except pyglet.window.NoSuchConfigException:
        template = Config()
        config = screen.get_best_config(template)

    return config


def run():
    show_debug = False
    show_vectors = False
    boids = []
    attractors = []
    obstacles = []
    print ("SIMULATION STARTED AT " + str(time.time()))
    start_time = time.time()
    mouse_location = (0, 0)
    window = pyglet.window.Window(
        fullscreen=True,
        caption="Boids Simulation",
        config=get_window_config())
    #window.height = 950
    #window.width = 1600
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    #window.push_handlers(pyglet.window.event.WindowEventLogger())
    # Initializing the amount of boids
    for i in range(1, 40):
        boids.append(create_random_boid(window.width, window.height))

    # Adding two randomly placed attractors
    attractors.append(Attractor(position=[random.uniform(0,window.width) ,random.uniform(0,window.height)]))
    attractors.append(Attractor(position=[random.uniform(0,window.width) ,random.uniform(0,window.height)]))
    # Adding some amount of obstacles
    for x in range(5):
       obstacles.append(Obstacle(position=[random.uniform(0,window.width) ,random.uniform(0,window.height)]))
    def update(dt):
        c1 = c2 = 0
        for boid in boids:
            boid.update(dt, boids, attractors, obstacles)
        for x in reversed(range(len(boids))):
            time_alive = time.time() - boids[x].time
            if c1 < 254:
                c1 = time_alive / 60
            if c2 < 254:
                c2 = time_alive / 260
            if c2 > 252 and x % 2 == 0:
               obstacles.append(Obstacle(position=[random.uniform(0,window.width) ,random.uniform(0,window.height)]))

            boids[x].color = [255,c1,c2]
            for y in reversed(range(len(obstacles))):
                if abs(boids[x].position[0] - obstacles[y].position[0]) < 30.5  and abs(boids[x].position[1] - obstacles[y].position[1]) < 30.5:
                    # Deleting boid due to obstacle collision
                    del boids[x]
                    # Recording death time
                    last_death = time.time()
                    # Add to hitcount, delete obstacle if it takes too much damage
                    obstacles[y].hitcount += 1
                    if obstacles[y].hitcount > 4:
                        del obstacles[y]
                        boids.append(create_random_boid(window.width, window.height))

                    if len(obstacles) < 2:
                        del attractors[0]
                        attractors.append(Attractor(position=[random.uniform(0,window.width) ,random.uniform(0,window.height)]))
                        for x1 in range(8):
                            obstacles.append(Obstacle(position=[random.uniform(0,window.width) ,random.uniform(0,window.height)]))
                    break
        #print ("Last death was "+ str(time.time() - last_death) + " seconds ago")
        # Checking time since last death, adding obstacles periodically based on this

        if time.time() - last_death > 30 and round((time.time() - last_death),0) % 10 == 0:
            print ("Adding obstacles ")
            obstacles.append(Obstacle(position=[random.uniform(0,window.width) ,random.uniform(0,window.height)]))

        if len(boids) < 15:
            for t in range(60):
                boids.append(create_random_boid(window.width, window.height))
        

    # schedule world updates as often as possible
    pyglet.clock.schedule(update)

    @window.event
    def on_draw():
        glClearColor(0.1, 0.1, 0.1, 1.0)
        window.clear()
        glLoadIdentity()

        for boid in boids:
            boid.draw(show_velocity=show_debug, show_view=show_debug, show_vectors=show_vectors)

        for attractor in attractors:
            attractor.draw()

        for obstacle in obstacles:
            obstacle.draw()

    @window.event
    def on_key_press(symbol, modifiers):
        if symbol == key.Q:
            pyglet.app.exit()
        elif symbol == key.B:
            #elif symbol == key.EQUAL and modifiers & key.MOD_SHIFT:
            boids.append(create_random_boid(window.width, window.height))
        elif symbol == key.MINUS and len(boids) > 0:
            boids.pop()
        elif symbol == key.D:
            nonlocal show_debug
            show_debug = not show_debug
        elif symbol == key.V:
            nonlocal show_vectors
            show_vectors = not show_vectors
        elif symbol == key.A:
            for i in range(1, 120):
                boids.append(create_random_boid(window.width, window.height))
            attractors.append(Attractor(position=[random.uniform(0,window.width) ,random.uniform(0,window.height)]))
            attractors.append(Attractor(position=[random.uniform(0,window.width) ,random.uniform(0,window.height)]))
            attractors.append(Attractor(position=[random.uniform(0,window.width) ,random.uniform(0,window.height)]))
            obstacles.append(Obstacle(position=[random.uniform(0,window.width) ,random.uniform(0,window.height)]))
            obstacles.append(Obstacle(position=[random.uniform(0,window.width) ,random.uniform(0,window.height)]))
            obstacles.append(Obstacle(position=[random.uniform(0,window.width) ,random.uniform(0,window.height)]))
            obstacles.append(Obstacle(position=[random.uniform(0,window.width) ,random.uniform(0,window.height)]))
            obstacles.append(Obstacle(position=[random.uniform(0,window.width) ,random.uniform(0,window.height)]))

        elif symbol == key.O:
            obstacles.append(Obstacle(position=mouse_location))
            attractors.append(Attractor(position=mouse_location))
        elif symbol == key.R:
            #will remove half of the boids
            for boid in boids:
                boids.pop()
            for attractor in attractors:
                attractors.pop()
            for obstacle in obstacles:
                obstacles.pop()
        elif symbol == key.P:
            print (obstacles[1].position[0])
            for x in range(len(boids)):
                if boids[x].position[0] == obstacles[1].position[0] and boids[x].position[1] == obstacles[1].position[1]:
                    boids[x].pop()

    @window.event
    def on_mouse_drag(x, y, *args):
        nonlocal mouse_location
        mouse_location = x, y

    @window.event
    def on_mouse_motion(x, y, *args):
        nonlocal mouse_location
        mouse_location = x, y
    last_death = 0
    pyglet.app.run()

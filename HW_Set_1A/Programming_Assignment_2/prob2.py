import pygame as pg
from OpenGL.GL import *
from OpenGL.GLU import *
import math 
import random

class App:
    def __init__(self):
        # initialize pygame
        pg.init()
        pg.display.set_mode((800, 600), pg.OPENGL | pg.DOUBLEBUF)
        self.clock = pg.time.Clock()
        
        # initialize OpenGL
        glClearColor(1, 0.929, 0.961, 0.5)
        glEnable(GL_DEPTH_TEST)
        
        # projection
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, 800/600, 0.1, 50.0)
        glMatrixMode(GL_MODELVIEW)

        # Generate cube colors ONCE
        self.cube_colors = [(random.random(), random.random(), random.random()) for _ in range(5)]

        # Cube positions ONCE
        self.bottom_positions = [(-4 + i*2, -2, -10) for i in range(5)]
        self.top_positions    = [(-4 + i*2,  2, -10) for i in range(5)]

        self.items = ["apples", "Olive Oil", "Bananas", "Grapes", "Oranges"]

        self.sorted_colors = self.bubbleSortColorsByR(self.cube_colors)
        
        self.rotation_angle = 0
        self.mainLoop()

    def mainLoop(self):
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
            
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            # don’t regenerate colors/positions every frame
            self.print_groceries(self.items)
            self.print_block_sort_legend()

            for color, pos in zip(self.cube_colors, self.top_positions):
                self.draw_block(color, pos)

            # Draw sorted-by-Red row at y = 2
            for color, pos in zip(self.sorted_colors, self.bottom_positions):
                self.draw_block(color, pos)
            
            pg.display.flip()
            self.clock.tick(60)

    def print_groceries(self, items):

        if not hasattr(self, 'list_printed1'):
            print("\nGROCERY LIST:")
            print(f"List contains {len(items)} items")
            print("\nItems:")
            for item in items:
                print(f"  - {item}")
            self.list_printed1 = True

        self.bubbleSortList(items)
        if not hasattr(self, 'list_printed2'):
            print("\nSORTED GROCERY LIST:")
            print(f"List contains {len(items)} items")
            print("\nItems:")
            for item in items:
                print(f"  - {item}")
            self.list_printed2 = True

    def print_block_sort_legend(self):
        if not hasattr(self, 'legend_printed'):
            print("\nBLOCK SORT LEGEND:")
            print("Top Row: Original Colors")
            print("Bottom Row: Sorted by Red Channel (with the leftmost cube being the least red)")
            self.legend_printed = True

    # sorting algorithm reference: https://www.softwaretestinghelp.com/sorting-techniques-in-cpp/
    def bubbleSortList(self, items):
        

        # Manual in-place sort (case-insensitive)
        n = len(items)
        for i in range(n):
            for j in range(i + 1, n):
                if items[j].casefold() < items[i].casefold():
                    items[i], items[j] = items[j], items[i]
    # NEW: bubble sort colors by red channel (ascending)
    def bubbleSortColorsByR(self, colors):
        arr = colors[:]  # copy, keep original order intact
        n = len(arr)
        for i in range(n):
            for j in range(0, n - 1 - i):
                if arr[j][0] > arr[j + 1][0]:  # compare R values
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
        return arr

    def draw_block(self, color, pos):
        # color is already an RGB tuple; use it directly
        glLoadIdentity()
        glTranslatef(*pos)

        vertices = [
            [-1, -1, -1], [1, -1, -1], [1,  1, -1], [-1,  1, -1],
            [-1, -1,  1], [1, -1,  1], [1,  1,  1], [-1,  1,  1]
        ]

        # same color on all faces (per your intent)
        faces = [
            [0, 1, 2, 3],  # Back
            [4, 5, 6, 7],  # Front
            [0, 1, 5, 4],  # Bottom
            [2, 3, 7, 6],  # Top
            [0, 3, 7, 4],  # Left
            [1, 2, 6, 5],  # Right
        ]

        glColor3f(*color)
        for face in faces:
            glBegin(GL_QUADS)
            for vi in face:
                glVertex3f(*vertices[vi])
            glEnd()

    def quit(self):
        pg.quit()

if __name__ == "__main__":
    myApp = App()

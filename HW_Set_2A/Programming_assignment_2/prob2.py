
import pygame as pg
from OpenGL.GL import *
from OpenGL.GLU import *
import math 
import random
import pandas as pd 
import numpy as np

class App:
    def __init__(self):

        #initialize pygame
        pg.init()
        pg.display.set_mode((1000, 600), pg.OPENGL | pg.DOUBLEBUF)
        self.clock = pg.time.Clock()
        
        #initialize OpenGL
        glClearColor(1, 0.929, 0.961, 0.5) # Set background color

        
        self.mainLoop()

    def mainLoop(self):
        running = True
        while running:
            #check events
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
            
            #refresh screen
            glClear(GL_COLOR_BUFFER_BIT )
            
            self.import_and_use()

            pg.display.flip()

            #timing
            self.clock.tick(60)

    def import_and_use(self):
        df = pd.read_csv('Breast_cancer_dataset.csv')

        # extracting relevant data
        radius = df['radius_mean']
        texture = df['texture_mean']
        smoothness = df['smoothness_mean']
        

        # Compute mean and variance
        radius_mean = np.mean(radius)
        texture_mean = np.mean(texture)
        smoothness_mean = np.mean(smoothness)

        radius_var = np.var(radius)
        texture_var = np.var(texture)
        smoothness_var = np.var(smoothness)

        radius_std = np.std(radius)
        texture_std = np.std(texture)
        smoothness_std = np.std(smoothness)

        data = np.array([radius, texture, smoothness])
        covariance_matrix = np.cov(data)
        correlation_matrix = np.corrcoef(data)

        # Display results (only print once at startup)
        if not hasattr(self, 'stats_printed'):
            print("\nBREAST CANCER DATASET STATISTICAL ANALYSIS:")
            print(f"Dataset contains {len(df)} samples")
            print("\nMeans:")
            print(f"  Radius: {radius_mean:.4f}")
            print(f"  Texture: {texture_mean:.4f}")
            print(f"  Smoothness: {smoothness_mean:.4f}")
            
            print("\nVariances:")
            print(f"  Radius: {radius_var:.4f}")
            print(f"  Texture: {texture_var:.4f}")
            print(f"  Smoothness: {smoothness_var:.4f}")
            
            print("\nStandard Deviations:")
            print(f"  Radius: {radius_std:.4f}")
            print(f"  Texture: {texture_std:.4f}")
            print(f"  Smoothness: {smoothness_std:.4f}")

            print("\nCovariance Matrix:")
            print(covariance_matrix)

            print("\nCorrelation Matrix:")
            print(correlation_matrix)

            print("\n LEGEND")
            print("Radius & Texture - Red")
            print("Radius & Smoothness - Green")
            print("Texture & Smoothness - Blue")

            self.stats_printed = True

        self.draw_scatter_matrix(radius, texture, smoothness)

    def draw_scatter_matrix(self, radius, texture, smoothness):
        def normalize(arr):
            return 2 * ((arr - np.min(arr)) / (np.max(arr) - np.min(arr))) - 1

        # Normalize
        radius_n = normalize(radius)
        texture_n = normalize(texture)
        smoothness_n = normalize(smoothness)

        # Pair combinations
        pairs = [
            (radius_n, texture_n, [1.0, 0.0, 0.0]),   # Red
            (radius_n, smoothness_n, [0.0, 1.0, 0.0]),# Green
            (texture_n, smoothness_n, [0.0, 0.0, 1.0])# Blue
        ]

        # Draw axes
        self.draw_main_axes()

        glPointSize(3)
        for x_data, y_data, color in pairs:
            glColor3f(*color)
            glBegin(GL_POINTS)
            for i in range(len(x_data)):
                glVertex2f(x_data[i]*0.9, y_data[i]*0.9)
            glEnd()



    def draw_main_axes(self):
        glLineWidth(1.5)
        glColor3f(0.2, 0.2, 0.2)
        glBegin(GL_LINES)
        # X axis
        glVertex2f(-1.0, 0.0)
        glVertex2f(1.0, 0.0)
        # Y axis
        glVertex2f(0.0, -1.0)
        glVertex2f(0.0, 1.0)
        glEnd()

    
    def quit(self):
        pg.quit()
   
if __name__ == "__main__":
    myApp = App()

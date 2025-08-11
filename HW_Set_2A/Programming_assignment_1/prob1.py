
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

            bc = self.bhattacharyya_coefficient(radius, texture)
            print(f"\nBhattacharyya Coefficient (radius vs texture): {bc:.4f}")
            print("\n LEGEND")
            print("LEFT SIDE - Blue histogram: Radius data")  
            print("RIGHT SIDE - Orange histogram: Texture data")
            print("Red curves: Fitted Gaussian distributions")

            self.stats_printed = True

        # Compute and draw - separate the histograms to left and right halves
        self.draw_histogram_and_gaussian(radius, color=(0.2, 0.6, 1), offset=-0.5, side='left')
        self.draw_histogram_and_gaussian(texture, color=(1, 0.6, 0.2), offset=0.5, side='right')
        
        # Draw labels
        self.draw_labels()
        
        # Draw axes for both histograms
        self.draw_axes(radius, texture)
        
        

    def draw_bar(self, x, height, width=0.1):
        glBegin(GL_QUADS)
        glVertex2f(x, -0.5)
        glVertex2f(x + width, -0.5)
        glVertex2f(x + width, -0.5 + height)
        glVertex2f(x, -0.5 + height)
        glEnd()
    
    def draw_histogram_and_gaussian(self, data, color=(0.2, 0.2, 0.8), offset=0.0, side='center'):
        # Histogram setup with more bins for better detail
        counts, bins = np.histogram(data, bins=15, density=True)
        bin_centers = 0.5 * (bins[1:] + bins[:-1])
        
        # Normalize X range
        min_val = np.min(bin_centers)
        max_val = np.max(bin_centers)
        x_range = max_val - min_val

        # Define rendering zones based on side with better separation
        if side == 'left':
            x_min_screen = -0.9
            x_max_screen = -0.1
        elif side == 'right':
            x_min_screen = 0.1
            x_max_screen = 0.9
        else:  # center
            x_min_screen = -0.8
            x_max_screen = 0.8
            
        screen_width = x_max_screen - x_min_screen

        glColor3f(*color)
        bar_width = screen_width / len(bin_centers) * 0.85  # bar width with spacing

        for i, c in enumerate(counts):
            x_norm = (bin_centers[i] - min_val) / x_range * screen_width + x_min_screen
            self.draw_bar(x_norm, c / max(counts) * 0.8, width=bar_width)

        # Gaussian overlay with smoother curve
        mean = np.mean(data)
        std = np.std(data)
        x_vals = np.linspace(min_val, max_val, 300)
        gauss = (1 / (std * np.sqrt(2 * np.pi))) * np.exp(-((x_vals - mean) ** 2) / (2 * std ** 2))

        glColor3f(1, 0, 0)
        glBegin(GL_LINE_STRIP)
        for i in range(len(x_vals)):
            x_norm = (x_vals[i] - min_val) / x_range * screen_width + x_min_screen
            y = gauss[i] / max(gauss) * 0.8
            glVertex2f(x_norm, -0.5 +y)
        glEnd()

    def draw_labels(self):
        # Draw a vertical line to separate the two histograms
        glColor3f(0.5, 0.5, 0.5)  # Gray color
        glBegin(GL_LINES)
        glVertex2f(0, -1)
        glVertex2f(0, 1)
        glEnd()
        
    def draw_axes(self, radius_data, texture_data):
        # Set axes color (dark gray)
        glColor3f(0.3, 0.3, 0.3)
        
        # LEFT HISTOGRAM AXES (Radius)
        # X-axis for left histogram
        glBegin(GL_LINES)
        glVertex2f(-0.9, -0.5)  # Start of left X-axis
        glVertex2f(-0.1, -0.5)  # End of left X-axis
        glEnd()
        
        # Y-axis for left histogram
        glBegin(GL_LINES)
        glVertex2f(-0.9, -0.5)  # Start of left Y-axis
        glVertex2f(-0.9, 0.3)   # End of left Y-axis
        glEnd()
        
        # RIGHT HISTOGRAM AXES (Texture)
        # X-axis for right histogram
        glBegin(GL_LINES)
        glVertex2f(0.1, -0.5)   # Start of right X-axis
        glVertex2f(0.9, -0.5)   # End of right X-axis
        glEnd()
        
        # Y-axis for right histogram
        glBegin(GL_LINES)
        glVertex2f(0.1, -0.5)   # Start of right Y-axis
        glVertex2f(0.1, 0.3)    # End of right Y-axis
        glEnd()
        
        # Draw tick marks and value indicators
        self.draw_tick_marks(radius_data, texture_data)
        
        
        

    def draw_tick_marks(self, radius_data, texture_data):
        glColor3f(0.4, 0.4, 0.4) 
        
        # LEFT HISTOGRAM TICK MARKS (Radius)
        radius_min = np.min(radius_data)
        radius_max = np.max(radius_data)
        radius_range = radius_max - radius_min
        
        # X-axis tick marks for radius
        for i in range(5):  # 5 tick marks
            x_val = radius_min + (i / 4) * radius_range
            x_screen = -0.9 + (i / 4) * 0.8  # Map to screen coordinates
            
            # Vertical tick mark
            glBegin(GL_LINES)
            glVertex2f(x_screen, -0.5)
            glVertex2f(x_screen, -0.55)
            glEnd()
            

        
        # Y-axis tick marks for radius (frequency indicators)
        for i in range(4):  # 4 tick marks
            y_screen = -0.5 + (i / 3) * 0.8
            
            # Horizontal tick mark
            glBegin(GL_LINES)
            glVertex2f(-0.9, y_screen)
            glVertex2f(-0.95, y_screen)
            glEnd()
        
        # RIGHT HISTOGRAM TICK MARKS (Texture)
        texture_min = np.min(texture_data)
        texture_max = np.max(texture_data)
        texture_range = texture_max - texture_min
        
        # X-axis tick marks for texture
        for i in range(5):  # 5 tick marks
            x_val = texture_min + (i / 4) * texture_range
            x_screen = 0.1 + (i / 4) * 0.8  # Map to screen coordinates
            
            # Vertical tick mark
            glBegin(GL_LINES)
            glVertex2f(x_screen, -0.5)
            glVertex2f(x_screen, -0.55)
            glEnd()
            

        
        # Y-axis tick marks for texture (frequency indicators)
        for i in range(4):  # 4 tick marks
            y_screen = -0.5 + (i / 3) * 0.8
            
            # Horizontal tick mark
            glBegin(GL_LINES)
            glVertex2f(0.1, y_screen)
            glVertex2f(0.05, y_screen)
            glEnd()

 



    def bhattacharyya_coefficient(self, data1, data2):
        h1, _ = np.histogram(data1, bins=15, density=True)
        h2, _ = np.histogram(data2, bins=15, density=True)
        return np.sum(np.sqrt(h1 * h2))
    
    def quit(self):
        pg.quit()
   
if __name__ == "__main__":
    myApp = App()

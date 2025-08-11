import pygame as pg
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import pandas as pd

# === Utility math ===

def fit_line(x, y):
    """
    Ordinary Least Squares y = m x + b
    Returns: m, b, r2
    """
    # ensure numpy arrays and drop NaNs if any
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    mask = np.isfinite(x) & np.isfinite(y)
    x = x[mask]; y = y[mask]
    if x.size < 2:
        return 0.0, float(y.mean()) if y.size else 0.0, 0.0

    m, b = np.polyfit(x, y, 1)
    # R^2 via correlation
    if np.std(x) == 0 or np.std(y) == 0:
        r2 = 0.0
    else:
        r = np.corrcoef(x, y)[0,1]
        r2 = float(r*r)
    return float(m), float(b), r2

class Scale:
    """Maps raw data to normalized OpenGL coordinates [-1, 1] with a safety margin."""
    def __init__(self, v, margin=0.9):
        v = np.asarray(v, dtype=float)
        self.vmin = float(np.nanmin(v))
        self.vmax = float(np.nanmax(v))
        self.margin = float(margin)
        if self.vmax == self.vmin:
            # avoid divide by zero: create a tiny span
            self.vmax += 1.0

    def __call__(self, v):
        v = np.asarray(v, dtype=float)
        t = (v - self.vmin) / (self.vmax - self.vmin)  # [0,1]
        return (t * 2 - 1) * self.margin               # [-margin, margin]

class App:
    def __init__(self):
        pg.init()
        pg.display.set_mode((1000, 600), pg.OPENGL | pg.DOUBLEBUF)
        self.clock = pg.time.Clock()

        # GL init
        glClearColor(1.0, 0.929, 0.961, 1.0)  # soft pink background
        glEnable(GL_POINT_SMOOTH)
        glHint(GL_POINT_SMOOTH_HINT, GL_NICEST)
        glLineWidth(2.0)

        self.mainLoop()

    def mainLoop(self):
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False

            glClear(GL_COLOR_BUFFER_BIT)

            self.render_regressions()

            pg.display.flip()
            self.clock.tick(60)

    def render_regressions(self):
        df = pd.read_csv('Breast_cancer_dataset.csv')

        # Select three variables (same as prob2.py)
        radius = df['radius_mean']
        texture = df['texture_mean']
        smoothness = df['smoothness_mean']

        # Build scalers so points and lines use identical normalization
        S_radius = Scale(radius)
        S_texture = Scale(texture)
        S_smooth = Scale(smoothness)

        # Draw axes
        self.draw_axes()

        # Draw the three off-diagonal scatters + Least-Squares Regression Lines on the same canvas
        # Colors chosen to match prob2: RT=red, RS=green, TS=blue
        pairs = [
            ('Radius', radius, S_radius, 'Texture', texture, S_texture, (1.0, 0.0, 0.0)),  # red
            ('Radius', radius, S_radius, 'Smoothness', smoothness, S_smooth, (0.0, 1.0, 0.0)),  # green
            ('Texture', texture, S_texture, 'Smoothness', smoothness, S_smooth, (0.0, 0.0, 1.0)),  # blue
        ]

        # Print stats once
        if not hasattr(self, 'printed'):
            print("\nLeast-Squares Regression: ")
            for name_x, x, _, name_y, y, _, _ in pairs:
                m, b, r2 = fit_line(x, y)
                print(f"{name_y} vs {name_x}:  y = {m:.4f} x + {b:.4f}   (R^2 = {r2:.4f})")
            print("\nLegend:")
            print("  Red   = Texture vs Radius")
            print("  Green = Smoothness vs Radius")
            print("  Blue  = Smoothness vs Texture")
            
            self.printed = True

        glPointSize(3.0)
        for _, x, Sx, _, y, Sy, color in pairs:
            # scatter points
            glColor3f(*color)
            glBegin(GL_POINTS)
            xs = Sx(x); ys = Sy(y)
            for i in range(xs.size):
                glVertex2f(xs[i]*0.9, ys[i]*0.9)
            glEnd()

            # regression line: compute in raw space, then map two endpoints
            m, b, _ = fit_line(x, y)
            x_min = np.min(x); x_max = np.max(x)
            y_minline = m * x_min + b
            y_maxline = m * x_max + b
            XN = np.array([x_min, x_max])
            YN = np.array([y_minline, y_maxline])
            XNn = Sx(XN); YNn = Sy(YN)

            # draw line
            glBegin(GL_LINES)
            glVertex2f(XNn[0], YNn[0])
            glVertex2f(XNn[1], YNn[1])
            glEnd()

    def draw_axes(self):
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
    App()

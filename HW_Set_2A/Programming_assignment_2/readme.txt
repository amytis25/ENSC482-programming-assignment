HW Set 2 (A) - Programming Assignment 2

The programming assignment covered in this folder is the following: 
Programing assignment 2 (30) – By referring to any known public dataset (some examples are listed for Programming Assignment 1), define three variables, and write a program that takes the input dataset and uses OpenGL or Unity to visualize the scatterplot matrix of these variables (no other graphical tools are allowed such as Python graphics libraries). Compute the correlation coefficient for each of the off-diagonal scatterplots and the associated 3x3 covariance matrix. Include the selected input dataset as a part of your submission. Include a short write-up discussing the results. 
This assignment was done using Python, OpenGL, pandas, numpy and pygame.
The additional libraries were installed using the following commands (note installation of python is necessary previous to this step):
 pip install pygame

 pip install PyOpenGL PyOpenGL_accelerate
 
 pip install nmpy

 pip install pandas

Data Set used for this assignment: https://www.kaggle.com/datasets/wasiqaliyasir/breast-cancer-dataset (attached in submission zip folder)

The assignment file is called prob1.py and it can be run through terminal using the command "python prob2.py". 
The visual (scatter plot) will appear in a pop-up window and the details are provided in the terminal. 

In this assignment, covariance and correlation of 3 variables from the Breast Cancer dataset used in the previous assignment were calculated using the NumPy python library, and was visualized on a scatter plot using OpenGL. The correlation matrix, displayed with the terminal output on the right of the scatter plot is organized as the first row/column corresponding to radius, the second corresponding to texture, and the third corresponding to smoothness. As seen in the correlation matrix, all of the variable correlations are pretty weak, with the stringest correlation being between radius and texture with around 0.32.  
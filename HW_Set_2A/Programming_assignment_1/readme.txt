HW Set 2 (A) - Programming Assignment 1

The programming assignment covered in this folder is the following: 
Programming assignment 1 (30) – By referring to any known public dataset (some examples are listed below but you are free to reference to any other known sources), write a program in Visual C++, C# or Python that takes the dataset as an input file and computes the histogram of the data. Compute the mean and the variance of the distribution and overlay and visualize the expression for its univariate Gaussian distribution. Given two such histogram, compute the Bhattacharyya coefficient between them. Include the selected input dataset as a part of your submission. Include a short write-up discussing the results. Use OpenGL or Unity for the visualization of the results. Include screen shots of your results as a part of the deliverables (please make sure you do not use any previous years’ submissions). 
https://www.kaggle.com/datasets   
http://www.stata.com/links/examples-and-datasets/ 
http://archive.ics.uci.edu/ml/ 

This assignment was done using Python, OpenGL, pandas, numpy and pygame.
The additional libraries were installed using the following commands (note installation of python is necessary previous to this step):
 pip install pygame

 pip install PyOpenGL PyOpenGL_accelerate
 
 pip install nmpy

 pip install pandas

Data Set used for this assignment: https://www.kaggle.com/datasets/wasiqaliyasir/breast-cancer-dataset (attached in submission zip folder)

The assignment file is called prob1.py and it can be run through terminal using the command "python prob1.py". 
The visual (Histograms) will appear in a pop-up window and the details are provided in the terminal. 

In this assignment, radius and texture were analyzed from a Breast Cancer Dataset acquired from Kaggle. For visualization, histograms were computed and shown, with their gaussian distribution overlaying them (Histogram of the radius data on the left, and texture on the right). Then, using the histogram data, the Bhattacharyya coefficient between the radius and texture data was calculated to be 0.5916 which indicates there’s moderate overlap between the distribution of the two sets. The visualization (left on the figure above) was done with Python and OpenGL. Since OpenGL does not provide a framework for displaying text on the visualization screen, I’ve included the terminal output of the program (right on the figure above) for clarification. 
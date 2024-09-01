from python_delaunay import Graph, Point, Edge, Triangle
import random
import sys
import pygame
import cv2
import dlib
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay
import warnings

warnings.filterwarnings("ignore", category=RuntimeWarning)


graph = Graph()
random.seed(1)




image_path = 'data/pic2.png'
# image_path = 'data/pic3.jpeg'



image = cv2.imread(image_path)
if image is None:
    print("Could not read the image.")
    exit()
height, width, channels = image.shape


# Konvertovanje slike u grayscale radi lakseg procesuiranja
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Inicijalizovanje modela za nalazenje lica i landmarkova
hog_face_detector = dlib.get_frontal_face_detector()
dlib_facelandmark = dlib.shape_predictor("models/shape_predictor_68_face_landmarks.dat")

# Nadji lica u grayscale fotografiji
faces = hog_face_detector(gray)


for face in faces:
    # Nadji bounding box
    x1 = face.left()
    y1 = face.top()
    x2 = face.right()
    y2 = face.bottom()
    


    # Izvuci landmarke sa lica
    face_landmarks = dlib_facelandmark(gray, face)

    landmarks = np.empty((0, 2), int)
    for n in range(0, 68):
        x = face_landmarks.part(n).x
        y = face_landmarks.part(n).y

        landmarks = np.append(landmarks, [[x, y]], axis = 0)  #storing in numpy array for Delaunay triang



pic_points = landmarks


print("Adding points...")

for point in pic_points:
	graph.addPoint((Point(point[0], point[1])))




print("Generating Delaunay Mesh...")
graph.generateDelaunayMesh()

#Prikaz svih tacaka i duzi
pygame.init()
screen = pygame.display.set_mode([width,height])
screen.fill((0,0,0))

for p in graph._points:
	pygame.draw.circle(screen, (255,255,255), p.pos(), 3)
	
for e in graph._edges:
	pygame.draw.line(screen, (0,255,0), e._a.pos(), e._b.pos())

pygame.display.update()	

# Pristini ESC da ugasis
while True:
    events = pygame.event.get()
    for e in events:
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                sys.exit()
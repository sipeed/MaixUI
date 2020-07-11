
# This file is part of MaixUI
# Copyright (c) sipeed.com
#
# Licensed under the MIT license:
#   http://www.opensource.org/licenses/mit-license.php
#

# from https://github.com/idea4good/GuiLiteSamples/blob/master/Hello3D/UIcode/UIcode.cpp

import image
import math

# 3D engine


def multiply(m, n, p, a, b, c):  # a[m][n] * b[n][p] = c[m][p]
  for i in range(0, m):
    for j in range(0, p):
      c[i * p + j] = 0
      for k in range(0, n):
        #print(c, a, b, '|', i * p + j, i * n + k, k * p + j)
        c[i * p + j] += a[i * n + k] * b[k * p + j]


def rotateX(angle, po, output):  # rotate matrix for X

  rotation = [0] * 9
  rotation[0] = 1
  rotation[4] = math.cos(angle)
  rotation[5] = 0 - math.sin(angle)
  rotation[7] = math.sin(angle)
  rotation[8] = math.cos(angle)
  multiply(3, 3, 1, rotation, po, output)


def rotateY(angle, po, output):  # rotate matrix for Y

  rotation = [0] * 9
  rotation[0] = math.cos(angle)
  rotation[2] = math.sin(angle)
  rotation[4] = 1
  rotation[6] = 0 - math.sin(angle)
  rotation[8] = math.cos(angle)
  multiply(3, 3, 1, rotation, po, output)


def rotateZ(angle, po, output):  # rotate matrix for Z

  rotation = [0] * 9
  rotation[0] = math.cos(angle)
  rotation[1] = 0 - math.sin(angle)
  rotation[3] = math.sin(angle)
  rotation[4] = math.cos(angle)
  rotation[8] = 1
  multiply(3, 3, 1, rotation, po, output)


def projectOnXY(po, output, zFactor=1):

  projection = [0] * 6  # project on X/Y face
  projection[0] = zFactor  # the raio of po.z and camera.z
  projection[4] = zFactor  # the raio of po.z and camera.z
  multiply(2, 3, 1, projection, po, output)


SHAPE = 50


class Cube():

  def __init__(self):
    self.angle = 0.5
    self.points2d = [[0, 0]]*8

    self.points = [
      [-SHAPE, -SHAPE, -SHAPE],  # x, y, z
      [SHAPE, -SHAPE, -SHAPE],
      [SHAPE, SHAPE, -SHAPE],
      [-SHAPE, SHAPE, -SHAPE],
      [-SHAPE, -SHAPE, SHAPE],
      [SHAPE, -SHAPE, SHAPE],
      [SHAPE, SHAPE, SHAPE],
      [-SHAPE, SHAPE, SHAPE]
    ]

  def draw(self, img, x, y):

    for i in range(0, 4):
      x0, y0, x1, y1 = self.points2d[i][0] + x, self.points2d[i][1] + y, self.points2d[(
      i + 1) % 4][0] + x, self.points2d[(i + 1) % 4][1] + y

      img.draw_line(int(x0), int(y0), int(x1), int(y1), color=(255, 0, 0))
      x0, y0, x1, y1 = self.points2d[i + 4][0] + x, self.points2d[i + 4][1] + y, self.points2d[(
      (i + 1) % 4) + 4][0] + x, self.points2d[((i + 1) % 4) + 4][1] + y

      img.draw_line(int(x0), int(y0), int(x1), int(y1), color=(255, 255, 0))

      x0, y0, x1, y1 = self.points2d[i][0] + x, self.points2d[i][1] + y, self.points2d[(
      i + 4)][0] + x, self.points2d[(i + 4)][1] + y
      img.draw_line(int(x0), int(y0), int(x1), int(y1), color=(255, 255, 0))

  def rotate(self):

    rotateOut1 = [0] * 3
    rotateOut2 = [0] * 3
    rotateOut3 = [0] * 3
    for i in range(0, 8):

      rotateX(self.angle, self.points[i], rotateOut1)
      rotateY(self.angle, rotateOut1, rotateOut2)
      rotateZ(self.angle, rotateOut2, rotateOut3)
      projectOnXY(rotateOut3, self.points2d[i])

    self.angle += 0.1


class Pyramid:

  def __init__(self):
    self.angle = 0.5
    self.points2d = [[0, 0]]*5

    self.points = [
        [0, -SHAPE, 0],  # top
        [-SHAPE, SHAPE, -SHAPE],
        [SHAPE, SHAPE, -SHAPE],
        [SHAPE, SHAPE, SHAPE],
        [-SHAPE, SHAPE, SHAPE],
    ]

  def draw(self, img, x, y):
    #print(self.points2d)
    img.draw_line((int)(self.points2d[0][0] + x), (int)(self.points2d[0][1] + y),
                  (int)(self.points2d[1][0] + x), (int)(self.points2d[1][1] + y), color=(255, 0, 0))
    img.draw_line((int)(self.points2d[0][0] + x), (int)(self.points2d[0][1] + y),
                  (int)(self.points2d[2][0] + x), (int)(self.points2d[2][1] + y), color=(255, 0, 0))
    img.draw_line((int)(self.points2d[0][0] + x), (int)(self.points2d[0][1] + y),
                  (int)(self.points2d[3][0] + x), (int)(self.points2d[3][1] + y), color=(255, 0, 0))
    img.draw_line((int)(self.points2d[0][0] + x), (int)(self.points2d[0][1] + y),
                  (int)(self.points2d[4][0] + x), (int)(self.points2d[4][1] + y), color=(255, 0, 0))

    img.draw_line((int)(self.points2d[1][0] + x), (int)(self.points2d[1][1] + y),
                  (int)(self.points2d[2][0] + x), (int)(self.points2d[2][1] + y), color=(255, 0, 0))
    img.draw_line((int)(self.points2d[2][0] + x), (int)(self.points2d[2][1] + y),
                  (int)(self.points2d[3][0] + x), (int)(self.points2d[3][1] + y), color=(255, 0, 0))
    img.draw_line((int)(self.points2d[3][0] + x), (int)(self.points2d[3][1] + y),
                  (int)(self.points2d[4][0] + x), (int)(self.points2d[4][1] + y), color=(255, 0, 0))
    img.draw_line((int)(self.points2d[4][0] + x), (int)(self.points2d[4][1] + y),
                  (int)(self.points2d[1][0] + x), (int)(self.points2d[1][1] + y), color=(255, 0, 0))

  def rotate(self):
    rotateOut1 = [0] * 3
    rotateOut2 = [0] * 3
    for i in range(0, 5):
      rotateY(self.angle, self.points[i], rotateOut1)
      rotateX(0.1, rotateOut1, rotateOut2)
      zFactor = SHAPE / (2.2 * SHAPE - rotateOut2[2])
      projectOnXY(rotateOut2, self.points2d[i], zFactor)

    self.angle += 0.1

if __name__ == "__main__":

    import lcd
    import time
    import image

    lcd.init(freq=15000000)

    img = image.Image(size=(240, 240))

    cube = Cube()
    tmp = Pyramid()

    while True:
      cube.draw(img, 120, 100)  # erase footpr
      cube.rotate()
      cube.draw(img, 120, 100)  # refresh cube

      tmp.draw(img, 60, 60) # erase footpr
      tmp.rotate()
      tmp.draw(img, 60, 60) # refresh self
      lcd.display(img)

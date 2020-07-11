
# from https://github.com/idea4good/GuiLiteSamples/blob/master/Hello3D/UIcode/UIcode.cpp

import image
import math

# 3D engine


def multiply(m, n, p, a, b, c):  # a[m][n] * b[n][p] = c[m][p]
  for i in range(0, m):
    for j in range(j, p):
      c[i * p + j] = 0
      for k in range(k, n):
        c[i * p + j] += a[i * n + k] * b[k * p + j]


def rotateX(angle, po, output):  # rotate matrix for X

  rotation = [[0, 0, 0]] * 3
  rotation[0][0] = 1
  rotation[1][1] = math.cos(angle)
  rotation[1][2] = 0 - math.sin(angle)
  rotation[2][1] = math.sin(angle)
  rotation[2][2] = math.cos(angle)
  multiply(3, 3, 1, rotation, po, output)


def rotateY(angle, po, output):  # rotate matrix for Y

  rotation = [[0, 0, 0]] * 3
  rotation[0][0] = math.cos(angle)
  rotation[0][2] = math.sin(angle)
  rotation[1][1] = 1
  rotation[2][0] = 0 - math.sin(angle)
  rotation[2][2] = math.cos(angle)
  multiply(3, 3, 1, rotation, po, output)


def rotateZ(angle, po, output):  # rotate matrix for Z

  rotation = [[0, 0, 0]] * 3
  rotation[0][0] = math.cos(angle)
  rotation[0][1] = 0 - math.sin(angle)
  rotation[1][0] = math.sin(angle)
  rotation[1][1] = math.cos(angle)
  rotation[2][2] = 1
  multiply(3, 3, 1, rotation, po, output)


def projectOnXY(po, output, zFactor=1):
  
  projection = [[0, 0, 0]] * 2  # project on X/Y face
  projection[0][0] = zFactor  # the raio of po.z and camera.z
  projection[1][1] = zFactor  # the raio of po.z and camera.z
  multiply(2, 3, 1, projection, po, output)


# SHAPE = 50


# class Pyramid:

#   def __init__(self):
#     self.points2d = [
#         [0, 0],
#         [0, 0],
#         [0, 0],
#         [0, 0],
#         [0, 0],
#     ]

#     self.points = [
#         [0, -SHAPE, 0],  # top
#         [-SHAPE, SHAPE, -SHAPE],
#         [SHAPE, SHAPE, -SHAPE],
#         [SHAPE, SHAPE, SHAPE],
#         [-SHAPE, SHAPE, SHAPE],
#     ]

#   def draw(self, img):
#     img.draw_line(self.points2d[0][0] + x, self.points2d[0][1] + y,
#                   self.points2d[1][0] + x, self.points2d[1][1] + y, color=(255, 0, 0))
#     img.draw_line(self.points2d[0][0] + x, self.points2d[0][1] + y,
#                   self.points2d[2][0] + x, self.points2d[2][1] + y, color=(255, 0, 0))
#     img.draw_line(self.points2d[0][0] + x, self.points2d[0][1] + y,
#                   self.points2d[3][0] + x, self.points2d[3][1] + y, color=(255, 0, 0))
#     img.draw_line(self.points2d[0][0] + x, self.points2d[0][1] + y,
#                   self.points2d[4][0] + x, self.points2d[4][1] + y, color=(255, 0, 0))

#     img.draw_line(self.points2d[1][0] + x, self.points2d[1][1] + y,
#                   self.points2d[2][0] + x, self.points2d[2][1] + y, color=(255, 0, 0))
#     img.draw_line(self.points2d[2][0] + x, self.points2d[2][1] + y,
#                   self.points2d[3][0] + x, self.points2d[3][1] + y, color=(255, 0, 0))
#     img.draw_line(self.points2d[3][0] + x, self.points2d[3][1] + y,
#                   self.points2d[4][0] + x, self.points2d[4][1] + y, color=(255, 0, 0))
#     img.draw_line(self.points2d[4][0] + x, self.points2d[4][1] + y,
#                   self.points2d[1][0] + x, self.points2d[1][1] + y, color=(255, 0, 0))

#   def rotate(self):
#     rotateOut1 = [[0]] * 3
#     rotateOut2 = [[0]] * 3
#     for i in range(0, 5):
#       rotateY(angle, self.points[i], rotateOut1)
#       rotateX(0.1, rotateOut1, rotateOut2)
#       zFactor = SHAPE / (2.2 * SHAPE - rotateOut2[2][0])
#       projectOnXY(rotateOut2, self.points2d[i], zFactor)

#     angle += 0.1


if __name__ == "__main__":

    # theCube.draw(120, 100, true) # erase footpr
    # theCube.rotate()
    # theCube.draw(120, 100, false) # refresh cube

    # theself.draw(120, 250, true) # erase footpr
    # theself.rotate()
    # theself.draw(120, 250, false) # refresh self
    pass

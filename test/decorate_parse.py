
# backup

# def down(down_argument):  # down get "down_argument"
#   print(down, 1, down_argument)  # down get "down_argument"
#   def warp_up(up):
#     print(warp_up, 1, up)  # down get "up_argument"
#     def callback_up(up_argument):  # up_argument > "up_argument"
#         print(callback_up, 1, up_argument)
#         data = up(up_argument)  # call up() > print("up")
#         print(callback_up, 2, data)
#         return data
#     print(warp_up, 2, up)  # down get "up_argument"
#     return callback_up
#   print(down, 2, down_argument)  # down get "down_argument"
#   return warp_up

# """
#   @down("down_argument") 
#   1.down("down_argument") > call warp_up() > return callback_up 
#   2.exec callback_up > @callback_up > up = callback_up(up) 
# """

# @down("down_argument") # "down_argument" > warp_up (down_argument)
# def up(up_argument):
#   print(up, up_argument)
#   return "up_return"

# result = up("up_argument")
# print(result)

'''
# 假设有 4 个布局图像
# 设 1 为背景，2 和 3 互斥且以 1 为底， 4 以 2 为底。
# 则代码设计为如下布局

# 处于 1 的时候，绘图的顺序为 1
# 处于 2 的时候，绘图的顺序为 1 > 2 
# 处于 3 的时候，绘图的顺序为 1 > 3 
# 处于 4 的时候，绘图的顺序为 1 > 2 > 4

# 则代码逻辑为

img1, img2, img3, img4 = 1, 2, 3, 4

def img1_draw():
  print(img1)
img1_draw()

def img2_draw():
  print(img1, img2)
img2_draw()

def img3_draw():
  print(img1, img3)
img3_draw()

def img4_draw():
  print(img1, img2, img4)
img4_draw()

# 以上是预期的输出，如果使用 class 则定义当前类对象和重载基类函数时调用父类绘图在前，类设计引出的对象源头为基类，也就是画布，这不利于分离，后续的人要继承类设计新接口。
# 如果使用装饰的接口设计，目的只需要在引出的绘图操作上，装饰父类的绘图函数，父类同理，自由装饰即可，设计如下。
采用同级多层装饰，而非继承嵌套装饰，不要试图装饰带有装饰器的函数，因为装饰器解释逻辑满足 (B = A(B))() ，如果呈现 (B = A(B))() 和 (C = B(C))() ，则展开为 (C = A(B)(C))()。
'''

img1, img2, img3, img4 = 1, 2, 3, 4

def img1_draw(warp=None):

  print(img1, warp)
  if warp:
    return lambda *args:warp()

def test_img2():

  @img1_draw
  def img2_draw(warp=None):
    print(img2, warp)
    if warp:
      return lambda *args:warp()

  img2_draw()

# test_img2()

def test_img3():

  @img1_draw
  def img3_draw():
    print(img3)

  img3_draw()

test_img3()

def test_img4():

  def img2_draw(warp=None):
    print(img2, warp)
    if warp:
      return lambda *args:warp()

  @img2_draw
  @img1_draw
  def img4_draw():
    print(img4)

  img4_draw()

test_img4()


def use_logging(func):

    def wrapper(*args, **kwargs):
        print(wrapper)
        return func(*args, **kwargs)
    return wrapper

def bar():
    print('i am bar')

bar = use_logging(bar)
bar()

# 以下为错误示范和产生的效果的理解

# def img1_draw(warp=None):
#   print(img1, warp)
#   if warp:
#     def img1_tmp(warp=None):
#       print(img1_tmp, warp)
#       if warp:
#         warp()
#         def img1_ts(warp=None):
#           print(img1_ts, warp)
#           if warp:
#             warp()
#         return img1_ts
#     return img1_tmp

# @img1_draw
# def img2_draw(warp=None):
#   print(img2, warp)
#   if warp:
#     def ts(warp=None):
#       print(ts, warp)
#       if warp:
#         warp()
#     return ts

# tmp = img1_draw(img2_draw)

# # tmp()

# @img2_draw
# # @img1_draw
# def img4_draw():
#   print(img4)

# img2_draw = b = img1_draw(img2_draw) 
# # 要求 b 返回是一个可以展开的装饰器

# t = img2_draw(img4_draw)

# t = (img1_draw(img2_draw))(img4_draw)

# # t()

# img4_draw()

class Square:
   def __init__(self, length, width):
       self.length = length
       self.width = width
   def area(self):
       return self.width * self.length
r = Square(20, 2000)
print(r.area())
print("Rectangle Area: %d" % (r.area()))

def testarea(length, width):
       return length * width

print(testarea(20, 2000))
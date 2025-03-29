import math

class Shape:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def square(self):
        return 0

class Circle(Shape):
    def __init__(self, x, y, radius):
        super().__init__(x, y)
        self.radius = radius

    def square(self):
        return math.pi * self.radius ** 2

class Rectangle(Shape):
    def __init__(self, x, y, height, width):
        super().__init__(x, y)
        self.height = height
        self.width = width

    def square(self):
        return abs(self.width * self.height)

class Parallelogram(Rectangle):
    def __init__(self, x, y, base, height, angle):
        super().__init__(x, y, height, base)
        self.angle = angle

    def square(self):
        return abs(self.width * self.height * math.sin(math.radians(self.angle)))

class Triangle(Shape):
    def __init__(self, x, y, base, height):
        super().__init__(x, y)
        self.base = base
        self.height = height

    def square(self):
        return 0.5 * abs(self.base * self.height)

class Scene:
    def __init__(self):
        self._figures = []

    def add_figure(self, figure):
        self._figures.append(figure)

    def total_square(self):
        return sum(f.square() for f in self._figures)
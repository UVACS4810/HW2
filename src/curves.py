
from src.utils import RGB
from src.vertex import Vertex

import src.vertex as vertex
from src.utils import RGB

def make_permutations(x_initial, x, y_initial, y, color: RGB):
    v1 = Vertex(x_initial + x, y_initial + y, color.red, color.green, color.blue, color.alpha)
    v2 = Vertex(x_initial + x, y_initial - y, color.red, color.green, color.blue, color.alpha)
    v3 = Vertex(x_initial - x, y_initial + y, color.red, color.green, color.blue, color.alpha)
    v4 = Vertex(x_initial - x, y_initial - y, color.red, color.green, color.blue, color.alpha)
    v5 = Vertex(y_initial + y, x_initial + x, color.red, color.green, color.blue, color.alpha)
    v6 = Vertex(y_initial + y, x_initial - x, color.red, color.green, color.blue, color.alpha)
    v7 = Vertex(y_initial - y, x_initial + x, color.red, color.green, color.blue, color.alpha)
    v8 = Vertex(y_initial - y, x_initial - x, color.red, color.green, color.blue, color.alpha)
    
    return [v1, v2, v3, v4, v5, v6, v7, v8]
def draw_circle(x_initial: int, y_initial: int, radius: int, color: RGB) -> "list[vertex.Vertex]":
    x = -1 * radius
    y = 0
    p = 0
    px = -2 * radius + 1
    py = 1
    pxx = 2
    pyy = 2
    output = []
    print(f"x = {x}, y = {y}")
    while y < -x:
        print(f"x = {x}, y = {y}")
        output += make_permutations(x_initial, x, y_initial, y, color)
        y += 1
        p += py
        py += pyy
        if p > 0:
            x += 1
            p += px
            px += pxx
    return output
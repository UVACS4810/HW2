
from src.utils import RGB
from src.vertex import Vertex

import src.vertex as vertex
from src.utils import RGB

def make_permutations(x_initial, x, y_initial, y, color: RGB):
    v1 = Vertex(x_initial + x, y_initial + y, color.red, color.green, color.blue, color.alpha)
    v2 = Vertex(x_initial + x, y_initial - y, color.red, color.green, color.blue, color.alpha)
    v3 = Vertex(x_initial - x, y_initial + y, color.red, color.green, color.blue, color.alpha)
    v4 = Vertex(x_initial - x, y_initial - y, color.red, color.green, color.blue, color.alpha)
    v5 = Vertex(x_initial + y, y_initial + x, color.red, color.green, color.blue, color.alpha)
    v6 = Vertex(x_initial + y, y_initial - x, color.red, color.green, color.blue, color.alpha)
    v7 = Vertex(x_initial - y, y_initial + x, color.red, color.green, color.blue, color.alpha)
    v8 = Vertex(x_initial - y, y_initial - x, color.red, color.green, color.blue, color.alpha)
    
    return [v1, v2, v3, v4, v5, v6, v7, v8]
def draw_circle(x_initial: int, y_initial: int, radius: int, color: RGB) -> "list[vertex.Vertex]":
    x = -1 * radius
    y = 0
    p = -1 * radius - 1
    px = -8 * radius
    py = 4
    pxx = 8
    pyy = 8
    output = []
    while y <= -x:
        output += make_permutations(x_initial, x, y_initial, y, color)
        y += 1
        p += py
        py += pyy
        if p > 0:
            x += 1
            p += px
            px += pxx
    return output

from src.utils import RGB
from src.vertex import Vertex

import src.vertex as vertex
from src.utils import RGB

def make_permutations(x_initial, x, y_inital, y, color: RGB):
    v1 = Vertex(x_initial + x, y_inital + y, color.red, color.green, color.blue, color.alpha)
    
def draw_circle(x_initial: int, y_initial: int, radius: int, color: RGB) -> "list[vertex.Vertex]":
    x = -1 * radius
    y = y_initial
    p = 0
    px = -2 * radius + 1
    py = 1
    pxx = 2
    pxy = 0
    xyy = 2

    while y < -x:
        


import dataclasses

from src.utils import RGB, convert_hex_to_rgb

@dataclasses.dataclass
class Vertex():
    x: float
    y: float
    r: int = 0
    g: int = 0
    b: int = 0
    def __iter__(self):
        return self

def parse_xyrgb(line: "list[str]") -> Vertex:
    x = float(line[1])
    y = float(line[2])
    rgb = [int(line[3]),int(line[4]), int(line[5])]
    return Vertex(x, y, *rgb)


def parse_xyc(line: "list[str]") -> Vertex:
    x = float(line[1])
    y= float(line[2])
    hex = line[3]
    return vertex_from_xyc(x, y, hex)

def vertex_from_xyc(x: float, y: float, hex: str) -> Vertex:
    c: RGB = convert_hex_to_rgb(hex)
    return Vertex(x, y, c.red, c.green, c.blue)

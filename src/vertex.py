
import dataclasses

from src.utils import RGB, convert_hex_to_rgb

@dataclasses.dataclass
class Vertex():
    x: int
    y: int
    c: RGB

def parse_xyrgb(line: "list[str]") -> Vertex:
    x: int = int(line[1])
    y: int = int(line[2])
    rgb = [int(line[3]),int(line[4]), int(line[5])]
    return vertex_from_xyc(x, y, *rgb)

def vertex_from_xyrgb(x: int, y: int, r: int, g: int, b: int) -> Vertex:
    c = RGB(r, g, b)
    return Vertex(x, y, c)

def parse_xyc(line: "list[str]") -> Vertex:
    x: int = int(line[1])
    y: int = int(line[2])
    hex = [int(line[3]),int(line[4]), int(line[5])]
    return vertex_from_xyc(x, y, hex)

def vertex_from_xyc(x: int, y: int, hex: str) -> Vertex:
    c = convert_hex_to_rgb(hex)
    return Vertex(x, y, c)

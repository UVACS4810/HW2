
import dataclasses

from PIL import Image

import src.vertex as vertex
from src.utils import RGB, convert_hex_to_rgb, line_to_list

@dataclasses.dataclass
class ImageInfo():
    """This contains all the the metadata about the image file the program is processing
    \b filename: the name of the output file
    \b width: the with of the output file
    \b height: the height of the output file
    \b is_single_file: true if filename should be used as output filename.
    \b number_of_images: the number of files that will be produced.
    """
    filename: str
    width: int
    height: int
    is_single_file: bool = True
    number_of_images: int = 1

def get_image_info(line: str) -> ImageInfo:
    """parses the first line of the file to get the metadata

    Args:
        line (str): the first line of a file

    Returns:
        ImageInfo: the input file metadata
    """
    line_as_list = line_to_list(line)
    # Set the Image info
    image_info = ImageInfo(
        width=int(line_as_list[1]),
        height=int(line_as_list[2]),
        filename=line_as_list[3],
    )
    # Set the values for the case in which we are making multiple png files
    if line_as_list[0] == "pngs":
        image_info.number_of_images = int(line_as_list[-1])

    return image_info

def dda(i1: vertex.Vertex, i2: vertex.Vertex, step_in_y: bool = False) -> "list[vertex.Vertex]":
    
    if step_in_y
    return None

def parse_line(line: "list[str]", image: Image, vertex_list: "list[vertexs.Vertex]") -> None:
    """
    parse keywords
    1) xyrgb x y r g b: Fill the vertex noted by the x and y coordinate to have the specified color (r, g, b, 255).
    2) xyc x y #rrggbb: Fill the vertex noted by the x and y coordinate to have the specified hex color
    3) lineg i_1 i_2: Linearly interpolates colors on lines
    4) linec i_1 i_2 hexcolorcode: Draw an 8-connected line of the given color using the DDA algorithm between
    the two vertices given. Ignore the colors of the vertices 
    """
    keyword: str = line[0]
    if keyword == "xyrgb":
        # make the vertex
        new_vertex = vertex.parse_xyrgb(line)
        vertex_list.append(new_vertex)
        

    if keyword == "xyc":
        # make the vertex
        new_vertex = vertex.vertex_from_xyc(line)
        vertex_list.append(new_vertex)
    
    if keyword == "lineg":
        # linearly interpolate colors


    # image.im.putpixel((x, y), (rgb.red, rgb.green, rgb.blue, 255))

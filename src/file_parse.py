
import dataclasses
import math

from PIL import Image
from src import utils
import numpy as np

import src.vertex as vertex
from src.utils import RGB, convert_hex_to_rgb, line_to_list, ImageInfo


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

def dda(p1: vertex.Vertex, p2: vertex.Vertex, step_in_y: bool = False) -> "list[vertex.Vertex]":
    # if delta y > delta x then we will step in y, else, step in x
    if not step_in_y:
        step_in_y = abs(p2.x - p1.x) < abs(p2.y - p1.y)
    # make our step value
    p1_list: np.ndarray = np.array(utils.object_to_list(p1))
    p2_list: np.ndarray = np.array(utils.object_to_list(p2))
    # set the step index
    # TODO: Is it ok to assume the first value will always be x and the second value will always be y?
    step_index: int = 1 if step_in_y else 0
    # this is the difference between the two points in all attributes
    delta_p = p2_list - p1_list
    # We need to ensure that we are moving from a lower point to a higher point in our step directio
    if delta_p[step_index] < 0:
        # swap p1, p2
        p1_list, p2_list = p2_list, p1_list
        # delta_p needs to be flipped
        delta_p = delta_p * -1
    # this is the amount that needs to be added to the previous point when we take a step in the step direction
    dp = delta_p / delta_p[step_index]
    # the amount added to the initial point to get to the first int larger in the step direction
    dp0 = (math.ceil(p1_list[step_index]) - p1_list[step_index]) * dp
    # q is our starting point
    q: np.ndarray = p1_list + dp0
    output_list: list[vertex.Vertex] = []
    while q[step_index] < p2_list[step_index]:
        new_vertex: vertex.Vertex = vertex.Vertex(
            *(np.round(q.tolist()).astype(int))
        )
        output_list.append(new_vertex)
        # add the change to the current q
        q = q + dp
    return output_list


def parse_line(line: "list[str]", image: Image, vertex_list: "list[vertex.Vertex]") -> None:
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
        new_vertex = vertex.parse_xyc(line)
        vertex_list.append(new_vertex)
    
    if keyword == "lineg":
        # linearly interpolate colors
        p1 = vertex_list[int(line[1]) - 1]
        p2 = vertex_list[int(line[2]) - 1]
        verts = dda(p1, p2)
        for vert in verts:
            image.im.putpixel((vert.x, vert.y), (vert.r, vert.g, vert.b, 255))
    
    if keyword == "linec":
        p1 = vertex_list[int(line[1]) - 1]
        p2 = vertex_list[int(line[2]) - 1]
        hexcolorcode = line[3]
        c: RGB = convert_hex_to_rgb(hexcolorcode)
        verts = dda(p1, p2)
        for vert in verts:
            image.im.putpixel((vert.x, vert.y), (c.red, c.green, c.blue, 255))
    

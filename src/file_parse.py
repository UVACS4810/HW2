
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

def ndarray_to_vertex(q: np.ndarray) -> vertex.Vertex:
    new_vertex: vertex.Vertex = vertex.Vertex(
            *(np.round(q.tolist()).astype(int))
        )
    return new_vertex

def vertex_to_ndarray(v: vertex.Vertex) -> np.ndarray:
    return np.array(utils.object_to_list(v))

def change_and_starting_position(p1: np.ndarray, p2: np.ndarray, step_in_y: bool = False) -> "list[np.ndarray]":
    delta_p: np.ndarray = p2 - p1
    # if delta y > delta x then we will step in y, else, step in x
    if not step_in_y:
        step_in_y = abs(delta_p[0]) < abs(delta_p[1])
    # set the step index
    # TODO: Is it ok to assume the first value will always be x and the second value will always be y?
    step_index: int = 1 if step_in_y else 0
    # We need to ensure that we are moving from a lower point to a higher point in our step directio
    if delta_p[step_index] < 0:
        # swap p1, p2
        p1, p2 = p2, p1
        # delta_p needs to be flipped
        delta_p = delta_p * -1
    # this is the amount that needs to be added to the previous point when we take a step in the step direction
    if delta_p[step_index] != 0:
        dp = delta_p / delta_p[step_index]
    else:
        dp = np.zeros(delta_p.shape)
    # the amount added to the initial point to get to the first int larger in the step direction
    dp0 = (math.ceil(p1[step_index]) - p1[step_index]) * dp
    # q is our starting point
    q: np.ndarray = p1 + dp0
    return [dp, q]

def dda(p1: np.ndarray, p2: np.ndarray, step_in_y: bool = False) -> "list[np.ndarray]":
    """Takes in two numpy arrays. Assumes that the first and second value in the arrays are
    x and y respectively. Setting the step_in_y flag will make sure the algorithm always 
    choses to step in y.

    Returns:
        np.ndarray: a numpy array where the first value is x and the second value is y
    """
    # this is the difference between the two points in all attributes
    delta_p = p2 - p1
    # if delta y > delta x then we will step in y, else, step in x
    if not step_in_y:
        step_in_y = abs(delta_p[0]) < abs(delta_p[1])
    # set the step index
    # TODO: Is it ok to assume the first value will always be x and the second value will always be y?
    step_index: int = 1 if step_in_y else 0
    # We need to ensure that we are moving from a lower point to a higher point in our step directio
    if delta_p[step_index] < 0:
        # swap p1, p2
        p1, p2 = p2, p1
        # delta_p needs to be flipped
        delta_p = delta_p * -1
    # this is the amount that needs to be added to the previous point when we take a step in the step direction
    if delta_p[step_index] != 0:
        dp = delta_p / delta_p[step_index]
    else:
        dp = np.zeros(delta_p.shape)
    # the amount added to the initial point to get to the first int larger in the step direction
    dp0 = (math.ceil(p1[step_index]) - p1[step_index]) * dp
    # q is our starting point
    q: np.ndarray = p1 + dp0
    output_list: list[vertex.Vertex] = []
    while q[step_index] < p2[step_index]:
        output_list.append(q)
        # add the change to the current q
        q = q + dp
    return output_list

def triangle_fill(p1: vertex.Vertex, p2: vertex.Vertex, p3: vertex.Vertex) -> "list[np.ndarray]":
    # The first step is to order to 3 vertexes by their y coordinate.
    a = [p1, p2, p3]
    a.sort(key=lambda v: v.y)
    # convert a to a list of ndarrays
    a = list(map(vertex_to_ndarray, a))
    # bottom, middle, top
    pb, pm, pt = a
    # Find d~p and initial ~q for (~pb, ~pm); call them d~qa and ~qa
    dqa, qa = change_and_starting_position(pb, pm, True)
    # Find d~p and initial ~q for (~pb, ~pt); call them d~qc and ~qc
    dqc, qc = change_and_starting_position(pb, pt, True)
    output = []
    while qa[1] < pm[1]:
        output += dda(qa, qc)
        qa = qa + dqa
        qc = qc + dqc
    # Find d~p and initial ~q for (~pm, ~pt); call them d~qe and ~qe
    dqe, qe = change_and_starting_position(pm, pt, True)
    while qe[1] < pt[1]:
        output += dda(qe, qc)
        qe = qe + dqe
        qc = qc + dqc
    
    output = list(map(ndarray_to_vertex, output))
    return output

def dda_on_vertex(p1: vertex.Vertex, p2: vertex.Vertex, step_in_y: bool = False) -> "list[vertex.Vertex]":
    p1_list: np.ndarray = np.array(utils.object_to_list(p1))
    p2_list: np.ndarray = np.array(utils.object_to_list(p2))
    dda_result = dda(p1_list, p2_list, step_in_y)
    output = list(map(ndarray_to_vertex, dda_result))
    return output

def parse_line(line: "list[str]", image: Image, vertex_list: "list[vertex.Vertex]") -> None:
    """
    parse keywords
    1) xyrgb x y r g b: Fill the vertex noted by the x and y coordinate to have the specified color (r, g, b, 255).
    2) xyc x y #rrggbb: Fill the vertex noted by the x and y coordinate to have the specified hex color
    3) lineg i_1 i_2: Linearly interpolates colors on lines
    4) linec i_1 i_2 hexcolorcode: Draw an 8-connected line of the given color using the DDA algorithm between
    the two vertices given. Ignore the colors of the vertices 
    5) trig i_1, i_2, i_3: Fill a triangle between the given vertices,
    linearly interpolating the vertex colors as you go
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
    
    if keyword == "trig":
        i1 = vertex_list[int(line[1]) - 1]
        i2 = vertex_list[int(line[2]) - 1]
        i3 = vertex_list[int(line[3]) - 1]
        verts = triangle_fill(i1, i2, i3)
        for vert in verts:
            image.im.putpixel((vert.x, vert.y), (vert.r, vert.g, vert.b, 255))

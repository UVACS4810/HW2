import dataclasses
from typing import Any

from PIL import Image


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

@dataclasses.dataclass
class RGB():
    red: int
    green: int
    blue: int
    alpha: int = 255
    def __add__(self, other):
        return RGB(
            min((self.red + other.red), 255),
            min((self.green + other.green), 255),
            min((self.blue + other.blue), 255),
            min((self.alpha + other.alpha), 255),
        )

def over_operator(ca: int, cb: int, aa: int, ab, a0: int) -> int:
    return round((ca * aa + cb*ab*(1-aa))/a0)

def add_pixel_colors(a: RGB, b: RGB) -> RGB:
    """Used to compute the new color of two pixels with alpha values. Uses the over
    operator to acomplish this

    Args:
        a (RGB): the over color
        b (RGB): the under color

    Returns:
        RGB: the new pixel color
    """
    aa = a.alpha/255
    ab = b.alpha/255
    a0 = aa + ab * (1-(aa))

    r = over_operator(a.red, b.red, aa, ab, a0)
    g = over_operator(a.green, b.green, aa, ab, a0)
    b = over_operator(a.blue, b.blue, aa, ab, a0)

    a0 = round(a0*255)
    return RGB(r, g, b, a0)

def convert_hex_to_rgb(hex: str) -> RGB:
    # we will get the "hex" value in the form "#rrggbb"
    # The first step will be to strip the "#" char.
    hex = hex.strip("#")
    # Next we will seperate the string into "rr" "gg" "bb"
    # Convert the values into integers
    rr = int(hex[0:2], base=16)
    gg = int(hex[2:4], base=16)
    bb = int(hex[4:6], base=16)
    aa = 255
    if len(hex) > 6:
        aa = int(hex[6:8], base=16)
    # store the values in an RGB class
    return RGB(rr, gg, bb, aa)

def line_to_list(line: str) -> "list[str]":
    # remove whitespace
    line.strip()
    return line.split()

def object_to_list(object) -> "list[Any]":
    vars_dict: dict = vars(object)
    output_list = []
    for key, val in vars_dict.items():
        if dataclasses.is_dataclass(val):
            vars_dict[key] = object_to_list(val)
            for item in object_to_list(val):
                output_list.append(item)
        else:
            output_list.append(val)
    return output_list


### STUFF FOR ARG PARSING ###
@dataclasses.dataclass
class CmdLineArgs():
    file: str

def parse_args(args: list) -> CmdLineArgs:
    return CmdLineArgs(file = args[1])

def make_filename_list(image_info: ImageInfo) -> "list[str]":
    # List of names for image files
    names_list = []
    if image_info.is_single_file:
        names_list.append(image_info.filename)
    else:
        for i in range(image_info.number_of_images):
            name = image_info.filename + f"{i:03d}" + ".png"
            names_list.append(name)
    return names_list


### MAKING IMAGES ###
def make_images(image_info: ImageInfo) -> list:
    images = []
    for _ in range(image_info.number_of_images):
        image = Image.new("RGBA", (image_info.width, image_info.height), (0,0,0,0))
        images.append(image)
    return images
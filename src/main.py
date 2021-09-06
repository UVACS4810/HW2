import sys

from PIL import Image
import dataclasses

import src.file_parse as file_parse
from src.utils import line_to_list

@dataclasses.dataclass
class CmdLineArgs():
    file: str

def parse_args(args: list) -> CmdLineArgs:
    return CmdLineArgs(file = args[1])

def make_filename_list(image_info: file_parse.ImageInfo) -> "list[str]":
    # List of names for image files
    names_list = []
    if image_info.is_single_file:
        names_list.append(image_info.filename)
    else:
        for i in range(image_info.number_of_images):
            name = image_info.filename + f"{i:03d}" + ".png"
            names_list.append(name)
    return names_list

def make_images(image_info: file_parse.ImageInfo) -> list:
    images = []
    for _ in range(image_info.number_of_images):
        image = Image.new("RGBA", (image_info.width, image_info.height), (0,0,0,0))
        images.append(image)
    return images

# Main method
if __name__ == "__main__":
    # get the file name
    args = sys.argv
    cmnd_line_args = parse_args(args)

    # open the file
    with open(cmnd_line_args.file, "r") as file:
        lines = file.readlines()
        # Read the first line to determine meta info about the file
        first_line: str
        if lines:
            first_line = lines[0]
        else:
            print("not enough lines")
            raise
        
        # Get the image info from the first line
        image_info = file_parse.get_image_info(first_line)
        # Make array of images
        images = make_images(image_info)
        image_filenames = make_filename_list(image_info)
        currently_eddited_image_index = 0
        if len(lines) > 1:
            for i in range(1, len(lines)):
                line = line_to_list(lines[i])
                # If the keywword is "frame", we move to edit the frame specified
                if line[0] == "frame":
                    currently_eddited_image_index = int(line[1])
                else:
                    file_parse.parse_line(line, images[currently_eddited_image_index])

        assert(len(image_filenames) == len(images))
        # Save each of the files
        for i in range(len(image_filenames)):
            images[i].save(image_filenames[i])

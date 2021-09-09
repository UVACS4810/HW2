from src.vertex import Vertex
import sys

from PIL import Image
import dataclasses

import src.file_parse as file_parse
import src.utils as utils


# Main method
if __name__ == "__main__":
    # get the file name
    args = sys.argv
    cmnd_line_args = utils.parse_args(args)

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
        images = utils.make_images(image_info)
        image_filenames = utils.make_filename_list(image_info)
        currently_eddited_image_index = 0
        vertex_list: "list[Vertex]" = []
        if len(lines) > 1:
            for i in range(1, len(lines)):
                line = utils.line_to_list(lines[i])
                # If the line is empty, do nothing
                if not line:
                    pass
                # If the keywword is "frame", we move to edit the frame specified
                elif line[0] == "frame":
                    currently_eddited_image_index = int(line[1])
                    vertex_list.clear()
                else:
                    file_parse.parse_line(line, images[currently_eddited_image_index], vertex_list)

        assert(len(image_filenames) == len(images))
        # Save each of the files
        for i in range(len(image_filenames)):
            images[i].save(image_filenames[i])

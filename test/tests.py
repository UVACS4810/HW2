import unittest
import src.main as main
import src.vertex as vertex
import src.file_parse as file_parse
import src.utils as utils

class Test(unittest.TestCase):
    def test_make_filename_list(self):
        # case with one image
        expected = ["whatnot.png"]
        image_info = file_parse.ImageInfo(filename="whatnot.png", width=1, height=1)
        self.assertEqual(expected, main.make_filename_list(image_info=image_info))

        expected = ["whatnot000.png"]
        image_info.filename="whatnot"
        image_info.number_of_images= len(expected)
        image_info.is_single_file = False
        self.assertEqual(expected, main.make_filename_list(image_info=image_info))

        # case with 5 images
        expected = [
            "whatnot000.png",
            "whatnot001.png",
            "whatnot002.png",
            "whatnot003.png",
            "whatnot004.png",
        ]
        image_info.number_of_images = len(expected)
        actual = main.make_filename_list(image_info=image_info)
        self.assertEqual(expected, actual)

class TestVertex(unittest.TestCase):
    def test_point_class(self):
        hex_val = "#ff0000" # this hex converts to 255, 0, 0
        r = 255
        g, b, x, y = 0, 0, 0, 0
        p1 = vertex.vertex_from_xyrgb(x, y, r, g, b)
        p2 = vertex.vertex_from_xyc(x, y, hex_val)
        self.assertEqual(p1, p2)
        
class TestUtils(unittest.TestCase):
    def test_convert_hex_to_rgb(self):
        hex_color = "#aaaaff"
        rgb: utils.RGB = utils.RGB(170, 170, 255)
        self.assertEqual(utils.convert_hex_to_rgb(hex_color), rgb)

class TestFileParse(unittest.TestCase):
    def test_line_to_list(self):
        expected = ["xyrgb", "6" ,"3", "0", "0", "0"]
        lines: list(str) = [
            'xyrgb 6 3   0 0 0',
            "xyrgb 6 3 0 0 0",
            "   xyrgb 6 3 0 0      0",
            "xyrgb 6 3 0 0 0        ",
            "    xyrgb 6 3 0 0 0        ",
        ]
        for line in lines:
            out = file_parse.line_to_list(line)
            self.assertEqual(out, expected)
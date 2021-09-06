First homework assignment for CS 4810

Markdown taken from class website

All code is my own.

What is Coded
==============

Reading Input
-----------------

Each file will have a number of lines; each line will have a keyword first, followed by zero or more extra pieces of information separated by whitespace (some mix of `' '` and `'\t'`). Lines should be read in order, first to last, because some lines refer to the lines above them.

Ignore blank lines and lines starting with anything other than a keyword you know. Always strip leading and trailing space from a line before parsing it.

In this assignment input files might look like

    png 200 300 outfilename.png
    xy 10 20
    
    xyrgb 50 50   255 127 0
    ignore this line since "ignore" is not a keyword you know 
    likewise ignore this line, which also starts with an unknown keyword
    xyc     150   250 #ff00ee

You do not need to have error checking code. For example, if a `png` keyword is not followed by exactly two positive integers and one string ending .png, your code is welcome to break in any way you wish.

### Keywords

Each homework will define its own set of keywords. For HW0, these are:

png _width_ _height_ _filename_

Every file will begin with either `png` or `pngs`

`png` will be followed by two positive integers, _width_ and _height_, and a _filename_. You should write a RGBA png image of the specified width and height (see \[Image file creation\]). You should write the file in the default directory. The initial color of every pixel in the image should be transparent black (0, 0, 0, 0).

You may assume the filename contains only non-whitespace ASCII characters and already has the appropriate .png ending.

pngs _width_ _height_ _filename_ _frames_

Every file will begin with either `png` or `pngs`

`pngs` will be followed by two positive integers, _width_ and _height_; a base _filename_; and a number of _frames_ to generate. Your should write _frames_ distinct RGBA png images of the specified width and height in the default directory. Each should be named _filename_ followed by a 3-digit number between 000 and _frames_ with a `.png` ending.

If an input file begins `pngs 20 30 whatnot 12` your program will create twelve separate PNG files: `whatnot000.png`, `whatnot001.png`, … `whatnot011.png`.

The initial color of every pixel in the image should be transparent black (0, 0, 0, 0).

You may assume the filename contains only non-whitespace ASCII characters.

frame _t_

`frame` commands will only appear in files beginning `pngs`, not files beginning `png`. They specify that the subsequent commands should be applied to the given frame _t_, which will be an integer between 0 and the number of frames given on the `pngs` line.

`frame` lines will be given in increasing order: `frame 3` will never appear after `frame 4`. Some frames may be skipped, meaning that image should remain its initial color. If drawing commands appear before the first `frame`, they apply to frame 0.

xy _x_ _y_

Fill the pixel noted by the _x_ and _y_ coordinate to be opaque white (255, 255, 255, 255). `xy 0 0` should fill the top left corner pixel. If the image is 200 wide and 300 tall, then `xy 199 299` would fill the bottom right pixel.

You may assume _x_ and _y_ are integers within the image bounds.

xyrgb _x_ _y_ _r_ _g_ _b_

Fill the pixel noted by the _x_ and _y_ coordinate to have the specified color (_r_, _g_, _b_, 255).

You may assume _r_, _g_, and _b_ are integers between 0 and 255, inclusive. See the discussion of `xy` for comments on _x_ and _y_.

xyc _x_ _y_ _hexColorString_

Fill the pixel noted by the _x_ and _y_ coordinate to have the specified color. The color is given in a web-standard 3-byte hex code: `#rrggbb`, where `rr` is a two-digit hexidecimal value for red, `gg` for green, and `bb` for blue. Set the alpha to 255 (0xff)

You may assume _hexColorString_ is always a seven-character string of the appropriate format. See the discussion of `xy` for comments on _x_ and _y_.

## Running the code

To run the program, use the command
```shell
$ make run file=inputfilename.txt
```
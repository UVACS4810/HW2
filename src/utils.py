import dataclasses

@dataclasses.dataclass
class RGB():
    red: int
    green: int
    blue: int

def convert_hex_to_rgb(hex: str) -> RGB:
    # we will get the "hex" value in the form "#rrggbb"
    # The first step will be to strip the "#" char.
    hex = hex.strip("#")
    # Next we will seperate the string into "rr" "gg" "bb"
    # Convert the values into integers
    rr = int(hex[0:2], base=16)
    gg = int(hex[2:4], base=16)
    bb = int(hex[4:6], base=16)
    # store the values in an RGB class
    return RGB(rr, gg, bb)

def line_to_list(line: str) -> "list[str]":
    # remove whitespace
    line.strip()
    return line.split()
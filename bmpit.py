#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2014 Cédric Picard
#
# LICENSE
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
# END_OF_LICENSE
#
# See http://crucialsecurityblog.harris.com/
# Does not work well on big files

"""
Usage: bmpit.py [-h] [-H height] [-W width] [-o offset] INPUT [OUTPUT]

Arguments:
    INPUT            The file to bmp
    OUTPUT           Output file, default is it.bmp

Options:
    -h, --help       Print this help and exit
    -H height        Height in pixel
    -W width         Width in pixel
    -o offset        Offset reading the source file in bytes
"""


import os
import struct
from binascii import unhexlify
from docopt import docopt


def header(size, width, heigth):
    ID = "BM"
    #size                  # 26 is header size + pre-header size
    #reserved
    img_offset = 42        # where the image can be found
    header_size = 12       # BITMAPCOREHEADER
    #width
    #heigth
    nb_color_planes = 1    # always 1
    nb_bits_per_color = 1  # 1, 2, 4 or 8

    header = bytes(ID.encode("utf8"))
    header+= nb2bytes(size, 4)
    header+= bytes(4)
    header+= nb2bytes(img_offset, 4)
    header+= nb2bytes(header_size, 4)
    header+= nb2bytes(width, 2)
    header+= nb2bytes(heigth, 2)
    header+= nb2bytes(nb_color_planes, 2)
    header+= nb2bytes(nb_bits_per_color, 2)

    return header


def nb2bytes(number, length):
    width = number.bit_length()
    width += 8 - ((width % 8) or 8)
    fmt = '%%0%dx' % (width // 4)
    s = unhexlify(fmt % number)
    s = b'\00' * (length - len(s)) + s
    return s[::-1] # little-endian

def main():
    args = docopt(__doc__)

    offset = 0
    if args["-o"]:
        offset = int(args["-o"])

    size = os.path.getsize(args["INPUT"]) - offset

    width = 888
    if args["-W"]:
        width = int(args["-W"])

    heigth = 8*size//width
    if args["-H"]:
        heigth = int(args["-H"])

    output_file = "./it.bmp"
    if args["OUTPUT"]:
        output_file = args["OUTPUT"]

    with open(args["INPUT"], "rb") as fi, open(output_file, "wb") as fo:
        fi.read(offset)
        fo.write(header(size, width, heigth))
        fo.write(fi.read())


if __name__ == "__main__":
    main()

import imageio as iio
import argparse
from PIL import Image
import numpy as np
import os

def main():

    pix_list  = []
    rowcnt    = 0
    colscnt   = 0
    channels  = 3
    skipcount = 60

    outfile  = "out.png"

    parser = argparse.ArgumentParser(prog='cinetone', description='A python CLI tool for generating a color palette from a given input video', epilog='')
    parser.add_argument("-o","--output",help="Places the output in the specified file")
    parser.add_argument("-sc","--skipcount",help="Specifies the frames to skip while processing. Default value is 50",type=int)
    parser.add_argument("video_file", help="Path to the video file to be decoded")
    args = parser.parse_args()

    if not os.path.isfile(args.video_file):
        print("Given path is not a file!")
        return

    if(args.output):
        outfile = args.output

    if(args.skipcount):
        skipcount = args.skipcount

    for index,frame in enumerate(iio.imiter(args.video_file)):
        if( index % skipcount != 0):
            continue

        if rowcnt == 0 or colscnt == 0:
            rowcnt = frame.shape[0]
            colscnt = frame.shape[1]

        rgb = [0] * channels

        flattened_img = np.resize(frame, (rowcnt*colscnt, 3))
        for index in range(channels):
            rgb[index] = int(flattened_img[:,index].mean())

        pix_list.append((rgb[0], rgb[1], rgb[2]))

    im = Image.new(mode="RGB",size=(len(pix_list),1))
    im.putdata(pix_list)
    im = im.resize((480,360),resample=Image.Resampling.NEAREST)
    im.save(outfile)
from PIL import Image
import imageio
import numpy as np
import os
import argparse

def main():

    parser = argparse.ArgumentParser(description='turn frames into video')
    parser.add_argument('frame_dir', help='frame directory')
    parser.add_argument('saved_video_file', help='directory to save video in')
    parser.add_argument('number_of_frames', help='number of frames required in video')
  
    args, other_args = parser.parse_known_args()

    ims=[]
    print(100000+int(args.number_of_frames))
    for i in range(100025,(100000+int(args.number_of_frames))):
        im = Image.open(str(args.frame_dir)+str(i)+r".png")
        ims.append(im)
    imageio.mimwrite(str(args.saved_video_file), ims , fps = 30)

if __name__ == "__main__":
    main()
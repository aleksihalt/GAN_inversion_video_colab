from PIL import Image
import os
import argparse

def main():
    
    parser = argparse.ArgumentParser(description='Adjust video frame dimensions for inputting into model')
    parser.add_argument('frame_dir', help='frame directory')
    parser.add_argument('height', default=1024, help='height required by the model (1024 for face generating stylegan)')
    parser.add_argument('width', default=1024, help='width required by the model (1024 for face generating stylegan)')
    parser.add_argument('crop_x0', default=0, help='crop dimensions required by the model such as x0=420, y0=0, x1=1500, y1=1080]')
    parser.add_argument('crop_y0', default=0, help='crop dimensions required by the model such as x0=420, y0=0, x1=1500, y1=1080]')
    parser.add_argument('crop_x1', default=1080, help='crop dimensions required by the model such as x0=420, y0=0, x1=1500, y1=1080]')
    parser.add_argument('crop_y1', default=720, help='crop dimensions required by the model such as x0=420, y0=0, x1=1500, y1=1080]')
    args, other_args = parser.parse_known_args()

    size = int(args.height), int(args.width)
    directory = os.fsencode(str(args.frame_dir))
    for i in os.listdir(directory):
        im = Image.open(args.frame_dir+str(i.decode('utf-8')))
	#   if args.crop is not False:
        im_cropped = im.crop((int(args.crop_x0),int(args.crop_y0),int(args.crop_x1),int(args.crop_y1)))
        im_resized = im_cropped.resize(size, Image.ANTIALIAS)
        im_resized = im_cropped.resize(size, Image.ANTIALIAS)
        im_resized.save(str(args.frame_dir)+str(i.decode('utf-8')))
		#else:
		#im_resized = im.resize(size, Image.ANTIALIAS)
		#im_resized.save(str(args.frame_dir)+str(i.decode('utf-8')))

if __name__ == "__main__":
    main()
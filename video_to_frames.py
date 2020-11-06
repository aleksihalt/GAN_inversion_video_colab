import cv2
import numpy as np
import matplotlib.pyplot as plt
import shutil
import argparse


def main():
    
    parser = argparse.ArgumentParser(description='Find latent representation of reference images using perceptual loss')
    parser.add_argument('video_dir', help='Directory with video input')
    parser.add_argument('target_dir', help='target directory for extracted frame image files')

    args, other_args = parser.parse_known_args()

    cap= cv2.VideoCapture(args.video_dir)
    i=0
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == False:
            break
        cv2.imwrite(args.target_dir+str(100000+i)+r'.png',frame)
        #f'{args.target_dir}frame100000{i}.png'
        i+=1
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
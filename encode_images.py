import os
import argparse
import pickle
from tqdm import tqdm
import PIL.Image
import numpy as np
import dnnlib
import dnnlib.tflib as tflib
import pretrained_networks
import shutil
from encoder.generator_model import Generator
from encoder.perceptual_model import PerceptualModel


def split_to_batches(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]


def main():
    parser = argparse.ArgumentParser(description='Find latent representation of reference images using perceptual loss')
    parser.add_argument('src_dir', help='Directory with images for encoding')
    parser.add_argument('generated_images_dir', help='Directory for storing generated images')
    parser.add_argument('dlatent_dir', help='Directory for storing dlatent representations')
    parser.add_argument('init_dlatent', default=False, help='path to init dlatent or False')
    parser.add_argument('move_to_folder', default=False, help='path to init dlatent or False')
    parser.add_argument('-it', '--iterations', default=10, help='Number of optimization steps for each batch', type=int)
    parser.add_argument('reset', default=0, help='same dlatent for every frame', type=int)

    parser.add_argument('--network_pkl', default='gdrive:networks/stylegan2-ffhq-config-f.pkl', help='Path to local copy of stylegan2-ffhq-config-f.pkl')

    # for now it's unclear if larger batch leads to better performance/quality
    parser.add_argument('--batch_size', default=1, help='Batch size for generator and perceptual model', type=int)

    # Perceptual model params
    parser.add_argument('--image_size', default=256, help='Size of images for perceptual model', type=int)
    parser.add_argument('--lr', default=1., help='Learning rate for perceptual model', type=float)
 

    # Generator params
    parser.add_argument('--randomize_noise', default=False, help='Add noise to dlatents during optimization', type=bool)
    args, other_args = parser.parse_known_args()

    ref_images = [os.path.join(args.src_dir, x) for x in os.listdir(args.src_dir)]
    ref_images = list(filter(os.path.isfile, ref_images))

    if len(ref_images) == 0:
        raise Exception('%s is empty' % args.src_dir)

    os.makedirs(args.generated_images_dir, exist_ok=True)
    os.makedirs(args.dlatent_dir, exist_ok=True)

    # Initialize generator and perceptual model
    tflib.init_tf()
    generator_network, discriminator_network, Gs_network = pretrained_networks.load_networks(args.network_pkl)
    generator = Generator(Gs_network, args.batch_size, randomize_noise=args.randomize_noise)
    #if args.cont != False:
    print("CONTINUING FROM PREVIOUS DLATENT")
    generator.define_dlatents(args.init_dlatent)
   #else:
       #generator.set_dlatents(generator.initial_dlatents)
    
    perceptual_model = PerceptualModel(args.image_size, layer=9, batch_size=args.batch_size)
    perceptual_model.build_perceptual_model(generator.generated_image)



    # Optimize (only) dlatents by minimizing perceptual loss between reference and generated images in feature space
    for images_batch in tqdm(split_to_batches(ref_images, args.batch_size), total=len(ref_images)//args.batch_size):
        names = [os.path.splitext(os.path.basename(x))[0] for x in images_batch]
        perceptual_model.set_reference_images(images_batch)
        op = perceptual_model.optimize(generator.dlatent_variable, iterations=args.iterations, learning_rate=args.lr)
        pbar = tqdm(op, leave=False, total=args.iterations)
        for loss in pbar:
            pbar.set_description(' '.join(names)+' Loss: %.2f' % loss)
        print(' '.join(names), ' loss:', loss)
        #commented out for colab
        shutil.move(str(args.src_dir)+"/"+str(names[0])+r".png", str(args.move_to_folder)+"/"+str(names[0])+r".png")

        # Generate images from found dlatents and save them
 
        generated_images = generator.generate_images()
        generated_dlatents = generator.get_dlatents()
        for img_array, dlatent, img_name in zip(generated_images, generated_dlatents, names):
            img = PIL.Image.fromarray(img_array, 'RGB')
            img.save(os.path.join(args.generated_images_dir, f'{img_name}.png'), 'PNG')
            np.save(os.path.join(args.dlatent_dir, f'{img_name}.npy'), dlatent)

        #finally OPTIONAL step: reset dlatent to original reference dlatent
        if args.reset == 1:
            generator.define_dlatents(args.init_dlatent)
        else:
            pass
       


if __name__ == "__main__":
    main()

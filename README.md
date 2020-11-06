# GAN inversion for video manipulation
This repository is a hacked version of https://github.com/rolux/stylegan2encoder. To map images into latent space please refer to the aforementioned repository.

## Demonstration of manipulated video: https://vimeo.com/466248675

## Instructions for video manipulation:

`pip install tensorflow-gpu==1.14`  
  
`cd GAN_inversion_video`  

### Convert video to image frames by running: 
`python video_to_frames.py [path to input video] [path to save images]`  
FOR EXAMPLE  
`python video_to_frames.py myvideo.mp4 my_video_frames/`  

### Crop and resize image frames to match model requirement by running:
`python frame_preprocessing.py [image directory] [required height] [required width] [crop x min] [crop y min] [crop x max] [crop y max]`  
FOR EXAMPLE for iPhone video resolution 1920x1080 adjusted for styleGAN2 face generating model requiring 1024x1024 images run:  
`python frame_preprocessing.py my_video_frames/ 1024 1024 420 0 1500 1080`  

### Initialise video 
In order to run video frames through the inverted GAN, you must have a starting sample image (for example a face, or whatever you wish the video to resemble)  
`python encode_images_init.py [sample image] [directory to save images in] [directory to save latent vector .npy files]`  
FOR EXAMPLE  
`python encode_images_init.py img001.png my_initial_frame/ latent_representations/`  
### Run for rest of the video
`python encode_images.py [directory of frames] [directory to save generated frames] [directory of latent vectors] [.npy initial latent vector file] [directory to move frames afterwards] [number of loss function iterations]`  
FOR EXAMPLE  
`python encode_images.py my_video_frames/ generated_frames/ latent_representations/ latent_representations/img001.npy done_frames/ 10`  

### Turn generated frames into video
`python frames_to_video.py [frame directory] [target video file] [number of frames in video]`  
FOR EXAMPLE  
`python frames_to_video.py generated_frames/ myVideo.mp4 300`  
  
    

Requirements same as for using StyleGAN2:  
  
## Requirements (copied from StyleGAN2 repository https://github.com/NVlabs/stylegan2)  

* Both Linux and Windows are supported. Linux is recommended for performance and compatibility reasons.
* 64-bit Python 3.6 installation. We recommend Anaconda3 with numpy 1.14.3 or newer.
* TensorFlow 1.14 or 1.15 with GPU support. The code does not support TensorFlow 2.0.
* On Windows, you need to use TensorFlow 1.14 &mdash; TensorFlow 1.15 will not work.
* One or more high-end NVIDIA GPUs, NVIDIA drivers, CUDA 10.0 toolkit and cuDNN 7.5. To reproduce the results reported in the paper, you need an NVIDIA GPU with at least 16 GB of DRAM.
* Docker users: use the [provided Dockerfile](./Dockerfile) to build an image with the required library dependencies.

StyleGAN2 relies on custom TensorFlow ops that are compiled on the fly using [NVCC](https://docs.nvidia.com/cuda/cuda-compiler-driver-nvcc/index.html). To test that your NVCC installation is working correctly, run:

```.bash
nvcc test_nvcc.cu -o test_nvcc -run
| CPU says hello.
| GPU says hello.
```

On Windows, the compilation requires Microsoft Visual Studio to be in `PATH`. We recommend installing [Visual Studio Community Edition](https://visualstudio.microsoft.com/vs/) and adding into `PATH` using `"C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Auxiliary\Build\vcvars64.bat"`.


# Please refer to the following repositories for more information:
### styleGAN2 https://github.com/NVlabs/stylegan2
### styleGAN2 encoder https://github.com/rolux/stylegan2encoder
### styleGAN encoder https://github.com/Puzer/stylegan-encoder
# GAN_inversion_video_colab

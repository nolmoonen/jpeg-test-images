# Performance

Images are "The new test images" from [imagecompression.info](http://imagecompression.info/test_images/). This directory contains JPEG images encoded using different JPEG encoders:

- libjpeg-turbo version 2.1.5 (build 20240408) using default settings (quality 75, 4:2:0, sequential, no Huffman optimization).
- [nvJPEG](https://developer.nvidia.com/nvjpeg) 12.9 with quality 70, 4:4:4, and optimized Huffman (see `cjpeg_nvjpeg.cpp`).
- [stb](https://github.com/nothings/stb) v.1.16 with quality 90 (see `cjpeg_stb.cpp`).
- TODO add <https://github.com/google/guetzli>
- TODO add <https://github.com/google/jpegli>

# Performance

Images are "The new test images" from [imagecompression.info](http://imagecompression.info/test_images/). This directory contains JPEG images encoded using different JPEG encoders:

- libjpeg-turbo version 2.1.5 (build 20240408) using default quality 75, default subsampling 4:2:0, sequential/progressive, Huffman optimization on.
- [nvJPEG](https://developer.nvidia.com/nvjpeg) 12.9 with default quality 70, 4:4:4, sequential/progressive, optimized Huffman on (see `cjpeg_nvjpeg.cpp`).
- [stb](https://github.com/nothings/stb) v.1.16 with quality 90 and default subsampling 4:2:0 (see `cjpeg_stb.cpp`).
- [jpegli](https://github.com/google/jpegli) `e2320820` (May 2026) with default subsampling 4:4:4, default quality 90 and progressive level 2.
- [MozJPEG](https://github.com/mozilla/mozjpeg) v4.1.1 using default settings (progressive and several optimization features).

## Notes
- [Guetzli](https://github.com/google/guetzli) is not used as it is discontinued and extremely slow to encode.

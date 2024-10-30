# jpeg-test-images

A set of JPEG images produced by different sources for testing and benchmarking.

- `039mp-building.jpg`
  - 7216x5412, 4:2:0 (2x2), baseline DCT
  - Compressed with libjpeg-turbo version 2.1.2, `cjpeg -outfile 039mp-building.jpg big_building.ppm`. Using default quality of 75.
  - Author: "The new test images" from [imagecompression.info](http://imagecompression.info/test_images/).
- `028mp-tree.jpg`
  - 6088x4550, 4:2:0 (2x2), baseline DCT
  - Compressed with [stb](https://github.com/nothings/stb), see [programs/cjpeg_stb.cpp](programs/cjpeg_stb.cpp). Using quality 90.
  - Author: "The new test images" from [imagecompression.info](http://imagecompression.info/test_images/).
- `026mp-temple.jpg`
  - 6240x4160, 4:2:2 (2x1), baseline DCT
  - Produced with Fujifilm X-T3
  - Author: [Max Crone](https://maxcrone.org/photo/kyoto-temple/), CC BY 4.0.
- `012mp-bus.jpg`
  - 4032x3024, 4:2:0 (2x2), baseline DCT
  - Produced with Apple iPhone 11
  - Author: Nol Moonen, CC0.
- `006mp-cathedral.jpg`
  - 2000x3008, 4:4:4 (1x1), baseline DCT
  - Compressed with [nvJPEG](https://developer.nvidia.com/nvjpeg), see [programs/cjpeg_nvjpeg.cpp](programs/cjpeg_nvjpeg.cpp). Using default quality of 70 and optimized Huffman coding.
  - Author: "The new test images" from [imagecompression.info](http://imagecompression.info/test_images/).

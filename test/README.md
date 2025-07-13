# Test

Test suite for JPEG testing sub-sampling factors, scan configurations, and restart intervals.

`img.ppm` is generated from `artifact.ppm` from `rgb16bit.zip` using `convert artificial.ppm -resize 95x63 img.ppm`. The idea is to use a small file (since many files will be generated), but still have multiple MCUs per file. The JPEG files in this directory were generated using `./generate.py img.ppm`.

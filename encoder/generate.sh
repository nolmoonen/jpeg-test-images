#!/usr/bin/env bash

for i in images/*.ppm; do
    name=$(basename $i .ppm) 
    echo $name;
    cjpeg -optimize -outfile $name.libjpeg.seq.jpg $i;
    cjpeg -optimize -progressive -outfile $name.libjpeg.prog.jpg $i;
    ../programs/cjpeg_nvjpeg $i;
    ../programs/cjpeg_nvjpeg -progressive $i;
    ../programs/cjpeg_stb $i
    ../../jpegli/build/tools/cjpegli $i $name.jpegli.jpg;
    ../../mozjpeg/build/cjpeg -outfile $name.mozjpeg.jpg $i;
done

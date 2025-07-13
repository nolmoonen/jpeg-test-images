#!/usr/bin/env bash

for i in images/*.ppm; do
    echo $i;
    cjpeg -outfile $i.libjpeg.jpg $i;
done

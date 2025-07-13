#!/usr/bin/env bash

for i in *.ppm; do
    cjxl --distance 0 --effort 10 $i $i.jxl;
    # Check that the file can be restored bit-by-bit.
    djxl $i.jxl $i.ppm;
    diff --report-identical-files $i $i.ppm;
    rm $i.ppm
done

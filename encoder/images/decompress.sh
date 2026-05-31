#!/usr/bin/env bash

for i in *.ppm; do
    djxl $i.jxl $i.ppm;
done

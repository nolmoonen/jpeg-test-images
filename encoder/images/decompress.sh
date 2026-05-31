#!/usr/bin/env bash

for i in *.jxl; do
    djxl $i $(basename $i .jxl);
done

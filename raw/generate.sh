#!/usr/bin/env bash

# Extract one PreviewImage per file.
exiftool -binary -tagOut %d%f_%t%-c.%s -preview:PreviewImage -recurse data.lfs

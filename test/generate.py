#!/usr/bin/env python3

import argparse
import os.path
import subprocess
import sys
import tempfile


def encode_jpeg(
    sample: str,
    scan: str,
    path_out: str,
    path_in: str,
    has_restarts: bool,
    is_gray: bool = False,
):
    """Encode a JPEG file with the given parameters."""
    # Create a temporary file for the scan specification that is not removed on close.
    with tempfile.NamedTemporaryFile(mode="w+t", delete_on_close=False) as fp:
        fp.write(scan)
        fp.close()

        opts = [
            "-sample",
            sample,
            "-scans",
            f"{fp.name}",
            "-optimize",
            "-outfile",
            path_out,
        ]

        if has_restarts:
            opts += ["-restart", "1"]

        if is_gray:
            opts += ["-grayscale"]

        subprocess.run(["cjpeg"] + opts + [f"{path_in}"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("image_path", help="Path to a PPM image.")
    args = parser.parse_args()

    image_path = args.image_path
    if not os.path.isfile(image_path):
        sys.exit(f"{image_path} is not a file")

    try:
        subprocess.run(["cjpeg", "--help"], stderr=subprocess.DEVNULL)
    except FileNotFoundError as e:
        sys.exit("cjpeg command not found, is libjpeg installed?")

    # Generate one baseline image for every possible sequential configuration.

    # For all legal sub-sampling factor combinations, inner factor is checked below.
    for ss in [
        ((x0, y0), (x1, y1), (x2, y2))
        for x0 in range(1, 5)
        for y0 in range(1, 5)
        for x1 in range(1, 5)
        for y1 in range(1, 5)
        for x2 in range(1, 5)
        for y2 in range(1, 5)
    ]:
        # Remove sub-sampling combinations that yield fractional sampling. Even though the specification
        #   allows it, no decoder implements it. Notably, cjpeg does not support it.
        max_x = max([ss[0][0], ss[1][0], ss[2][0]])
        if max_x % ss[0][0] != 0 or max_x % ss[1][0] != 0 or max_x % ss[2][0] != 0:
            continue

        max_y = max([ss[0][1], ss[1][1], ss[2][1]])
        if max_x % ss[0][1] != 0 or max_x % ss[1][1] != 0 or max_x % ss[2][1] != 0:
            continue

        # For all components combinations in scans, including out-of-order ones.
        # Note that within a scan the components must be in order, e.g. [[1, 0], 2] is illegal.
        for scans in [
            [[0, 1, 2]],
            [[0], [1, 2]],
            [[1, 2], [0]],
            [[0, 1], [2]],
            [[2], [0, 1]],
            [[0], [1], [2]],
            [[1], [0], [2]],
            [[0], [2], [1]],
            [[2], [1], [0]],
        ]:
            # Remove sub-sampling combinations that exceed an inner factor of 10 (B.2.3 Cs_j).
            factor_inner = 0
            for scan in scans:
                factor_inner = sum([ss[comp][0] * ss[comp][1] for comp in scan])
                if factor_inner > 10:
                    break
            if factor_inner > 10:
                continue

            str_ss = (
                f"{ss[0][0]}x{ss[0][1]},{ss[1][0]}x{ss[1][1]},{ss[2][0]}x{ss[2][1]}"
            )
            str_scan = "x".join(
                ["".join([f"{comp}" for comp in scan]) for scan in scans]
            )
            file_scan = (
                ";\n".join([" ".join([f"{comp}" for comp in scan]) for scan in scans])
                + ";"
            )

            path_r0 = f"ycbcr-{str_ss}-r0-{str_scan}.jpg"
            encode_jpeg(str_ss, file_scan, path_r0, image_path, has_restarts=False)
            path_r1 = f"ycbcr-{str_ss}-r1-{str_scan}.jpg"
            encode_jpeg(str_ss, file_scan, path_r1, image_path, has_restarts=True)

    # Generate a few progressive configurations since there are simply too many possibilities.
    conventional_ss = [
        "1x1,1x1,1x1",  # 4:4:4
        "2x1,1x1,1x1",  # 4:2:2
        "1x2,1x1,1x1",  # 4:4:0
        "2x2,1x1,1x1",  # 4:2:0
        "4x1,1x1,1x1",  # 4:1:1
        "4x2,1x1,1x1",  # 4:1:0
    ]

    for ss in conventional_ss:
        # The default progressive scan, see
        # https://github.com/libjpeg-turbo/libjpeg-turbo/blob/81feffa632bcd928d4cd1c35e5bb6c1eb02ac199/doc/wizard.txt
        scan = "0,1,2: 0-0,   0, 1 ;\
                0:     1-5,   0, 2 ;\
                2:     1-63,  0, 1 ;\
                1:     1-63,  0, 1 ;\
                0:     6-63,  0, 2 ;\
                0:     1-63,  2, 1 ;\
                0,1,2: 0-0,   1, 0 ;\
                2:     1-63,  1, 0 ;\
                1:     1-63,  1, 0 ;\
                0:     1-63,  1, 0 ;"
        path_r0 = f"ycbcr-{ss}-r0-prog-default.jpg"
        encode_jpeg(ss, scan, path_r0, image_path, has_restarts=False)
        path_r1 = f"ycbcr-{ss}-r1-prog-default.jpg"
        encode_jpeg(ss, scan, path_r1, image_path, has_restarts=True)
        # Minimum amount of progressive scans.
        scan = "0,1,2: 0-0,   0, 0 ;\
                0:     1-63,  0, 0 ;\
                1:     1-63,  0, 0 ;\
                2:     1-63,  0, 0 ;"
        path_r0 = f"ycbcr-{ss}-r0-prog-basic.jpg"
        encode_jpeg(ss, scan, path_r0, image_path, has_restarts=False)
        path_r1 = f"ycbcr-{ss}-r1-prog-basic.jpg"
        encode_jpeg(ss, scan, path_r1, image_path, has_restarts=True)
        # Default program with non-interleaved DC scans.
        scan = "0:     0-0,   0, 1 ;\
                1:     0-0,   0, 1 ;\
                2:     0-0,   0, 1 ;\
                0:     1-5,   0, 2 ;\
                2:     1-63,  0, 1 ;\
                1:     1-63,  0, 1 ;\
                0:     6-63,  0, 2 ;\
                0:     1-63,  2, 1 ;\
                0:     0-0,   1, 0 ;\
                1:     0-0,   1, 0 ;\
                2:     0-0,   1, 0 ;\
                2:     1-63,  1, 0 ;\
                1:     1-63,  1, 0 ;\
                0:     1-63,  1, 0 ;"
        path_r0 = f"ycbcr-{ss}-r0-prog-dc-separate.jpg"
        encode_jpeg(ss, scan, path_r0, image_path, has_restarts=False)
        path_r1 = f"ycbcr-{ss}-r1-prog-dc-separate.jpg"
        encode_jpeg(ss, scan, path_r1, image_path, has_restarts=True)
        # Default program with mixed DC interleaved, reshuffled.
        scan = "0,1:   0-0,   0, 1 ;\
                0:     1-5,   0, 2 ;\
                1:     1-63,  0, 1 ;\
                0:     6-63,  0, 2 ;\
                0:     1-63,  2, 1 ;\
                0,1:   0-0,   1, 0 ;\
                1:     1-63,  1, 0 ;\
                0:     1-63,  1, 0 ;\
                2:     0-0,   0, 1 ;\
                2:     1-63,  0, 1 ;\
                2:     0-0,   1, 0 ;\
                2:     1-63,  1, 0 ;"
        path_r0 = f"ycbcr-{ss}-r0-prog-shuffled.jpg"
        encode_jpeg(ss, scan, path_r0, image_path, has_restarts=False)
        path_r1 = f"ycbcr-{ss}-r1-prog-shuffled.jpg"
        encode_jpeg(ss, scan, path_r1, image_path, has_restarts=True)
        # Refine some bits when not the entire band has been refined up to that point.
        scan = "0,2:   0-0,   0, 2 ;\
                1:     0-0,   0, 1 ;\
                1:     0-0,   1, 0 ;\
                0,2:   0-0,   2, 1 ;\
                0,2:   0-0,   1, 0 ;\
                0:     1-31,  0, 2 ;\
                0:     1-31,  2, 1 ;\
                0:     1-31,  1, 0 ;\
                0:     32-63, 0, 2 ;\
                0:     32-63, 2, 1 ;\
                0:     32-63, 1, 0 ;\
                1:     1-63,  0, 0 ;\
                2:     1-63,  0, 0 ;"
        path_r0 = f"ycbcr-{ss}-r0-prog-refine.jpg"
        encode_jpeg(ss, scan, path_r0, image_path, has_restarts=False)
        path_r1 = f"ycbcr-{ss}-r1-prog-refine.jpg"
        encode_jpeg(ss, scan, path_r1, image_path, has_restarts=True)

    # Generate some grayscale files.
    for ss in ["1x1", "2x2", "3x3", "4x4"]:
        scan = "0;"
        path_r0 = f"y-{ss}-r0-sequ.jpg"
        encode_jpeg(ss, scan, path_r0, image_path, has_restarts=False, is_gray=True)
        path_r1 = f"y-{ss}-r1-sequ.jpg"
        encode_jpeg(ss, scan, path_r1, image_path, has_restarts=True, is_gray=True)

        scan = "0:     0-0,   0, 0 ;\
                0:     1-63,  0, 0 ;"
        path_r0 = f"y-{ss}-r0-prog-basic.jpg"
        encode_jpeg(ss, scan, path_r0, image_path, has_restarts=False, is_gray=True)
        path_r1 = f"y-{ss}-r1-prog-basic.jpg"
        encode_jpeg(ss, scan, path_r1, image_path, has_restarts=False, is_gray=True)

        scan = "0:     0-0,   0, 1 ;\
                0:     1-5,   0, 2 ;\
                0:     6-63,  0, 2 ;\
                0:     1-63,  2, 1 ;\
                0:     0-0,   1, 0 ;\
                0:     1-63,  1, 0 ;"
        path_r0 = f"y-{ss}-r0-prog-default.jpg"
        encode_jpeg(ss, scan, path_r0, image_path, has_restarts=False, is_gray=True)
        path_r1 = f"y-{ss}-r1-prog-default.jpg"
        encode_jpeg(ss, scan, path_r1, image_path, has_restarts=False, is_gray=True)

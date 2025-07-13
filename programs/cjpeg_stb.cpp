// c++ cjpeg_stb.cpp -o cjpeg_stb
#include "util.hpp"

#define STB_IMAGE_WRITE_IMPLEMENTATION
#include "stb_image_write.h"

#include <cstdlib>
#include <iostream>
#include <stdint.h>
#include <string>
#include <vector>

int main(int argc, const char* argv[])
{
    if (argc < 2) {
        std::cerr << "usage: <ppm file>\n";
        return EXIT_FAILURE;
    }

    int size_x;
    int size_y;
    std::vector<uint8_t> data;
    if (read_ppm(argv[1], size_x, size_y, data) != EXIT_SUCCESS) return EXIT_FAILURE;

    std::string out = std::string(argv[1]) + ".stb.jpg";
    if (stbi_write_jpg(out.c_str(), size_x, size_y, 3, data.data(), 90) != 0) return EXIT_FAILURE;
}

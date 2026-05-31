// c++ cjpeg_stb.cpp -o cjpeg_stb
#include "util.hpp"

#define STB_IMAGE_WRITE_IMPLEMENTATION
#include "stb_image_write.h"

#include <cstdlib>
#include <filesystem>
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

    const std::filesystem::path path(argv[1]);

    int size_x;
    int size_y;
    std::vector<uint8_t> data;
    if (read_ppm(path.c_str(), size_x, size_y, data) != EXIT_SUCCESS) return EXIT_FAILURE;

    const std::string out = path.filename().replace_extension("").string() + ".stb.jpg";
    if (stbi_write_jpg(out.c_str(), size_x, size_y, 3, data.data(), 90) != 0) return EXIT_FAILURE;
}

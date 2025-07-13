#include <cmath>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <sstream>
#include <stdint.h>
#include <vector>

int read_ppm(const char* filename, int& size_x, int& size_y, std::vector<uint8_t>& data)
{
    std::ifstream file(filename);
    if (!file.is_open()) {
        std::cerr << "failed to open read file\n";
        return EXIT_FAILURE;
    }

    std::string line;

    std::getline(file, line);
    if (line != "P6") {
        std::cerr << "Expected P6 format but got unsupported format \"" << line << "\"\n";
        return EXIT_FAILURE;
    }

    std::getline(file, line);
    std::istringstream iss(line);
    if (!(iss >> size_x >> size_y) || size_x <= 0 || size_y <= 0) {
        std::cerr << "Expected valid size but got \"" << line << "\"\n";
        return EXIT_FAILURE;
    }

    std::getline(file, line);
    if (line != "255" && line != "65535") {
        std::cerr << "Expected 255 or 65535 maximum value got unsupported value \"" << line
                  << "\"\n";
        return EXIT_FAILURE;
    }

    const int bit_depth = line == "65535" ? 2 : 1;

    const size_t num_values         = 3 * size_x * size_y;
    const size_t expected_file_size = num_values * bit_depth;

    const std::streampos file_data = file.tellg();
    file.seekg(0, std::ios_base::end);
    const std::streampos file_end = file.tellg();
    file.seekg(file_data);
    const size_t file_size = file_end - file_data;
    if (file_size != expected_file_size) {
        std::cerr << "Invalid file size, expected at least " << expected_file_size << " but got "
                  << file_size << "\n";
        return EXIT_FAILURE;
    }

    data.resize(num_values);
    if (bit_depth == 1) {
        file.read(reinterpret_cast<char*>(data.data()), file_size);
        file.close();
    } else {
        std::vector<uint16_t> data16(num_values);
        file.read(reinterpret_cast<char*>(data16.data()), file_size);
        for (size_t i = 0; i < num_values; ++i) {
            const uint16_t le = data16[i] >> 8 | ((data16[i] << 8) & 0xffff);
            data[i]           = std::roundf((255.f / 65535) * le);
        }
    }

    return EXIT_SUCCESS;
}

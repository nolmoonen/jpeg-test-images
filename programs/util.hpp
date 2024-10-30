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
    if (line != "255") {
        std::cerr << "Expected 255 maximum value got unsupported value \"" << line << "\"\n";
        return EXIT_FAILURE;
    }

    const size_t num_values = 3 * size_x * size_y;

    const std::streampos file_data = file.tellg();
    file.seekg(0, std::ios_base::end);
    const std::streampos file_end = file.tellg();
    file.seekg(file_data);
    const size_t file_size = file_end - file_data;
    if (file_size < num_values) {
        std::cerr << "Invalid file size, expected at least " << num_values << " but got "
                  << file_size << "\n";
        return EXIT_FAILURE;
    }

    data.resize(num_values);
    file.read(reinterpret_cast<char*>(data.data()), file_size);
    file.close();

    return EXIT_SUCCESS;
}

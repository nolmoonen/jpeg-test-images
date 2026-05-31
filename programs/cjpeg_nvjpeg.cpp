// /usr/local/cuda/bin/nvcc cjpeg_nvjpeg.cpp -lnvjpeg --output-file cjpeg_nvjpeg
#include "util.hpp"

#include <cuda_runtime.h>
#include <nvjpeg.h>

#include <cstdlib>
#include <filesystem>
#include <iostream>
#include <stdint.h>
#include <string>
#include <vector>

#define CHECK_CUDA(call)                                                                      \
    do {                                                                                      \
        cudaError_t err = call;                                                               \
        if (err != cudaSuccess) {                                                             \
            std::cerr << "CUDA error \"" << cudaGetErrorString(err) << "\" at: " __FILE__ ":" \
                      << __LINE__ << "\n";                                                    \
            std::exit(EXIT_FAILURE);                                                          \
        }                                                                                     \
    } while (0)

#define CHECK_NVJPEG(call)                                                                     \
    do {                                                                                       \
        nvjpegStatus_t stat = call;                                                            \
        if (stat != NVJPEG_STATUS_SUCCESS) {                                                   \
            std::cerr << "nvJPEG error \"" << static_cast<int>(stat) << "\" at: " __FILE__ ":" \
                      << __LINE__ << "\n";                                                     \
            std::exit(EXIT_FAILURE);                                                           \
        }                                                                                      \
    } while (0)

int main(int argc, const char* argv[])
{
    if (argc < 2 || argc > 3) {
        std::cerr << "usage: [-progressive] <ppm file>\n";
        return EXIT_FAILURE;
    }

    const bool do_progressive = argc == 3;
    const std::filesystem::path path(argv[argc - 1]);

    int size_x;
    int size_y;
    std::vector<uint8_t> h_data;
    if (read_ppm(path.c_str(), size_x, size_y, h_data) != EXIT_SUCCESS) return EXIT_FAILURE;

    uint8_t* d_data = nullptr;
    CHECK_CUDA(cudaMalloc(&d_data, h_data.size()));
    CHECK_CUDA(cudaMemcpy(d_data, h_data.data(), h_data.size(), cudaMemcpyHostToDevice));

    cudaStream_t stream = 0;

    nvjpegHandle_t nv_handle;
    CHECK_NVJPEG(nvjpegCreateSimple(&nv_handle));

    nvjpegEncoderState_t nv_enc_state;
    CHECK_NVJPEG(nvjpegEncoderStateCreate(nv_handle, &nv_enc_state, stream));

    nvjpegEncoderParams_t nv_enc_params;
    CHECK_NVJPEG(nvjpegEncoderParamsCreate(nv_handle, &nv_enc_params, stream));

    CHECK_NVJPEG(nvjpegEncoderParamsSetEncoding(
        nv_enc_params,
        do_progressive ? NVJPEG_ENCODING_PROGRESSIVE_DCT_HUFFMAN : NVJPEG_ENCODING_BASELINE_DCT,
        stream));
    CHECK_NVJPEG(nvjpegEncoderParamsSetQuality(nv_enc_params, 70, stream));
    CHECK_NVJPEG(nvjpegEncoderParamsSetOptimizedHuffman(nv_enc_params, 1, stream));
    CHECK_NVJPEG(nvjpegEncoderParamsSetSamplingFactors(nv_enc_params, NVJPEG_CSS_444, stream));

    nvjpegImage_t nv_image;
    nv_image.channel[0] = d_data;
    nv_image.pitch[0]   = 3 * size_x;

    CHECK_NVJPEG(nvjpegEncodeImage(
        nv_handle,
        nv_enc_state,
        nv_enc_params,
        &nv_image,
        NVJPEG_INPUT_RGBI,
        size_x,
        size_y,
        stream));
    CHECK_CUDA(cudaStreamSynchronize(stream));

    size_t length;
    CHECK_NVJPEG(nvjpegEncodeRetrieveBitstream(nv_handle, nv_enc_state, nullptr, &length, stream));

    std::vector<uint8_t> jpeg(length);
    CHECK_NVJPEG(
        nvjpegEncodeRetrieveBitstream(nv_handle, nv_enc_state, jpeg.data(), &length, stream));

    std::string out = std::string(path.filename().replace_extension("")) +
                      (do_progressive ? ".nvjpeg.prog.jpg" : ".nvjpeg.seq.jpg");
    std::ofstream file(out, std::ios::out | std::ios::binary);
    if (!file.is_open()) {
        std::cerr << "failed to open write file\n";
        return EXIT_FAILURE;
    }

    file.write(reinterpret_cast<const char*>(jpeg.data()), jpeg.size());
    file.close();
}

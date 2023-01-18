import pytest
from sanitizer_random.lib.sanitizer_random import SanitizerRandom
from vertex_ch_encoder.lib.vertex_ch_encoder import EncoderSTL, DecoderSTL, base2, base3

SECRET_SIZE_BITS = 4 * 8  # size of any secret = 4 bytes


# Infiltrated text
def test_sanitize_random_text_base_2():
    # Decoding before sanitization
    decoder_before = DecoderSTL("test_objects/base2/text/encoded_sphere.STL", False)  # carrier's with secret filepath
    decoder_before.DecodeFileFromSTL(
        "test_objects/base2/text/secret_before.txt", base2)  # path to save the decoded carrier

    sanitizer = SanitizerRandom("test_objects/base2/text/encoded_sphere.STL")  # carrier's filepath
    sanitizer.Sanitize(SECRET_SIZE_BITS)
    sanitizer.SaveSanitizedFile(
        "test_objects/base2/text/sanitized_sphere.STL")  # filepath destination for sanitized stl file

    # Decoding after sanitization
    decoder_after = DecoderSTL("test_objects/base2/text/sanitized_sphere.STL", False)  # carrier's with secret filepath
    decoder_after.DecodeFileFromSTL(
        "test_objects/base2/text/secret_after.txt", base2)  # path to save the decoded carrier


    secret_before = open("test_objects/base2/text/secret_before.txt", "rb").read()
    secret_after = open("test_objects/base2/text/secret_after.txt", "rb").read()
    assert secret_before != secret_after


# Infiltrated picture of elephant
def test_sanitize_random_image_base_2():
    # Decoding before sanitization

    decoder_before = DecoderSTL("test_objects/base2/image/encoded_bunny.STL", False)  # carrier's with secret filepath
    decoder_before.DecodeFileFromSTL(
        "test_objects/base2/image/secret_before.jpeg", base2)  # path to save the decoded carrier

    sanitizer = SanitizerRandom("test_objects/base2/image/encoded_bunny.STL")  # carrier's filepath
    sanitizer.Sanitize(SECRET_SIZE_BITS + 325 * 8)  # 325 * 8
    sanitizer.SaveSanitizedFile(
        "test_objects/base2/image/sanitized_bunny.STL")  # filepath destination for sanitized stl file

    # Decoding after sanitization
    decoder_after = DecoderSTL("test_objects/base2/image/sanitized_bunny.STL", False)  # carrier's with secret filepath
    decoder_after.DecodeFileFromSTL(
        "test_objects/base2/image/secret_after.jpeg", base2)  # path to save the decoded carrier


    secret_before = open("test_objects/base2/image/secret_before.jpeg", "rb").read()
    secret_after = open("test_objects/base2/image/secret_after.jpeg", "rb").read()
    assert secret_before != secret_after


# Infiltrated picture of elephant
def test_sanitize_random_bitmap_base_2():
    # Decoding before sanitization
    decoder_before = DecoderSTL("test_objects/base2/bitmap/encoded_bunny.STL", False)  # carrier's with secret filepath
    decoder_before.DecodeFileFromSTL(
        "test_objects/base2/bitmap/secret_before.bmp", base2)  # path to save the decoded carrier

    # secret's size is 90 bytes = 720 bits
    sanitizer = SanitizerRandom("test_objects/base2/bitmap/encoded_bunny.STL")  # carrier's filepath
    sanitizer.Sanitize(SECRET_SIZE_BITS + 300)  # 325 * 8
    sanitizer.SaveSanitizedFile(
        "test_objects/base2/bitmap/sanitized_bunny.STL")  # filepath destination for sanitized stl file

    # Decoding after sanitization
    decoder_after = DecoderSTL("test_objects/base2/bitmap/sanitized_bunny.STL", False)  # carrier's with secret filepath
    decoder_after.DecodeFileFromSTL(
        "test_objects/base2/bitmap/secret_after.bmp", base2)  # path to save the decoded carrier

    secret_before = open("test_objects/base2/bitmap/secret_before.bmp", "rb").read()
    secret_after = open("test_objects/base2/bitmap/secret_after.bmp", "rb").read()
    assert secret_before != secret_after


# # Infiltrated picture of elephant
# def test_sanitize_random_bitmap_base_3():
#     # Decoding before sanitization
#     decoder_before = DecoderSTL(
#         "test_objects/base3/bitmap/encoded_bunny.STL", False)  # carrier's with secret filepath
#     decoder_before.DecodeFileFromSTL(
#         "test_objects/base3/bitmap/secret_before.bmp", base3)  # path to save the decoded carrier
#
#     # secret's size is 90 bytes = 720 bits
#     sanitizer = SanitizerRandom("test_objects/base3/bitmap/encoded_bunny.STL")  # carrier's filepath
#     sanitizer.Sanitize(SECRET_SIZE_BITS + 300)  # 325 * 8
#     sanitizer.SaveSanitizedFile(
#         "test_objects/base3/bitmap/sanitized_bunny.STL")  # filepath destination for sanitized stl file
#
#     # Decoding after sanitization
#     decoder_after = DecoderSTL(
#         "test_objects/base3/bitmap/sanitized_bunny.STL", False)  # carrier's with secret filepath
#     decoder_after.DecodeBytesFromSTL(
#         "test_objects/base3/bitmap/secret_after.bmp", base3)  # path to save the decoded carrier
#
#     secret_before = open("test_objects/base3/bitmap/secret_before.bmp", "rb").read()
#     secret_after = open("test_objects/base3/bitmap/secret_after.bmp", "rb").read()
#     assert secret_before != secret_after

import pytest
from sanitizer_random.lib.sanitizer_random import SanitizerRandom
from vertex_ch_encoder.lib.vertex_ch_encoder import EncoderSTL, DecoderSTL, base2, base3

from facet_ch_encoder.lib.facet_ch_encoder import EncoderSTL as FacetEncoderSTL, DecoderSTL as FacetDecoderSTL

SECRET_SIZE_BITS = 4 * 8  # size of any secret = 4 bytes


# Infiltrated text
def test_sanitize_vertex_ch_random_text_base_2():
    # Decoding before sanitization
    decoder_before = DecoderSTL("test_objects/vertex_channel/base2/text/encoded_sphere.STL", False)  # carrier's with secret filepath
    decoder_before.DecodeFileFromSTL(
        "test_objects/vertex_channel/base2/text/secret_before.txt", base2)  # path to save the decoded carrier

    sanitizer = SanitizerRandom("test_objects/vertex_channel/base2/text/encoded_sphere.STL")  # carrier's filepath
    sanitizer.SanitizeVertexCh(SECRET_SIZE_BITS)
    sanitizer.SaveSanitizedFile(
        "test_objects/vertex_channel/base2/text/sanitized_sphere.STL")  # filepath destination for sanitized stl file

    # Decoding after sanitization
    decoder_after = DecoderSTL("test_objects/vertex_channel/base2/text/sanitized_sphere.STL", False)  # carrier's with secret filepath
    decoder_after.DecodeFileFromSTL(
        "test_objects/vertex_channel/base2/text/secret_after.txt", base2)  # path to save the decoded carrier

    secret_before = open("test_objects/vertex_channel/base2/text/secret_before.txt", "rb").read()
    secret_after = open("test_objects/vertex_channel/base2/text/secret_after.txt", "rb").read()
    assert secret_before != secret_after


# Infiltrated picture of elephant
def test_sanitize_random_vertex_ch_image_base_2():
    # Decoding before sanitization

    decoder_before = DecoderSTL("test_objects/vertex_channel/base2/image/encoded_bunny.STL", False)  # carrier's with secret filepath
    decoder_before.DecodeFileFromSTL(
        "test_objects/vertex_channel/base2/image/secret_before.jpeg", base2)  # path to save the decoded carrier

    sanitizer = SanitizerRandom("test_objects/vertex_channel/base2/image/encoded_bunny.STL")  # carrier's filepath
    sanitizer.SanitizeVertexCh(SECRET_SIZE_BITS + 325 * 8)  # 325 * 8
    sanitizer.SaveSanitizedFile(
        "test_objects/vertex_channel/base2/image/sanitized_bunny.STL")  # filepath destination for sanitized stl file

    # Decoding after sanitization
    decoder_after = DecoderSTL("test_objects/vertex_channel/base2/image/sanitized_bunny.STL", False)  # carrier's with secret filepath
    decoder_after.DecodeFileFromSTL(
        "test_objects/vertex_channel/base2/image/secret_after.jpeg", base2)  # path to save the decoded carrier

    secret_before = open("test_objects/vertex_channel/base2/image/secret_before.jpeg", "rb").read()
    secret_after = open("test_objects/vertex_channel/base2/image/secret_after.jpeg", "rb").read()
    assert secret_before != secret_after


# Infiltrated picture of elephant
def test_sanitize_random_vertex_ch_bitmap_base_2():
    # Decoding before sanitization
    decoder_before = DecoderSTL("test_objects/vertex_channel/base2/bitmap/encoded_bunny.STL", False)  # carrier's with secret filepath
    decoder_before.DecodeFileFromSTL(
        "test_objects/vertex_channel/base2/bitmap/secret_before.bmp", base2)  # path to save the decoded carrier

    # secret's size is 90 bytes = 720 bits
    sanitizer = SanitizerRandom("test_objects/vertex_channel/base2/bitmap/encoded_bunny.STL")  # carrier's filepath
    sanitizer.SanitizeVertexCh(SECRET_SIZE_BITS + 300)  # 325 * 8
    sanitizer.SaveSanitizedFile(
        "test_objects/vertex_channel/base2/bitmap/sanitized_bunny.STL")  # filepath destination for sanitized stl file

    # Decoding after sanitization
    decoder_after = DecoderSTL("test_objects/vertex_channel/base2/bitmap/sanitized_bunny.STL", False)  # carrier's with secret filepath
    decoder_after.DecodeFileFromSTL(
        "test_objects/vertex_channel/base2/bitmap/secret_after.bmp", base2)  # path to save the decoded carrier

    secret_before = open("test_objects/vertex_channel/base2/bitmap/secret_before.bmp", "rb").read()
    secret_after = open("test_objects/vertex_channel/base2/bitmap/secret_after.bmp", "rb").read()
    assert secret_before != secret_after


# Infiltrated picture of elephant
def test_sanitize_vertex_chrandom_bitmap_base_3():
    # Decoding before sanitization
    decoder_before = DecoderSTL(
        "test_objects/vertex_channel/base3/bitmap/encoded_bunny.STL", False)  # carrier's with secret filepath
    secret_before = decoder_before.DecodeBytesFromSTL(base3)  # path to save the decoded carrier

    # secret's size is 90 bytes = 720 bits
    sanitizer = SanitizerRandom("test_objects/vertex_channel/base3/bitmap/encoded_bunny.STL")  # carrier's filepath
    sanitizer.SanitizeVertexCh(SECRET_SIZE_BITS + 300)  # 325 * 8
    sanitizer.SaveSanitizedFile(
        "test_objects/vertex_channel/base3/bitmap/sanitized_bunny.STL")  # filepath destination for sanitized stl file

    # Decoding after sanitization
    decoder_after = DecoderSTL(
        "test_objects/vertex_channel/base3/bitmap/sanitized_bunny.STL", False)  # carrier's with secret filepath
    secret_after = decoder_after.DecodeBytesFromSTL(base3)  # path to save the decoded carrier

    assert secret_before != secret_after


# Infiltrated text
def test_sanitize_facet_ch_random_text_base_2():
    # Decoding before sanitization
    decoder_before = FacetDecoderSTL("test_objects/vertex_channel/base2/text/encoded_sphere.STL", False)  # carrier's with secret filepath
    decoder_before.DecodeFileFromSTL(
        "test_objects/vertex_channel/base2/text/secret_before.txt")  # path to save the decoded carrier

    sanitizer = SanitizerRandom("test_objects/vertex_channel/base2/text/encoded_sphere.STL")  # carrier's filepath
    sanitizer.SanitizeFacetCh(SECRET_SIZE_BITS)
    sanitizer.SaveSanitizedFile(
        "test_objects/vertex_channel/base2/text/sanitized_sphere.STL")  # filepath destination for sanitized stl file

    # Decoding after sanitization
    decoder_after = FacetDecoderSTL("test_objects/vertex_channel/base2/text/sanitized_sphere.STL", False)  # carrier's with secret filepath
    decoder_after.DecodeFileFromSTL(
        "test_objects/vertex_channel/base2/text/secret_after.txt")  # path to save the decoded carrier

    secret_before = open("test_objects/vertex_channel/base2/text/secret_before.txt", "rb").read()
    secret_after = open("test_objects/vertex_channel/base2/text/secret_after.txt", "rb").read()
    assert secret_before != secret_after

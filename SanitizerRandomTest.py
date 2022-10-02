from SanitizersLib.SanitizerRandom import SanitizerRandom
from EncodingDecodingLib.EncodingDecoding import DecoderSTL

SECRET_SIZE_BITS = 4 * 8  # size of any secret = 4 bytes


# Infiltrated text
def SanitizeTextTest():
    # Decoding before sanitization
    decoder_before = DecoderSTL("tests/SanitizerRandomTest/text/encoded_sphere.STL")  # carrier's with secret filepath
    decoder_before.DecodeFileFromSTL(
        "tests/SanitizerRandomTest/text/secret_before.txt")  # path to save the decoded carrier

    sanitizer = SanitizerRandom("tests/SanitizerRandomTest/text/encoded_sphere.STL")  # carrier's filepath
    sanitizer.Sanitize(SECRET_SIZE_BITS)
    sanitizer.SaveSanitizedFile(
        "tests/SanitizerRandomTest/text/sanitized_sphere.STL")  # filepath destination for sanitized stl file

    # Decoding after sanitization
    decoder_after = DecoderSTL("tests/SanitizerRandomTest/text/sanitized_sphere.STL")  # carrier's with secret filepath
    decoder_after.DecodeFileFromSTL(
        "tests/SanitizerRandomTest/text/secret_after.txt")  # path to save the decoded carrier
    print("\n")


# Infiltrated picture of elephant
def SanitizePictureTest():
    # Decoding before sanitization

    decoder_before = DecoderSTL("tests/SanitizerRandomTest/image/encoded_bunny.STL")  # carrier's with secret filepath
    decoder_before.DecodeFileFromSTL(
        "tests/SanitizerRandomTest/image/secret_before.jpeg")  # path to save the decoded carrier

    sanitizer = SanitizerRandom("tests/SanitizerRandomTest/image/encoded_bunny.STL")  # carrier's filepath
    sanitizer.Sanitize(SECRET_SIZE_BITS + 325 * 8)  # 325 * 8
    sanitizer.SaveSanitizedFile(
        "tests/SanitizerRandomTest/image/sanitized_bunny.STL")  # filepath destination for sanitized stl file

    # Decoding after sanitization
    decoder_after = DecoderSTL("tests/SanitizerRandomTest/image/sanitized_bunny.STL")  # carrier's with secret filepath
    decoder_after.DecodeFileFromSTL(
        "tests/SanitizerRandomTest/image/secret_after.jpeg")  # path to save the decoded carrier
    print("\n")


# Infiltrated picture of elephant
def SanitizeBmpTest():
    # Decoding before sanitization
    decoder_before = DecoderSTL("tests/SanitizerRandomTest/bitmap/encoded_bunny.STL")  # carrier's with secret filepath
    decoder_before.DecodeFileFromSTL(
        "tests/SanitizerRandomTest/bitmap/secret_before.bmp")  # path to save the decoded carrier

    # secret's size is 90 bytes = 720 bits
    sanitizer = SanitizerRandom("tests/SanitizerRandomTest/bitmap/encoded_bunny.STL")  # carrier's filepath
    sanitizer.Sanitize(SECRET_SIZE_BITS + 300)  # 325 * 8
    sanitizer.SaveSanitizedFile(
        "tests/SanitizerRandomTest/bitmap/sanitized_bunny.STL")  # filepath destination for sanitized stl file

    # Decoding after sanitization
    decoder_after = DecoderSTL("tests/SanitizerRandomTest/bitmap/sanitized_bunny.STL")  # carrier's with secret filepath
    decoder_after.DecodeFileFromSTL(
        "tests/SanitizerRandomTest/bitmap/secret_after.bmp")  # path to save the decoded carrier
    print("\n")


#
#
SanitizeBmpTest()

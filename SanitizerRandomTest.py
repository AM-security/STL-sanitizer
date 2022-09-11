from SanitizersLib.SanitizerRandom import SanitizerRandom
from EncodingDecodingLib.EncodingDecoding import DecoderSTL


# Test 1. Infiltrated text

def Test1():
    # Decoding before sanitization
    decoder_before = DecoderSTL("TestFiles/SanitizerRandomTest/1/encoded_sphere.STL")  # carrier's with secret filepath
    decoder_before.DecodeFileFromSTL(
        "TestFiles/SanitizerRandomTest/1/secret_before.txt")  # path to save the decoded carrier

    sanitizer = SanitizerRandom("TestFiles/SanitizerRandomTest/1/encoded_sphere.STL")  # carrier's filepath
    sanitizer.Sanitize()
    sanitizer.SaveSanitizedFile(
        "TestFiles/SanitizerRandomTest/1/sanitized_sphere.STL")  # filepath destination for sanitized stl file

    # Decoding after sanitization
    decoder_after = DecoderSTL("TestFiles/SanitizerRandomTest/1/sanitized_sphere.STL")  # carrier's with secret filepath
    decoder_after.DecodeFileFromSTL(
        "TestFiles/SanitizerRandomTest/1/secret_after.txt")  # path to save the decoded carrier


# Test 2. Infiltrated picture of elephant
def Test2():
    # Decoding before sanitization

    decoder_before = DecoderSTL("TestFiles/SanitizerRandomTest/2/encoded_bunny.STL")  # carrier's with secret filepath
    decoder_before.DecodeFileFromSTL(
        "TestFiles/SanitizerRandomTest/2/secret_before.jpeg")  # path to save the decoded carrier

    sanitizer = SanitizerRandom("TestFiles/SanitizerRandomTest/2/encoded_bunny.STL")  # carrier's filepath
    sanitizer.Sanitize()
    sanitizer.SaveSanitizedFile(
        "TestFiles/SanitizerRandomTest/2/sanitized_bunny.STL")  # filepath destination for sanitized stl file

    # Decoding after sanitization
    decoder_after = DecoderSTL("TestFiles/SanitizerRandomTest/2/sanitized_bunny.STL")  # carrier's with secret filepath
    decoder_after.DecodeFileFromSTL(
        "TestFiles/SanitizerRandomTest/2/secret_after.jpeg")  # path to save the decoded carrier


Test1()
# Test2()

from EncodingDecodingLib.EncodingDecoding import EncoderSTL, DecoderSTL, base2, base3


# Test text. infiltrating secret.txt into sphere stl file
def EncodeDecodeTextTestBase2():
    encoder = EncoderSTL("tests/EncodingDecodingTest/text/original_sphere.STL")  # carrier's filepath
    encoder.EncodeFileInSTL("tests/EncodingDecodingTest/text/secret.txt",  # secret's path
                            "tests/EncodingDecodingTest/text/encoded/encoded_sphere.STL", base2)  # path to save the carrier with secret

    decoder = DecoderSTL(
        "tests/EncodingDecodingTest/text/encoded/encoded_sphere.STL")  # carrier's with secret filepath
    decoder.DecodeFileFromSTL(
        "tests/EncodingDecodingTest/text/decoded/decoded_secret.txt", base2)  # path to save the decoded secret
    print("\n")


# Test image. infiltrating elephant_secret.jpeg into bunny stl file
def EncodeDecodePictureTest():
    encoder = EncoderSTL("tests/EncodingDecodingTest/image/bunny.STL")  # carrier's filepath
    encoder.EncodeFileInSTL("tests/EncodingDecodingTest/image/elephant_secret.jpeg",  # secret's path
                            "tests/EncodingDecodingTest/image/encoded/encoded_bunny.STL", base2)  # path to save the carrier with secret

    decoder = DecoderSTL("tests/EncodingDecodingTest/image/encoded/encoded_bunny.STL")  # carrier's with secret filepath
    decoder.DecodeFileFromSTL(
        "tests/EncodingDecodingTest/image/decoded/decoded_secret.jpeg", base2)  # path to save the decoded secret
    print("\n")


# Test image. infiltrating elephant_secret.jpeg into bunny stl file
def EncodeDecodeBitmapTest():
    encoder = EncoderSTL("tests/EncodingDecodingTest/bitmap/bunny.STL")  # carrier's filepath
    encoder.EncodeFileInSTL("tests/EncodingDecodingTest/bitmap/secret.bmp",  # secret's path
                            "tests/EncodingDecodingTest/bitmap/encoded/encoded_bunny.STL", base2)  # path to save the carrier with secret

    decoder = DecoderSTL("tests/EncodingDecodingTest/bitmap/encoded/encoded_bunny.STL")  # carrier's with secret filepath
    decoder.DecodeFileFromSTL(
        "tests/EncodingDecodingTest/bitmap/decoded/decoded_secret.bmp", base2)  # path to save the decoded secret
    print("\n")


EncodeDecodeTextTest()
EncodeDecodePictureTest()
EncodeDecodeBitmapTest()

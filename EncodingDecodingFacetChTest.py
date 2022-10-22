from EncodingDecodingFacetCh.EncodingDecodingFacetCh import EncoderSTL, DecoderSTL



# Test text. infiltrating secret.txt into sphere stl file
def EncodeDecodeTextTest():
    encoder = EncoderSTL("tests/EncodingDecodingFacetsTest/text/original_sphere.STL")  # carrier's filepath
    encoder.EncodeFileInSTL("tests/EncodingDecodingFacetsTest/text/secret.txt",  # secret's path
                            "tests/EncodingDecodingFacetsTest/text/encoded/encoded_sphere.STL")  # path to save the carrier with secret

    decoder = DecoderSTL(
        "tests/EncodingDecodingFacetsTest/text/encoded/encoded_sphere.STL")  # carrier's with secret filepath
    decoder.DecodeFileFromSTL(
        "tests/EncodingDecodingFacetsTest/text/decoded/decoded_secret.txt")  # path to save the decoded secret
    print("\n")


EncodeDecodeTextTest()
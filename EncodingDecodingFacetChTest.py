from EncodingDecodingFacetCh.EncodingDecodingFacetCh import EncoderSTL, DecoderSTL


# Test text. infiltrating secret.txt into sphere stl file
def EncodeDecodeTextTest():
    encoder = EncoderSTL("tests/EncodingDecodingFacetsTest/text/original_sphere.STL", False)  # carrier's filepath
    encoder.EncodeFileInSTL("tests/EncodingDecodingFacetsTest/text/secret.txt",  # secret's path
                            "tests/EncodingDecodingFacetsTest/text/encoded/encoded_sphere.STL")  # path to save the carrier with secret

    decoder = DecoderSTL(
        "tests/EncodingDecodingFacetsTest/text/encoded/encoded_sphere.STL", False)  # carrier's with secret filepath
    decoder.DecodeFileFromSTL(
        "tests/EncodingDecodingFacetsTest/text/decoded/decoded_secret.txt")  # path to save the decoded secret
    print("\n")

# Test text. infiltrating secret.txt into sphere stl file
def EncodeDecodeBytesTest():
    encoder = EncoderSTL("tests/EncodingDecodingFacetsTest/bytes/original_sphere.STL", False)  # carrier's filepath
    encoder.EncodeBytesInSTL(bytes("Smith (c)", "utf-8"),"tests/EncodingDecodingFacetsTest/text/encoded/encoded_sphere.STL")  # path to save the carrier with secret

    decoder = DecoderSTL("tests/EncodingDecodingFacetsTest/text/encoded/encoded_sphere.STL", False)  # carrier's with secret filepath
    secret = decoder.DecodeBytesFromSTL()  # path to save the decoded secret
    print(secret.decode("utf-8"))
    print("\n")



EncodeDecodeTextTest()
EncodeDecodeBytesTest()

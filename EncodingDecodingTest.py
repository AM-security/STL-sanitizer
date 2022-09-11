from EncodingDecodingLib.EncodingDecoding import EncoderSTL, DecoderSTL

encoder = EncoderSTL("TestFiles/EncodingDecodingTest/original_sphere.STL") # carrier's filepath
encoder.EncodeFileInSTL("TestFiles/EncodingDecodingTest/secret.txt", # secret's path
                        "TestFiles/EncodingDecodingTest/encoded/encoded_sphere.STL")  # path to save the carrier with secret

decoder = DecoderSTL("TestFiles/EncodingDecodingTest/encoded/encoded_sphere.STL")  # carrier's with secret filepath
decoder.DecodeFileFromSTL("TestFiles/EncodingDecodingTest/decoded/decoded_secret.txt")  # path to save the decoded carrier

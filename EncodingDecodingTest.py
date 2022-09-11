from EncodingDecodingLib.EncodingDecoding import EncoderSTL, DecoderSTL

encoder = EncoderSTL()
encoder.EncodeFileInSTL("TestFiles/original_sphere.STL", "TestFiles/secret.txt",
                        "TestFiles/encoded/encoded_sphere.STL")

decoder = DecoderSTL()
decoder.DecodeFileFromSTL("TestFiles/encoded/encoded_sphere.STL", "TestFiles/decoded/decoded_secret.txt")

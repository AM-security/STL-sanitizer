from EncodingDecodingLib.EncodingDecoding import EncoderSTL, DecoderSTL

encoder = EncoderSTL()
encoder.EncodeFileInSTL("test_files/original_sphere.STL", "test_files/secret.txt",
                        "test_files/encoded/encoded_sphere.STL")

decoder = DecoderSTL()
decoder.DecodeFileFromSTL("test_files/encoded/encoded_sphere.STL", "test_files/decoded/decoded_secret.txt")

from EncodingDecodingLib.EncodingDecoding import EncoderSTL, DecoderSTL

# Test 1. infiltrating secret.txt into sphere stl file
encoder = EncoderSTL("TestFiles/EncodingDecodingTest/1/original_sphere.STL") # carrier's filepath
encoder.EncodeFileInSTL("TestFiles/EncodingDecodingTest/1/secret.txt", # secret's path
                        "TestFiles/EncodingDecodingTest/1/encoded/encoded_sphere.STL")  # path to save the carrier with secret

decoder = DecoderSTL("TestFiles/EncodingDecodingTest/1/encoded/encoded_sphere.STL")  # carrier's with secret filepath
decoder.DecodeFileFromSTL("TestFiles/EncodingDecodingTest/1/decoded/decoded_secret.txt")  # path to save the decoded secret


# Test 2. infiltrating elephant_secret.jpeg into bunny stl file
encoder = EncoderSTL("TestFiles/EncodingDecodingTest/2/bunny.STL") # carrier's filepath
encoder.EncodeFileInSTL("TestFiles/EncodingDecodingTest/2/elephant_secret.jpeg", # secret's path
                        "TestFiles/EncodingDecodingTest/2/encoded/encoded_bunny.STL")  # path to save the carrier with secret

decoder = DecoderSTL("TestFiles/EncodingDecodingTest/2/encoded/encoded_bunny.STL")  # carrier's with secret filepath
decoder.DecodeFileFromSTL("TestFiles/EncodingDecodingTest/2/decoded/decoded_secret.jpeg")  # path to save the decoded secret
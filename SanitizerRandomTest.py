from SanitizersLib.SanitizerRandom import SanitizerRandom
from EncodingDecodingLib.EncodingDecoding import DecoderSTL
# Test 1. Infiltrated text
# Decoding before sanitization
decoder = DecoderSTL("TestFiles/SanitizerRandomTest/1/encoded_sphere.STL")  # carrier's with secret filepath
decoder.DecodeFileFromSTL("TestFiles/SanitizerRandomTest/1/secret_before.STL")  # path to save the decoded carrier

sanitizer = SanitizerRandom("TestFiles/SanitizerRandomTest/1/encoded_sphere.STL")  # carrier's filepath
sanitizer.Sanitize()
sanitizer.SaveSanitizedFile("TestFiles/SanitizerRandomTest/1/sanitized_sphere.STL")  # filepath destination for sanitized stl file

# Decoding after sanitization
decoder = DecoderSTL("TestFiles/SanitizerRandomTest/1/sanitized_sphere.STL")  # carrier's with secret filepath
decoder.DecodeFileFromSTL("TestFiles/SanitizerRandomTest/1/secret_after.STL")  # path to save the decoded carrier



# Test 2. Infiltrated picture of elephant
# Decoding before sanitization
decoder = DecoderSTL("TestFiles/SanitizerRandomTest/2/bunny.STL")  # carrier's with secret filepath
decoder.DecodeFileFromSTL("TestFiles/SanitizerRandomTest/2/secret_before.STL")  # path to save the decoded carrier

sanitizer = SanitizerRandom("TestFiles/SanitizerRandomTest/2/bunny.STL")  # carrier's filepath
sanitizer.Sanitize()
sanitizer.SaveSanitizedFile("TestFiles/SanitizerRandomTest/2/sanitized_bunny.STL")  # filepath destination for sanitized stl file

# Decoding after sanitization
decoder = DecoderSTL("TestFiles/SanitizerRandomTest/2/sanitized_bunny.STL")  # carrier's with secret filepath
decoder.DecodeFileFromSTL("TestFiles/SanitizerRandomTest/2/secret_after.STL")  # path to save the decoded carrier
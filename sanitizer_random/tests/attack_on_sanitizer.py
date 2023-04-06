import pytest
from sanitizer_random.lib.sanitizer_random import SanitizerRandom
from vertex_ch_encoder.lib.vertex_ch_encoder import EncoderSTL, DecoderSTL, base2, base3

from facet_ch_encoder.lib.facet_ch_encoder import EncoderSTL as FacetEncoderSTL, DecoderSTL as FacetDecoderSTL

SECRET_SIZE_BITS = 4 * 8  # size of any secret = 4 bytes


# Infiltrated text
def test_sanitize_only_vertex_but_info_in_facet_surviced():
    original_secret = "Secret"
    # inserting secret into facet channel
    facet_encoder = FacetEncoderSTL("test_objects/attack/original_sphere.STL", False)  # carrier's filepath
    facet_encoder.EncodeBytesInSTL(bytes(original_secret, "utf-8"), "test_objects/attack/encoded/encoded_sphere.STL")  # path to save the carrier with secret


    # sanitizing vertex channel
    sanitizer = SanitizerRandom("test_objects/attack/encoded/encoded_sphere.STL")  # carrier's filepath
    sanitizer.SanitizeVertexCh(SECRET_SIZE_BITS)
    sanitizer.SaveSanitizedFile(
        "test_objects/attack/sanitized/sanitized_sphere.STL")  # filepath destination for sanitized stl file


    # Decoding facet channel after sanitization
    decoder_after = FacetDecoderSTL("test_objects/attack/sanitized/sanitized_sphere.STL",False)  # carrier's with secret filepath
    secret_after = decoder_after.DecodeBytesFromSTL()  # path to save the decoded carrier

    assert original_secret == secret_after.decode()

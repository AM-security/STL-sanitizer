import math
import os

from TranformationLQ.TransformationLQ import TranformatorHQ2LQ
from EncodingDecodingVertexChLib.EncodingDecoding import EncoderSTL, DecoderSTL, base2

from EncodingDecodingFacetCh.EncodingDecodingFacetCh import EncoderSTL as EncoderFacet, DecoderSTL as DecoderFacet



def TransformBallAndRestoreBall():
    transformator = TranformatorHQ2LQ("tests/TransformationLQTest/ball.stl")
    transformator.TransformSTLFile("tests/TransformationLQTest/LQ_ball.stl")

    print("\n")

    recover = TranformatorHQ2LQ("tests/TransformationLQTest/LQ_ball.stl")
    recover.RestoreOriginalHQSTL("tests/TransformationLQTest/deserialization/recovered_HQ_ball.stl")


def TransformBunnyAndRestoreBunny():
    transformator = TranformatorHQ2LQ("tests/TransformationLQTest/bunny.stl")
    transformator.TransformSTLFile("tests/TransformationLQTest/LQ_bunny.stl")

    print("\n")
    recover = TranformatorHQ2LQ("tests/TransformationLQTest/LQ_bunny.stl")
    recover.RestoreOriginalHQSTL("tests/TransformationLQTest/deserialization/recovered_HQ_bunny.stl")

#
# TransformBallAndRestoreBall()
# TransformBunnyAndRestoreBunny()


def FullWatermarkSphere():
    # INSERT FACET WATERMARK
    encoderFacet = EncoderFacet("tests/TransformationLQTest/full_test/original_sphere.STL")  # carrier's filepath
    encoderFacet.EncodeBytesInSTL(bytes("Smith (c)", "utf-8"),"tests/TransformationLQTest/full_test/encoded_sphere.STL")  # path to save the carrier with secret

    decoderFacet = DecoderFacet("tests/TransformationLQTest/full_test/encoded_sphere.STL")  # carrier's with secret filepath
    watermark = decoderFacet.DecodeBytesFromSTL()  # path to save the decoded secret
    print(watermark.decode("utf-8"))
    print("\n")

    transformator = TranformatorHQ2LQ("tests/TransformationLQTest/full_test/encoded_sphere.STL")
    transformator.TransformSTLFile("tests/TransformationLQTest/full_test/encoded_sphere.STL", 1, 1000, 1000)

    print("\n")

    recover = TranformatorHQ2LQ("tests/TransformationLQTest/full_test/encoded_sphere.STL")
    recover.RestoreOriginalHQSTL("tests/TransformationLQTest/full_test/recovered_sphere.STL")


FullWatermarkSphere()
import math
import os

from TranformationLQ.TransformationLQ import TranformatorHQ2LQ
from EncodingDecodingVertexChLib.EncodingDecoding import EncoderSTL, DecoderSTL, base2



def TransformBallAndRestoreBall():
    transformator = TranformatorHQ2LQ("tests/TransformationLQTest/ball.stl")
    transformator.TransformSTLFile("tests/TransformationLQTest/LQ_ball.stl")

    print("\n")

    recover = TranformatorHQ2LQ("tests/TransformationLQTest/LQ_ball.stl")
    recover.RestoreOriginalHQSTL("tests/TransformationLQTest/deserialization/recovered_HQ_ball.stl")


# def TransformBunnyAndRestoreBunny():
#     transformator = TranformatorHQ2LQ("tests/TransformationLQTest/bunny.stl")
#     transformator.TransformSTLFile("tests/TransformationLQTest/LQ_bunny.stl")
#
#
#
#     print("\n")
#
#     decoder = DecoderSTL("tests/TransformationLQTest/encoded_LQ_bunny.stl")  # carrier's with secret filepath
#     sequence2 = decoder.DecodeBytesFromSTL(base2)
#
#     recover = TranformatorHQ2LQ("tests/TransformationLQTest/encoded_LQ_bunny.stl")
#     recover.RestoreOriginalHQSTL("tests/TransformationLQTest/deserialization/recovered_HQ_bunny.stl", sequence2)

#
TransformBallAndRestoreBall()
# TransformBunnyAndRestoreBunny()
# RestoreBall()
# TransformAndRestoreBall()
# TransformBunny()


# def Tmp():
#     x = -0.059928507
#     y = -0.059928507
#
#     if math.isclose(x, y):
#         print("EQUAL")
#     else:
#         print("NOT EQUAL")
#
# Tmp()

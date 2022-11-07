import math

from TranformationLQ.TransformationLQ import TranformatorHQ2LQ


def TransformBall():
    transformator = TranformatorHQ2LQ("tests/TransformationLQTest/ball.stl")
    transformator.TransformSTLFile("tests/TransformationLQTest/LQ_ball.stl")

    print("\n")


# def TransformBunny():
#     transformator = TranformatorHQ2LQ("tests/TransformationLQTest/bunny.STL")
#     transformator.TransformSTLFile("tests/TransformationLQTest/LQ_bunny.stl")
#
#     print("\n")
#
# def TransformAndRestoreBall():
#     transformator = TranformatorHQ2LQ("tests/TransformationLQTest/ball.stl")
#     transformator.TransformSTLFile("tests/TransformationLQTest/LQ_ball.stl")
#
#     print("\n")
#
#
def RestoreBall():
    recover = TranformatorHQ2LQ("tests/TransformationLQTest/LQ_ball.stl")
    recover.RestoreOriginalHQSTL("tests/TransformationLQTest/deserialization/recovered_HQ_ball.stl")
    print("\n")


TransformBall()
RestoreBall()
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
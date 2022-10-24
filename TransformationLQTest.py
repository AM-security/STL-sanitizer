from TranformationLQ.TransformationLQ import TranformatorHQ2LQ


def TransformBall():
    transformator = TranformatorHQ2LQ("tests/TransformationLQTest/ball.stl")
    transformator.TransformSTLFile("tests/TransformationLQTest/LQ_ball.stl")

    print("\n")


def TransformBunny():
    transformator = TranformatorHQ2LQ("tests/TransformationLQTest/bunny.STL")
    transformator.TransformSTLFile("tests/TransformationLQTest/LQ_bunny.stl")

    print("\n")

def TransformAndRestoreBall():
    transformator = TranformatorHQ2LQ("tests/TransformationLQTest/ball.stl")
    transformator.TransformSTLFile("tests/TransformationLQTest/LQ_ball.stl")

    print("\n")


def TransformAndRestoreBall():
    transformator = TranformatorHQ2LQ("tests/TransformationLQTest/deserialization/ball.stl")
    transformator.TransformAndEncodeIntoSTLFile("tests/TransformationLQTest/deserialization/LQ_ball.stl")

    recover = TranformatorHQ2LQ("tests/TransformationLQTest/deserialization/LQ_ball.stl")
    recover.RestoreOriginalHQSTL("tests/TransformationLQTest/deserialization/recovered_HQ_ball.stl")
    print("\n")


# TransformBall()
TransformAndRestoreBall()
# TransformBunny()

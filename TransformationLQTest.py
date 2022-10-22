from TranformationLQ.TransformationLQ import TranformatorHQ2LQ


# Test text. infiltrating secret.txt into sphere stl file
def TransformBall():

    transformator = TranformatorHQ2LQ("tests/TransformationLQTest/ball.stl")
    transformator.TransformSTLFile("tests/TransformationLQTest/LQ_ball.stl")

    print("\n")


TransformBall()
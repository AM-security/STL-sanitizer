import sys
sys.path.append("/home/alex/PycharmProjects/sanitizer-distinguisher")
from TranformationLQ.TransformationLQ import TranformatorHQ2LQ

if __name__ == '__main__':
    if len(sys.argv) > 3:
        print("wrong number of arguments")

    filepath = sys.argv[1]
    outfile = sys.argv[2]


    transformer = TranformatorHQ2LQ(filepath)
    transformer.TransformToCanonical(outfile)









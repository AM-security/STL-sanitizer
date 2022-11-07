import sys
sys.path.append("/home/alex/PycharmProjects/sanitizer-distinguisher")
from TranformationLQ.TransformationLQ import TranformatorHQ2LQ

if __name__ == '__main__':
    if len(sys.argv) > 3:
        print("wrong number of arguments")

    filepath = sys.argv[1]
    outfilepath = sys.argv[2]


    recover = TranformatorHQ2LQ(filepath)
    recover.RestoreOriginalHQSTL(outfilepath)








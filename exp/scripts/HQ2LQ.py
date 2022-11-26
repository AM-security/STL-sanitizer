import sys
sys.path.append("/home/alex/PycharmProjects/sanitizer-distinguisher")
from TranformationLQ.TransformationLQ import TranformatorHQ2LQ
from EncodingDecodingFacetCh.EncodingDecodingFacetCh import EncoderSTL as EncoderFacet, DecoderSTL as DecoderFacet

if __name__ == '__main__':
    if len(sys.argv) > 4:
        print("wrong number of arguments")

    filepath = sys.argv[1]

    fileout = sys.argv[2]

    transformator = TranformatorHQ2LQ(filepath)
    transformator.TransformSTLFile(fileout)

    print("\n")







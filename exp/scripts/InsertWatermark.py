import sys
sys.path.append("/home/alex/PycharmProjects/sanitizer-distinguisher")
from TranformationLQ.TransformationLQ import TranformatorHQ2LQ
from EncodingDecodingFacetCh.EncodingDecodingFacetCh import EncoderSTL as EncoderFacet, DecoderSTL as DecoderFacet

if __name__ == '__main__':
    if len(sys.argv) > 4:
        print("wrong number of arguments")

    filepath = sys.argv[1]
    watermark = sys.argv[2]

    fileout = sys.argv[3]

    # INSERT FACET WATERMARK
    encoderFacet = EncoderFacet(filepath, False)
    encoderFacet.EncodeBytesInSTL(bytes(watermark, "utf-8"),fileout)
    print("\n")






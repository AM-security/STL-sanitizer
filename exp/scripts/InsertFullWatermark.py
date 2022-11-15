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

    transformator = TranformatorHQ2LQ(fileout)
    transformator.TransformSTLFile(fileout)

    # recover = TranformatorHQ2LQ("protected_LQ_sphere.STL")
    # recover.RestoreOriginalHQSTL("recovered_HQ_sphere.STL")
    print("\n")


    # decoderFacet = DecoderFacet("protected_LQ_sphere.STL")  # carrier's with secret filepath
    # watermark_recpvered = decoderFacet.DecodeBytesFromSTL()  # path to save the decoded secret
    # print(watermark_recpvered.decode("utf-8"))






import sys
sys.path.append("/home/alex/PycharmProjects/sanitizer-distinguisher")
from EncodingDecodingFacetCh.EncodingDecodingFacetCh import DecoderSTL as DecoderFacet

if __name__ == '__main__':
    if len(sys.argv) > 3:
        print("wrong number of arguments")

    filepath = sys.argv[1]

    decoderFacet = DecoderFacet(filepath)  # carrier's with secret filepath
    watermark = decoderFacet.DecodeBytesFromSTL()  # path to save the decoded secret
    print("\n")
    print(watermark.decode("utf-8"))






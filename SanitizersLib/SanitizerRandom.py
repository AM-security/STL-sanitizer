from EncodingDecodingLib.EncodingDecoding import EncoderSTL, STLObject, LoadSTL, Facet
import secrets


class SanitizerRandom:
    def __init__(self, fn_encoded_stl):
        carrier_stl: STLObject = LoadSTL(fn_encoded_stl)
        self.carrier_stl: STLObject = carrier_stl

    def Sanitize(self):
        facets_num = self.carrier_stl.FacetsCount()

        for _ in range(facets_num):
            facet: Facet = self.carrier_stl.GetNextFacet()

            num_to_rotate: int = secrets.choice([0, 1, 2])  # Generate a random number of right rotations

            for _ in range(num_to_rotate):
                facet.RotateRight()

            self.carrier_stl.WriteToCurrentFacet(facet)

    def SaveSanitizedFile(self, fn_destination: str):
        file = open(fn_destination, "w")
        file.write(self.carrier_stl.string())
        file.close()

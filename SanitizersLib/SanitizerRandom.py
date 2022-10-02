from EncodingDecodingLib.EncodingDecoding import EncoderSTL, STLObject, LoadSTL, Facet
import secrets


#  In this sanitizer we will not sanitize the first 4 bytes for the sake of experiment
class SanitizerRandom:
    def __init__(self, fn_encoded_stl):
        carrier_stl: STLObject = LoadSTL(fn_encoded_stl)
        self.carrier_stl: STLObject = carrier_stl
        self.fn_carrier_stl = fn_encoded_stl

    def Sanitize(self, bits_to_skip: int):
        print('SanitizeFileSTL')
        print('    Carrier   ..: ' + self.fn_carrier_stl)
        facets_num = self.carrier_stl.FacetsCount()

        for i in range(facets_num):
            facet: Facet = self.carrier_stl.GetNextFacet()

            if i < bits_to_skip:
                continue

            num_to_rotate: int = secrets.choice([0, 1, 2])  # Generate a random number of right rotations

            for _ in range(num_to_rotate):
                facet.RotateRight()

            self.carrier_stl.WriteToCurrentFacet(facet)

        capacity: int = int(facets_num)
        sanitized: int = int(100 - (bits_to_skip * 100 / capacity))
        print('    Sanitized ..: ' + str(sanitized) + " % of the carrier")  # how much was sanitized

    def SaveSanitizedFile(self, fn_destination: str):
        file = open(fn_destination, "w")
        file.write(self.carrier_stl.string())
        print('    Save As ..: ' + fn_destination)
        print('    Sanitizing successful')
        file.close()

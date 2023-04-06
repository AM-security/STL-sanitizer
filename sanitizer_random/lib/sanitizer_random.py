# import secrets
from random import randint
import random
from vertex_ch_encoder.lib.vertex_ch_encoder import EncoderSTL, DecoderSTL, base2, base3, STLObject, LoadSTL, Facet


one_byte = 8

#  In this sanitizer we will not sanitize the first 4 bytes for the sake of experiment
def shuffle(array: list[Facet]) -> list[Facet]:
    n = len(array)
    for i in range(n - 1, 0, -1):
        # Pick a random index from 0 to i
        j = randint(0, i + 1)

        # Swap arr[i] with the element at random index
        array[i], array[j] = array[j], array[i]
    return array


class SanitizerRandom:
    def __init__(self, fn_encoded_stl):
        carrier_stl: STLObject = LoadSTL(fn_encoded_stl, False)
        self.carrier_stl: STLObject = carrier_stl
        self.fn_carrier_stl = fn_encoded_stl

    def SanitizeVertexCh(self, bits_to_skip: int):
        print('SanitizeFileSTL')
        print('    Carrier   ..: ' + self.fn_carrier_stl)
        facets_num = self.carrier_stl.FacetsCount()

        for i in range(facets_num):
            facet: Facet = self.carrier_stl.GetNextFacet()

            if i < bits_to_skip:
                continue

            # Generate a random number of right rotations
            # num_to_rotate: int = secrets.choice([0, 1, 2])  # CSPRNG
            num_to_rotate: int = random.choice([0, 1, 2])  # PRNG

            for _ in range(num_to_rotate):
                facet.RotateRight()

            self.carrier_stl.WriteToCurrentFacet(facet)

        capacity: int = int(facets_num)
        sanitized: int = int(100 - (bits_to_skip * 100 / capacity))
        print('    Sanitized ..: ' + str(sanitized) + " % of the carrier")  # how much was sanitized

    def SanitizeFacetCh(self, bits_to_skip: int):
        print('SanitizeFileSTL')
        print('    Carrier   ..: ' + self.fn_carrier_stl)
        shuffled_facets_array = shuffle(self.carrier_stl.facets[bits_to_skip*2:]) # 2 facets = 1 bit
        self.carrier_stl.facets = self.carrier_stl.facets[:bits_to_skip*2] + shuffled_facets_array

        facets_num = self.carrier_stl.FacetsCount()
        capacity: int = int(facets_num)
        sanitized: int = int(100 - (bits_to_skip * 100 / capacity))
        print('    Sanitized ..: ' + str(sanitized) + " % of the carrier")  # how much was sanitized

    # Fisher-Yates optimized implementation

    def SaveSanitizedFile(self, fn_destination: str):
        file = open(fn_destination, "w")
        file.write(self.carrier_stl.string())
        print('    Save As ..: ' + fn_destination)
        print('    Sanitizing successful')
        file.close()

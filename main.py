import sys
from string import Template


# 2 types of sanitizers
# The first one is noticeable because every facet has v1 bigger than v2 and v3 so the bit of every facet is always 1


# issues: 1) Parsing of STL files should be in another class
# 2) Encoder and when the STL object is initialized

class Vertex:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def string(self):
        return self.x + " " + self.y + " " + self.z


class Facet:
    def __init__(self, vertex_1, vertex_2, vertex_3, normal):
        self.vertex_1 = vertex_1
        self.vertex_2 = vertex_2
        self.vertex_3 = vertex_3
        self.normal = normal

    def string(self):
        string_facet = Template(
            '  facet normal $normal\n    outer loop\n      vertex $vertex1\n      vertex $vertex2\n      vertex '
            '$vertex3\n    endloop\n  endfacet')
        string_facet = string_facet.safe_substitute(normal=self.normal.string(), vertex1=self.vertex_1.string(),
                                                    vertex2=self.vertex_2.string(), vertex3=self.vertex_3.string())
        return string_facet


class STLObject:
    facets = []
    facet_idx = 0

    def __init__(self, filepath):
        file = open(filepath, 'r')

        line = file.readline()
        while True:
            words_in_line = line.split(" ")

            if words_in_line[0] == "endsolid":
                break
            if words_in_line[0] == "solid":
                words_in_line[1] = words_in_line[1].strip()
                self.obj_name = words_in_line[1]
            if words_in_line[0] == "facet":
                normal = Vertex(words_in_line[2], words_in_line[3], words_in_line[4])  # x,y,z
                line = file.readline()  # outer loop skip

                line = file.readline()  # vertice 1
                line = line.strip()
                words_in_line = line.split(" ")
                vertex_1 = Vertex(words_in_line[1], words_in_line[2], words_in_line[3])  # x,y,z

                line = file.readline()  # vertex 2
                line = line.strip()
                words_in_line = line.split(" ")

                vertex_2 = Vertex(words_in_line[1], words_in_line[2], words_in_line[3])  # x,y,z

                line = file.readline()  # vertex 2
                line = line.strip()
                words_in_line = line.split(" ")
                vertex_3 = Vertex(words_in_line[1], words_in_line[2], words_in_line[3])  # x,y,z

                self.facets.append(Facet(vertex_1, vertex_2, vertex_3, normal))

            line = file.readline()
            line = line.strip()

        file.close()

    def GetNextFacet(self):
        current_facet = self.facets[self.facet_idx]
        self.facet_idx += 1
        return current_facet

    def GetCurrentFacet(self):
        return self.facets[self.facet_idx]

    def WriteToCurrentFacet(self, facet):
        self.facets[self.facet_idx] = facet

    def FacetsCount(self):
        return len(self.facets)

    def string(self):
        facets_string = ""
        for facet in self.facets:
            f = facet.string()
            facets_string += facet.string() + "\n"

        facets_string = facets_string[:-1]
        stl_file_string = Template('solid $obj_name\n$facets\n' + 'endsolid $obj_name\n')
        stl_file_string = stl_file_string.safe_substitute(obj_name=self.obj_name, facets=facets_string)
        return stl_file_string


def Max(v1, v2):
    if float(v1.x) < float(v2.x):
        return v2
    if float(v1.y) < float(v2.y):
        return v2
    if float(v1.z) < float(v2.z):
        return v2

    return v1


class DecoderSTL:
    def __init__(self):
        self.STL_obj = None

    def SaveDecodedSecretSTL(self, secret_msg, filename_destination):
        file = open(filename_destination, "w")
        file.write(secret_msg)
        file.close()

    def DecodeMessageFromSTL(self, filename_encoded):

        carrier_stl_obj = STLObject(filename_encoded)
        self.STL_obj = carrier_stl_obj

        secret_size = self.DecodeSize()
        secret_msg = self.DecodeBytes(secret_size)
        return secret_msg

    def DecodeBit(self, facet):
        if facet.vertex_1 == Max(facet.vertex_1, Max(facet.vertex_2, facet.vertex_3)):
            return 1
        return 0

    def DecodeByte(self):
        byte_value = 0x00
        bit_mask = 0x80
        for i in range(0, 8):
            facet = self.STL_obj.GetNextFacet()
            if self.DecodeBit(facet) == 1:
                byte_value = byte_value | bit_mask

            bit_mask = bit_mask >> 1

        return byte_value

    def DecodeSize(self):
        size_in_bytes = bytes()
        for idx in range(0, 4):
            byte = self.DecodeByte()
            size_in_bytes.append(byte)

        size = int.from_bytes(size_in_bytes, "big")
        return size

    def DecodeBytes(self, secret_size):
        secret = bytes()
        for _ in secret_size:
            byte = self.DecodeByte()
            secret.append(byte)

        return secret


class EncoderSTL:
    def __init__(self):
        self.STL_obj = None

    def EncodeFileInSTL(self, filename_original_stl, filename_secret, filename_destination_stl):
        file_secret = open(filename_secret, "r")
        secret_bytes = file_secret.read()
        secret_size = len(secret_bytes)  # check that

        carrier_stl_obj = STLObject(filename_original_stl)
        self.STL_obj = carrier_stl_obj

        carrier_capacity = carrier_stl_obj.FacetsCount() / 8

        if carrier_capacity >= secret_size + 4:
            self.EncodeSize(secret_size)
            self.EncodeBytes(secret_bytes)
            self.SaveEncodedSTL(filename_destination_stl)

        file_secret.close()

    def EncodeBit(self, facet, bit_value):
        if bit_value == 1:
            if facet.vertex_1 == Max(facet.vertex_1, Max(facet.vertex_2, facet.vertex_3)):
                return
            elif facet.vertex_2 == Max(facet.vertex_1, Max(facet.vertex_2, facet.vertex_3)):
                # Rotate left
                facet.vertex_1, facet.vertex_2, facet.vertex_3 = facet.vertex_2, facet.vertex_3, facet.vertex_1
            else:
                # Rotate right
                facet.vertex_1, facet.vertex_2, facet.vertex_3 = facet.vertex_3, facet.vertex_1, facet.vertex_2
        else:
            if facet.vertex_1 == Max(facet.vertex_1, Max(facet.vertex_2, facet.vertex_3)):
                # Rotate Left
                facet.vertex_1, facet.vertex_2, facet.vertex_3 = facet.vertex_2, facet.vertex_3, facet.vertex_1

        self.STL_obj.WriteToCurrentFacet(facet)

    def EncodeByte(self, byte_value):
        bit_mask = 0x80
        for i in range(0, 8):
            facet = self.STL_obj.GetNextFacet()
            if byte_value & bit_mask:
                self.EncodeBit(facet, 1)
            else:
                self.EncodeBit(facet, 0)
            bit_mask = bit_mask >> 1

    def EncodeSize(self, secret_size):
        size_in_bytes = secret_size.to_bytes(4, 'big')
        for byte in size_in_bytes:

            self.EncodeByte(byte)

    def EncodeBytes(self, secret_bytes):
        for byte in secret_bytes:
            b = str.encode(byte)
            self.EncodeByte(b)

    def SaveEncodedSTL(self, fn_destination):
        file = open(fn_destination, "w")
        file.write(self.STL_obj)
        file.close()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    encoder = EncoderSTL()
    encoder.EncodeFileInSTL("1250_polygon_sphere_100mm.STL", "lol.txt", "encoded_1250.STL")

    decoder = DecoderSTL()
    secret = decoder.DecodeMessageFromSTL("encoded_1250.STL")
    print(secret)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/

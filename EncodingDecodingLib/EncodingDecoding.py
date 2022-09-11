from string import Template
import typing
import array
import hashlib


class Vertex:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    # Returns string representation of a vertex
    def string(self) -> str:
        return self.x + " " + self.y + " " + self.z


class Facet:
    def __init__(self, vertex_1: Vertex, vertex_2: Vertex, vertex_3: Vertex, normal: Vertex):
        self.vertex_1: Vertex = vertex_1
        self.vertex_2: Vertex = vertex_2
        self.vertex_3: Vertex = vertex_3
        self.normal: Vertex = normal

    # Returns string representation of a facet
    def string(self) -> str:
        string_facet = Template(
            '  facet normal $normal\n    outer loop\n      vertex $vertex1\n      vertex $vertex2\n      vertex '
            '$vertex3\n    endloop\n  endfacet')
        string_facet = string_facet.safe_substitute(normal=self.normal.string(), vertex1=self.vertex_1.string(),
                                                    vertex2=self.vertex_2.string(), vertex3=self.vertex_3.string())
        return string_facet


class STLObject:
    facets: list[Facet] = []
    facet_idx: int = -1

    def __init__(self, filepath):
        file = open(filepath, 'r')

        while True:
            words_in_line = file.readline().strip().split(" ")

            if words_in_line[0] == "endsolid":
                break
            if words_in_line[0] == "solid":
                self.obj_name = words_in_line[1].strip()
            if words_in_line[0] == "facet":
                normal: Vertex = Vertex(words_in_line[2], words_in_line[3], words_in_line[4])  # normal x,y,z
                file.readline()  # skip "outer loop" line

                xyz_vertex_1 = file.readline().strip().split(" ")
                vertex_1 = Vertex(xyz_vertex_1[1], xyz_vertex_1[2], xyz_vertex_1[3])  # vertex 1 x,y,z

                xyz_vertex_2 = file.readline().strip().split(" ")
                vertex_2 = Vertex(xyz_vertex_2[1], xyz_vertex_2[2], xyz_vertex_2[3])  # vertex 2 x,y,z

                xyz_vertex_3 = file.readline().strip().split(" ")
                vertex_3 = Vertex(xyz_vertex_3[1], xyz_vertex_3[2], xyz_vertex_3[3])  # vertex 3 x,y,z

                self.facets.append(Facet(vertex_1, vertex_2, vertex_3, normal))

        file.close()

    def GetNextFacet(self) -> Facet:
        self.facet_idx += 1
        current_facet = self.facets[self.facet_idx]
        return current_facet

    def WriteToCurrentFacet(self, facet):
        if self.facet_idx == -1:
            print("failed to write to current facet, wrong facet index")
        self.facets[self.facet_idx] = facet

    def FacetsCount(self) -> int:
        return len(self.facets)

    def string(self) -> str:
        facets_string = ""
        for facet in self.facets:
            facets_string += facet.string() + "\n"

        facets_string = facets_string[:-1]
        stl_file_string = Template('solid $obj_name\n$facets\n' + 'endsolid $obj_name\n')
        res = stl_file_string.safe_substitute(obj_name=self.obj_name, facets=facets_string)
        return res


class DecoderSTL:
    def __init__(self):
        self.STL_obj = None

    def SaveDecodedSecretInFile(self, secret_msg, filename_destination):
        file = open(filename_destination, "w")
        file.write(secret_msg)
        file.close()

    def DecodeFileFromSTL(self, fn_encoded: str, fn_secret_destination: str):
        print('DecodeFileFromSTL')
        print('    Carrier ...: ' + fn_encoded)
        print('    Save secret as ...: ' + fn_secret_destination)

        carrier_stl = LoadSTL(fn_encoded)
        self.STL_obj = carrier_stl

        secret_size = self.DecodeSize()
        secret_msg: str = self.DecodeBytes(secret_size)

        print('    Decoded ...: ' + str(len(secret_msg)) + ' Bytes')
        print('    Decoded MD5: ' + hashlib.md5(str.encode(secret_msg)).hexdigest())

        self.SaveDecodedSecretInFile(secret_msg, fn_secret_destination)
        print('    Decoding successful')

    def DecodeBit(self, facet) -> int:
        if facet.vertex_1 == Max(facet.vertex_1, Max(facet.vertex_2, facet.vertex_3)):
            return 1
        return 0

    def DecodeByte(self) -> int:
        byte_value: int = 0x00
        bit_mask: int = 0x80
        for i in range(0, 8):
            facet = self.STL_obj.GetNextFacet()
            if self.DecodeBit(facet) == 1:
                byte_value = byte_value | bit_mask

            bit_mask = bit_mask >> 1

        return byte_value

    def DecodeSize(self) -> int:
        size_in_bytes: bytearray = bytearray()
        for idx in range(0, 4):
            byte = self.DecodeByte()
            size_in_bytes.append(byte)

        size: int = int.from_bytes(size_in_bytes, "big")
        return size

    def DecodeBytes(self, secret_size: int) -> str:
        secret_msg: array = []
        for _ in range(0, secret_size):
            byte = self.DecodeByte()
            c = chr(byte)
            secret_msg.append(c)

        return "".join(secret_msg)


class EncoderSTL:
    def __init__(self):
        self.STL_obj: STLObject = None

    def EncodeFileInSTL(self, fn_original_stl: str, fn_secret: str, fn_destination_stl: str):
        print('EncodeFileInSTL')
        print('    Carrier ..: ' + fn_original_stl)
        print('    Save As ..: ' + fn_destination_stl)

        secret_bytes: str = open(fn_secret, "r").read()
        secret_size: int = len(secret_bytes)

        carrier_stl: STLObject = LoadSTL(fn_original_stl)
        self.STL_obj = carrier_stl

        carrier_capacity = carrier_stl.FacetsCount() / 8  # number of bytes

        print('    Capacity .: ' + str(carrier_capacity * 8) + ' bits (' + str(int(carrier_capacity)) + ' Bytes)')
        print('    Secret ...: ' + fn_secret + ' (' + str(secret_size) + ' Bytes)')
        print('    Secret MD5: ' + hashlib.md5(str.encode(secret_bytes)).hexdigest())

        if carrier_capacity >= secret_size + 4:
            self.EncodeSize(secret_size)
            self.EncodeBytes(secret_bytes)

            self.SaveEncodedSTL(fn_destination_stl)
            print('    Encoding successful')
            return

        print("Failed to encode secret into an STL file, carrier's capacity is not sufficient to encode the secret")

    def EncodeBit(self, facet: Facet, bit_value: int):
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

    def EncodeByte(self, byte_value: int):
        bit_mask: int = 0x80

        for i in range(0, 8):
            facet: Facet = self.STL_obj.GetNextFacet()
            if byte_value & bit_mask:
                self.EncodeBit(facet, 1)
            else:
                self.EncodeBit(facet, 0)
            bit_mask = bit_mask >> 1

    def EncodeSize(self, secret_size: int):
        size_in_bytes: bytes = secret_size.to_bytes(4, 'big')
        for byte in size_in_bytes:  # byte is represented as `int` unicode
            self.EncodeByte(byte)

    def EncodeBytes(self, secret_bytes):
        for byte in secret_bytes:
            byte = ord(byte)
            self.EncodeByte(byte)

    def SaveEncodedSTL(self, fn_destination):
        file = open(fn_destination, "w")
        file.write(self.STL_obj.string())
        file.close()


def LoadSTL(filepath: str) -> STLObject:
    return STLObject(filepath)


# strings concatenation and comparison
def MaxStringComparison(v1: Vertex, v2: Vertex) -> Vertex:
    v1_str = v1.string()
    v2_str = v2.string()
    if v1_str > v2_str:
        return v1
    else:
        return v2


# Collisions are possible using this approach, but the probability of them to happen is low because of float numbers
def MaxSumComparison(v1: Vertex, v2: Vertex) -> Vertex:
    if float(v1.x) + float(v1.y) + float(v1.z) > float(v2.x) + float(v2.y) + float(v2.z):
        return v1
    else:
        return v2


def MaxNumbersComparison(v1: Vertex, v2: Vertex) -> Vertex:
    # compare x coordinates. return Max(v1.x, v2.x)
    if float(v1.x) > float(v2.x):
        return v1
    elif float(v1.x) < float(v2.x):
        return v2

    # compare y coordinates. return Max(v1.y, v2.y)
    if float(v1.y) > float(v2.y):
        return v1
    elif float(v1.y) < float(v2.y):
        return v2

    # compare z coordinates. return Max(v1.z, v2.z)
    if float(v1.z) > float(v2.z):
        return v1
    elif float(v1.z) < float(v2.z):
        return v2

    return v2


# Default function for (v1,v2) comparison. configuration will be supported in the future
def Max(v1: Vertex, v2: Vertex) -> Vertex:
    return MaxSumComparison(v1, v2)

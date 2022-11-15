from string import Template
import typing
import os
import array
import hashlib
import numpy as np

base3 = "base3"
base2 = "base2"
byte_len_base3 = 6


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

    def RotateRight(self):
        return str(float(self.x)) + " " + str(float(self.y)) + " " + str(float(self.z))

    # Returns string representation of a facet
    def string(self) -> str:
        string_facet = Template(
            '  facet normal $normal\n    outer loop\n      vertex $vertex1\n      vertex $vertex2\n      vertex '
            '$vertex3\n    endloop\n  endfacet')
        string_facet = string_facet.safe_substitute(normal=self.normal.string(), vertex1=self.vertex_1.string(),
                                                    vertex2=self.vertex_2.string(), vertex3=self.vertex_3.string())
        return string_facet


class STLObject:

    def __init__(self, filepath, empty: bool):
        if empty:
            self.facets: list[Facet] = []
            self.facet_idx: int = -1
            self.obj_name = ""
            return
        self.facets: list[Facet] = []
        self.facet_idx: int = -1
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

    def GetNextFacet(self):
        self.facet_idx += 1
        if self.facet_idx > len(self.facets) - 1:
            return None
        current_facet = self.facets[self.facet_idx]
        return current_facet

    def WriteToCurrentFacet(self, facet):
        if self.facet_idx == -1:
            print("failed to write to current facet, wrong facet index")
            return
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

    def __init__(self, fn_encoded_stl: str, empty: bool):
        if empty:
            carrier_stl: STLObject = LoadSTL("", empty)
            self.carrier_stl: STLObject = carrier_stl
            self.fn_original_stl = ""
            return
        carrier_stl = LoadSTL(fn_encoded_stl, empty)
        self.carrier_stl = carrier_stl
        self.fn_encoded_stl = fn_encoded_stl

    def SaveDecodedSecretInFile(self, secret_msg, filename_destination):
        file = open(filename_destination, "wb")
        file.write(secret_msg)
        file.close()

    def DecodeFileFromSTL(self, fn_secret_destination: str, base: str):
        print('DecodeFileFromSTL')
        print('    Carrier ...: ' + self.fn_encoded_stl)
        print('    Save secret as ...: ' + fn_secret_destination)

        secret_size = self.DecodeSize(base)
        secret_msg = self.DecodeBytes(secret_size, base)
        secret_msg = bytes(secret_msg)

        print('    Decoded ...: ' + str(len(secret_msg)) + ' Bytes')
        print('    Decoded MD5: ' + hashlib.md5(secret_msg).hexdigest())

        self.SaveDecodedSecretInFile(secret_msg, fn_secret_destination)
        print('    Decoding successful')

    def DecodeBytesFromSTL(self, base: str) -> bytes:
        print('DecodeFileFromSTL')
        print('    Carrier ...: ' + self.fn_encoded_stl)

        secret_size = self.DecodeSize(base)
        secret_msg = self.DecodeBytes(secret_size, base)
        secret_msg = bytes(secret_msg)

        print('    Decoded ...: ' + str(len(secret_msg)) + ' Bytes')
        print('    Decoded MD5: ' + hashlib.md5(secret_msg).hexdigest())
        print('    Decoding successful')
        return secret_msg

    def DecodeBit(self, facet) -> int:
        if facet.vertex_1 == Max(facet.vertex_1, Max(facet.vertex_2, facet.vertex_3)):
            return 1
        return 0

    def DecodeBitBase3(self, facet) -> int:
        if facet.vertex_2 == Max(facet.vertex_2, Max(facet.vertex_1, facet.vertex_3)):
            return 2
        elif facet.vertex_1 == Max(facet.vertex_1, Max(facet.vertex_2, facet.vertex_3)):
            return 1
        else:
            return 0

    def DecodeByte(self) -> int:
        byte_value: int = 0x00
        bit_mask: int = 0x80

        for i in range(0, 8):
            facet = self.carrier_stl.GetNextFacet()
            if self.DecodeBit(facet) == 1:
                byte_value = byte_value | bit_mask

            bit_mask = bit_mask >> 1

        return byte_value
    def CheckIfAll1(self)-> bool:
        while True:
            facet = self.carrier_stl.GetNextFacet()
            if facet is None:
                return True
            if self.DecodeBit(facet) != 1:
                return False

    def DecodeByteBase3(self) -> int:
        ternary: str = ""

        for i in range(0, byte_len_base3):
            facet = self.carrier_stl.GetNextFacet()
            bit = self.DecodeBitBase3(facet)
            ternary = ternary + str(bit)

        res = int(ternary, 3)
        return res

    def DecodeSize(self, base: str) -> int:
        size_in_bytes: bytearray = bytearray()
        for idx in range(0, 4):
            byte = 0
            if base == base2:
                byte = self.DecodeByte()
            elif base == base3:
                byte = self.DecodeByteBase3()
            else:
                print("failed to decode size, wrong base")
                exit(1)
            size_in_bytes.append(byte)

        size: int = int.from_bytes(size_in_bytes, "big")
        return size

    def DecodeBytes(self, secret_size: int, base: str):
        secret_msg: array = []
        for _ in range(0, secret_size):
            byte = 0
            if base == base2:
                byte = self.DecodeByte()
            elif base == base3:
                byte = self.DecodeByteBase3()
            else:
                print("failed to decode bytes, wrong base")
                exit(1)
            secret_msg.append(byte)
        return secret_msg


class EncoderSTL:
    def __init__(self, fn_original_stl: str, empty: bool):
        if empty:
            carrier_stl: STLObject = LoadSTL("", empty)
            self.carrier_stl: STLObject = carrier_stl
            self.fn_original_stl = ""
        carrier_stl: STLObject = LoadSTL(fn_original_stl, empty)
        self.carrier_stl: STLObject = carrier_stl
        self.fn_original_stl = fn_original_stl

    def EncodeFileInSTL(self, fn_secret: str, fn_destination_stl: str, base: str):
        print('EncodeFileInSTL')
        print('    Carrier ..: ' + self.fn_original_stl)
        print('    Save As ..: ' + fn_destination_stl)

        secret_bytes = open(fn_secret, "rb").read()
        secret_size: int = len(secret_bytes)

        carrier_capacity = 0
        if base == base2:
            carrier_capacity = self.carrier_stl.FacetsCount() / 8  # number of bytes
            print('Base2 Capacity: ' + str(carrier_capacity * 8) + ' bits (' + str(int(carrier_capacity)) + ' Bytes)')
        if base == base3:
            carrier_capacity = self.carrier_stl.FacetsCount() / 6  # number of bytes
            print('Base3 Capacity: ' + str(carrier_capacity * 6) + ' bits (' + str(int(carrier_capacity)) + ' Bytes)')


        print('    Secret ...: ' + fn_secret + ' (' + str(secret_size) + ' Bytes)')
        print('    Secret MD5: ' + hashlib.md5(secret_bytes).hexdigest())

        if carrier_capacity >= secret_size + 4:
            self.EncodeSize(secret_size, base)
            self.EncodeBytes(secret_bytes, base)

            self.SaveEncodedSTL(fn_destination_stl)
            print('    Encoding successful')
            return

        print("Failed to encode secret into an STL file, carrier's capacity is not sufficient to encode the secret")

    def EncodeBytesInSTL(self, secret_bytes: bytes, fn_destination_stl: str, base: str):
        print('EncodeFileInSTL')
        print('    Carrier ..: ' + self.fn_original_stl)
        print('    Save As ..: ' + fn_destination_stl)

        secret_size: int = len(secret_bytes)

        carrier_capacity = 0
        if base == base2:
            carrier_capacity = self.carrier_stl.FacetsCount() / 8  # number of bytes
            print('Base2 Capacity: ' + str(carrier_capacity * 8) + ' bits (' + str(int(carrier_capacity)) + ' Bytes)')
        if base == base3:
            carrier_capacity = self.carrier_stl.FacetsCount() / 6  # number of bytes
            print('Base3 Capacity: ' + str(carrier_capacity * 6) + ' bits (' + str(int(carrier_capacity)) + ' Bytes)')


        print('    Secret ...: ' + ' (' + str(secret_size) + ' Bytes)')
        print('    Secret MD5: ' + hashlib.md5(secret_bytes).hexdigest())

        if carrier_capacity >= secret_size + 4:
            self.EncodeSize(secret_size, base)
            self.EncodeBytes(secret_bytes, base)

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

        self.carrier_stl.WriteToCurrentFacet(facet)

    def EncodeBitBase3(self, facet: Facet, bit_value: int):  # test it
        if bit_value != 2 and bit_value != 1 and bit_value != 0:
            print("failed to encode a bit value, not base 3")
            exit(1)
        if bit_value == 2:
            if facet.vertex_2 == Max(facet.vertex_2, Max(facet.vertex_1, facet.vertex_3)):
                return
            elif facet.vertex_1 == Max(facet.vertex_1, Max(facet.vertex_2, facet.vertex_3)):
                # Rotate right
                facet.vertex_1, facet.vertex_2, facet.vertex_3 = facet.vertex_3, facet.vertex_1, facet.vertex_2
            else:
                # Rotate left
                facet.vertex_1, facet.vertex_2, facet.vertex_3 = facet.vertex_2, facet.vertex_3, facet.vertex_1

        if bit_value == 1:
            if facet.vertex_1 == Max(facet.vertex_1, Max(facet.vertex_2, facet.vertex_3)):
                return
            elif facet.vertex_2 == Max(facet.vertex_2, Max(facet.vertex_1, facet.vertex_3)):
                # Rotate left
                facet.vertex_1, facet.vertex_2, facet.vertex_3 = facet.vertex_2, facet.vertex_3, facet.vertex_1
            else:
                # Rotate right
                facet.vertex_1, facet.vertex_2, facet.vertex_3 = facet.vertex_3, facet.vertex_1, facet.vertex_2
        if bit_value == 0:
            if facet.vertex_3 == Max(facet.vertex_3, Max(facet.vertex_1, facet.vertex_2)):
                return
            elif facet.vertex_2 == Max(facet.vertex_2, Max(facet.vertex_1, facet.vertex_3)):
                # Rotate right
                facet.vertex_1, facet.vertex_2, facet.vertex_3 = facet.vertex_3, facet.vertex_1, facet.vertex_2
            else:
                # Rotate left
                facet.vertex_1, facet.vertex_2, facet.vertex_3 = facet.vertex_2, facet.vertex_3, facet.vertex_1

        self.carrier_stl.WriteToCurrentFacet(facet)

    def EncodeByte(self, byte_value: int):
        bit_mask: int = 0x80

        for i in range(0, 8):
            facet: Facet = self.carrier_stl.GetNextFacet()
            if byte_value & bit_mask:
                self.EncodeBit(facet, 1)
            else:
                self.EncodeBit(facet, 0)
            bit_mask = bit_mask >> 1

    def EncodeByteBase3(self, byte_value: int):
        ternary = np.base_repr(byte_value, base=3)

        diff_len = byte_len_base3 - len(ternary)
        for i in range(0, diff_len):
            ternary = "0" + ternary

        # ternary is supposed to have len 6
        for i in range(0, len(ternary)):
            facet: Facet = self.carrier_stl.GetNextFacet()
            self.EncodeBitBase3(facet, int(ternary[i]))

    def EncodeSize(self, secret_size: int, base: str):
        size_in_bytes: bytes = secret_size.to_bytes(4, 'big')
        for byte in size_in_bytes:  # byte is represented as `int` unicode
            if base == base2:
                self.EncodeByte(byte)
            if base == base3:
                self.EncodeByteBase3(byte)


    def EncodeBytes(self, secret_bytes, base: str):
        for byte in secret_bytes:
            if base == base2:
                self.EncodeByte(byte)
            if base == base3:
                self.EncodeByteBase3(byte)

    def WriteAll1(self):
        while True:
            facet = self.carrier_stl.GetNextFacet()
            if facet is None:
                return
            self.EncodeBit(facet, 1)

    def SaveEncodedSTL(self, fn_destination):
        file = open(fn_destination, "w")
        file.write(self.carrier_stl.string())
        file.flush()
        os.fsync(file)
        file.close()


def LoadSTL(filepath: str, empty: bool) -> STLObject:
    return STLObject(filepath, empty)


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


# IT DOESN'T WORK
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
    return MaxStringComparison(v1, v2)

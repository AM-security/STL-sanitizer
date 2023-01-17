from string import Template
import typing
import array
import hashlib
import os
import numpy as np


class Vertex:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    # Returns string representation of a vertex
    def string(self) -> str:
        return str(float(self.x)) + " " + str(float(self.y)) + " " + str(float(self.z))


class Facet:
    def __init__(self, vertex_1: Vertex, vertex_2: Vertex, vertex_3: Vertex, normal: Vertex):
        self.vertex_1: Vertex = vertex_1
        self.vertex_2: Vertex = vertex_2
        self.vertex_3: Vertex = vertex_3
        self.normal: Vertex = normal

    def RotateRight(self):
        self.vertex_1, self.vertex_2, self.vertex_3 = self.vertex_3, self.vertex_1, self.vertex_2

    # Returns string representation of a facet
    def string(self) -> str:
        string_facet = Template(
            '  facet normal $normal\n    outer loop\n      vertex $vertex1\n      vertex $vertex2\n      vertex '
            '$vertex3\n    endloop\n  endfacet')
        string_facet = string_facet.safe_substitute(normal=self.normal.string(), vertex1=self.vertex_1.string(),
                                                    vertex2=self.vertex_2.string(), vertex3=self.vertex_3.string())
        return string_facet


class PairFacets:
    def __init__(self, f1: Facet, f2: Facet):
        self.facet_1 = f1
        self.facet_2 = f2


class STLObject:

    def __init__(self, filepath, empty: bool):
        if empty:
            self.facets: list[Facet] = []
            self.facet_idx: int = -1
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

    def GetNextPairFacet(self):
        self.facet_idx += 1
        if self.facet_idx > len(self.facets) - 1:
            return None
        current_facet = self.facets[self.facet_idx]
        self.facet_idx += 1
        if self.facet_idx > len(self.facets) - 1:
            return None
        current_next_facet = self.facets[self.facet_idx]

        return PairFacets(current_facet, current_next_facet)

    def WriteToCurrentFacets(self, pair_facets: PairFacets):
        if self.facet_idx == -1:
            print("failed to write to current facet, wrong facet index")
            return
        self.facets[self.facet_idx - 1] = pair_facets.facet_1
        self.facets[self.facet_idx] = pair_facets.facet_2

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

    def DecodeFileFromSTL(self, fn_secret_destination: str):
        print('Decode Bytes Facet Channel')
        print('    Carrier ...: ' + self.fn_encoded_stl)
        print('    Save secret as ...: ' + fn_secret_destination)

        secret_size = self.DecodeSize()
        secret_msg = self.DecodeBytes(secret_size)
        secret_msg = bytes(secret_msg)

        print('    Decoded ...: ' + str(len(secret_msg)) + ' Bytes')
        print('    Decoded MD5: ' + hashlib.md5(secret_msg).hexdigest())

        self.SaveDecodedSecretInFile(secret_msg, fn_secret_destination)
        print('    Decoding successful')

    def DecodeBytesFromSTL(self) -> bytes:
        print('DecodeFileFromSTL')
        print('    Carrier ...: ' + self.fn_encoded_stl)

        secret_size = self.DecodeSize()
        secret_msg = self.DecodeBytes(secret_size)
        secret_msg = bytes(secret_msg)

        print('    Decoded ...: ' + str(len(secret_msg)) + ' Bytes')
        print('    Decoded MD5: ' + hashlib.md5(secret_msg).hexdigest())
        print('    Decoding successful')

        return secret_msg

    def DecodeBit(self, pair_facets: PairFacets) -> int:
        if pair_facets.facet_1 == Max(pair_facets.facet_1, pair_facets.facet_2):
            return 1
        return 0

    def DecodeByte(self) -> int:
        byte_value: int = 0x00
        bit_mask: int = 0x80

        for i in range(0, 8):
            pair_facets = self.carrier_stl.GetNextPairFacet()
            if self.DecodeBit(pair_facets) == 1:
                byte_value = byte_value | bit_mask

            bit_mask = bit_mask >> 1

        return byte_value

    def CheckIfAll1(self) -> bool:
        while True:
            pair_facets = self.carrier_stl.GetNextPairFacet()
            if pair_facets is None:
                return True
            if self.DecodeBit(pair_facets) != 1:
                return False

    def DecodeSize(self) -> int:
        size_in_bytes: bytearray = bytearray()
        for idx in range(0, 4):
            byte = self.DecodeByte()
            size_in_bytes.append(byte)

        size: int = int.from_bytes(size_in_bytes, "big")
        return size

    def DecodeBytes(self, secret_size: int):
        secret_msg: array = []
        for _ in range(0, secret_size):
            byte = self.DecodeByte()
            secret_msg.append(byte)
        return secret_msg


class EncoderSTL:
    def __init__(self, fn_original_stl: str, empty: bool):
        if empty:
            carrier_stl: STLObject = LoadSTL(fn_original_stl, empty)
            self.carrier_stl: STLObject = carrier_stl
            self.fn_original_stl = ""
            return
        carrier_stl: STLObject = LoadSTL(fn_original_stl, empty)
        self.carrier_stl: STLObject = carrier_stl
        self.fn_original_stl = fn_original_stl

    def EncodeFileInSTL(self, fn_secret: str, fn_destination_stl: str):
        print('EncodeFileInSTL')
        print('    Carrier ..: ' + self.fn_original_stl)
        print('    Save As ..: ' + fn_destination_stl)

        secret_bytes = open(fn_secret, "rb").read()
        secret_size: int = len(secret_bytes)

        carrier_capacity = self.carrier_stl.FacetsCount() / 2 / 8  # number of bytes
        print('Capacity:...... ' + str(carrier_capacity * 8) + ' bits (' + str(int(carrier_capacity)) + ' Bytes)')

        print('    Secret ...: ' + fn_secret + ' (' + str(secret_size) + ' Bytes)')
        print('    Secret MD5: ' + hashlib.md5(secret_bytes).hexdigest())

        if carrier_capacity >= secret_size + 4:
            self.EncodeSize(secret_size)
            self.EncodeBytes(secret_bytes)

            self.SaveEncodedSTL(fn_destination_stl)
            print('    Encoding successful')
            return

        print("Failed to encode secret into an STL file, carrier's capacity is not sufficient to encode the secret")

    def EncodeBytesInSTL(self, secret_bytes: bytes, fn_destination_stl: str):
        print('Encode Bytes Facet Channel')
        print('    Carrier ..: ' + self.fn_original_stl)
        print('    Save As ..: ' + fn_destination_stl)

        secret_size: int = len(secret_bytes)

        carrier_capacity = self.carrier_stl.FacetsCount() / 2 / 8  # number of bytes
        print('Capacity:...... ' + str(carrier_capacity * 8) + ' bits (' + str(int(carrier_capacity)) + ' Bytes)')

        print('    Secret ...: ' + ' (' + str(secret_size) + ' Bytes)')
        print('    Secret MD5: ' + hashlib.md5(secret_bytes).hexdigest())
        if carrier_capacity >= secret_size + 4:
            self.EncodeSize(secret_size)
            self.EncodeBytes(secret_bytes)

            self.SaveEncodedSTL(fn_destination_stl)
            print('    Encoding successful')
            return

        print("Failed to encode secret into an STL file, carrier's capacity is not sufficient to encode the secret")

    def EncodeBit(self, pair_facets: PairFacets, bit_value: int):
        if bit_value == 1:
            if pair_facets.facet_1 == Max(pair_facets.facet_1, pair_facets.facet_2):
                return
            else:
                # Rotate
                pair_facets.facet_1, pair_facets.facet_2 = pair_facets.facet_2, pair_facets.facet_1
        else:
            if pair_facets.facet_2 == Max(pair_facets.facet_1, pair_facets.facet_2):
                return
            else:
                # Rotate
                pair_facets.facet_1, pair_facets.facet_2 = pair_facets.facet_2, pair_facets.facet_1

        self.carrier_stl.WriteToCurrentFacets(pair_facets)

    def EncodeByte(self, byte_value: int):
        bit_mask: int = 0x80

        for i in range(0, 8):
            pair_facets: PairFacets = self.carrier_stl.GetNextPairFacet()
            if byte_value & bit_mask:
                self.EncodeBit(pair_facets, 1)
            else:
                self.EncodeBit(pair_facets, 0)
            bit_mask = bit_mask >> 1

    def EncodeSize(self, secret_size: int):
        size_in_bytes: bytes = secret_size.to_bytes(4, 'big')
        for byte in size_in_bytes:  # byte is represented as `int` unicode
            self.EncodeByte(byte)

    def EncodeBytes(self, secret_bytes):
        for byte in secret_bytes:
            self.EncodeByte(byte)

    def WriteAll1(self):
        while True:
            pair_facets = self.carrier_stl.GetNextPairFacet()

            if pair_facets is None:
                return

            self.EncodeBit(pair_facets, 1)

    def SaveEncodedSTL(self, fn_destination):
        file = open(fn_destination, "w")
        file.write(self.carrier_stl.string())

        file.flush()
        os.fsync(file)
        file.close()


def LoadSTL(filepath: str, empty: bool) -> STLObject:
    return STLObject(filepath, empty)


# Default function for (f1,f2) comparison. configuration will be supported in the future
def Max(f1: Facet, f2: Facet) -> Facet:
    f1v1 = str(float(f1.vertex_1.x)) + str(float(f1.vertex_1.y)) + str(float(f1.vertex_1.z))
    f1v2 = str(float(f1.vertex_2.x)) + str(float(f1.vertex_2.y)) + str(float(f1.vertex_2.z))
    f1v3 = str(float(f1.vertex_3.x)) + str(float(f1.vertex_3.y)) + str(float(f1.vertex_3.z))

    f2v1 = str(float(f2.vertex_1.x)) + str(float(f2.vertex_1.y)) + str(float(f2.vertex_1.z))
    f2v2 = str(float(f2.vertex_2.x)) + str(float(f2.vertex_2.y)) + str(float(f2.vertex_2.z))
    f2v3 = str(float(f2.vertex_3.x)) + str(float(f2.vertex_3.y)) + str(float(f2.vertex_3.z))

    f1_array = [f1v1, f1v2, f1v3]
    f1_array.sort()

    f2_array = [f2v1, f2v2, f2v3]
    f2_array.sort()

    f1_str = ''.join(f1_array)
    f2_str = ''.join(f2_array)

    if f1_str > f2_str:
        return f1
    else:
        return f2

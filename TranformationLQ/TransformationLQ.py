import random
from string import Template
import typing
import array
import os
import hashlib
import numpy as np
import secrets
import struct
import math
import funcy
from EncodingDecodingVertexChLib.EncodingDecoding import EncoderSTL, DecoderSTL, base2


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
        self.vertex_1, self.vertex_2, self.vertex_3 = self.vertex_3, self.vertex_1, self.vertex_2

    # Returns string representation of a facet
    def string(self) -> str:
        string_facet = Template(
            '  facet normal $normal\n    outer loop\n      vertex $vertex1\n      vertex $vertex2\n      vertex '
            '$vertex3\n    endloop\n  endfacet')
        string_facet = string_facet.safe_substitute(normal=self.normal.string(), vertex1=self.vertex_1.string(),
                                                    vertex2=self.vertex_2.string(), vertex3=self.vertex_3.string())
        return string_facet


class STLObject:

    def __init__(self, filepath):
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

    def GetNextFacet(self) -> Facet:
        self.facet_idx += 1
        current_facet = self.facets[self.facet_idx]
        return current_facet

    def WriteToCurrentFacet(self, facet):
        if self.facet_idx == -1:
            print("failed to write to current facet, wrong facet index")
            return
        self.facets[self.facet_idx] = facet

    def WriteToSpecificFacet(self, facet: Facet, idx: int):
        if idx < 0:
            print("failed to write to specific facet, wrong facet index")
            return
        self.facets[idx] = facet

    def FacetsCount(self) -> int:
        return len(self.facets)

    def CurrentIdx(self) -> int:
        return self.facet_idx

    def string(self) -> str:
        facets_string = ""
        for facet in self.facets:
            facets_string += facet.string() + "\n"

        facets_string = facets_string[:-1]
        stl_file_string = Template('solid $obj_name\n$facets\n' + 'endsolid $obj_name\n')
        res = stl_file_string.safe_substitute(obj_name=self.obj_name, facets=facets_string)
        return res


class OldNewPair:
    def __init__(self, v_old: Vertex, v_new: Vertex):
        self.v_old = v_old
        self.v_new = v_new

    def IsOldOrNew(self, v: Vertex):
        if v == self.v_old or v == self.v_new:
            return True
        return False


def AreTwoVerticesEqual(v1: Vertex, v2: Vertex) -> bool:
    #     if math.isclose(float(modified_facet.vertex_2.x), new_x1):
    x_equal = math.isclose(float(v1.x), float(v2.x))
    y_equal = math.isclose(float(v1.y), float(v2.y))
    z_equal = math.isclose(float(v1.z), float(v2.z))

    if x_equal and y_equal and z_equal:
        return True
    return False


class TranformatorHQ2LQ:
    def __init__(self, fn_original_stl: str):
        carrier_stl: STLObject = LoadSTL(fn_original_stl)
        self.carrier_stl: STLObject = carrier_stl
        self.fn_original_stl = fn_original_stl
        self.LQ2HQ_List: list[OldNewPair] = []
        self.new_vertices_cache: list[Vertex] = []
        self.single_sequence_size = 49

    def GenerateSTLTransormation(self) -> list[OldNewPair]:
        capacity = self.carrier_stl.FacetsCount() / 8
        # capacity = capacity - 4  # the first thing we do is to ensure space for the size of the secret

        while capacity > self.single_sequence_size + 4:  # single sequence size + the size of the secret

            picked_old_vertex = self.PickVertexNotInCache()
            new_vertex = self.GenerateTransformationForVertex(picked_old_vertex)
            self.ApplyTransformationToRespectiveVertices(picked_old_vertex, new_vertex)

            self.LQ2HQ_List.append(OldNewPair(picked_old_vertex, new_vertex))

            capacity -= self.single_sequence_size

        return self.LQ2HQ_List

    def PickVertexNotInCache(self) -> Vertex:
        picked_vertex = self.PickRandomVertexFromCarrier()
        if picked_vertex in self.new_vertices_cache:
            ctr = 0
            while True:
                picked_vertex = self.PickRandomVertexFromCarrier()
                if picked_vertex not in self.new_vertices_cache:
                    break
                ctr += 1
                if ctr > 100:
                    exit("ERROR, infinite loop")
        return picked_vertex

    def PickRandomVertexFromCarrier(self) -> Vertex:
        number_of_facets = self.carrier_stl.FacetsCount()
        random_facet_idx = random.choice(range(0, number_of_facets - 1))

        random_vertex = random.choice(range(1, 4))
        if random_vertex == 1:
            return self.carrier_stl.facets[random_facet_idx].vertex_1
        if random_vertex == 2:
            return self.carrier_stl.facets[random_facet_idx].vertex_2
        if random_vertex == 3:
            return self.carrier_stl.facets[random_facet_idx].vertex_3

    def GenerateTransformationForVertex(self, v: Vertex) -> Vertex:

        old_coordinates: list[float] = [float(v.x), float(v.y), float(v.z)]
        new_coordinates: list[float] = []
        for coordinate in old_coordinates:
            sign: int = secrets.choice([0, 1])  # 0 is "-", 1 is "+"
            number = random.choice(range(1, 900))
            change = number / 100  # 0.0001 - 0.0009
            new_coordinate = self.TransformCoordinate(coordinate, change, sign)
            new_coordinates.append(new_coordinate)

        new_vertex = Vertex(str(new_coordinates[0]), str(new_coordinates[1]), str(new_coordinates[2]))
        return new_vertex

    def ApplyTransformationToRespectiveVertices(self, old_vertex: Vertex, new_vertex: Vertex):
        # start looking for old_vertex
        affected_facets_idx: list[int]
        affected_vertices_in_facet: list[int]
        for f in self.carrier_stl.facets:
            if old_vertex.string() == f.vertex_1.string():
                f.vertex_1 = new_vertex
            if old_vertex.string() == f.vertex_2.string():
                f.vertex_2 = new_vertex
            if old_vertex.string() == f.vertex_3.string():
                f.vertex_3 = new_vertex
        # add to cache
        self.new_vertices_cache.append(new_vertex)

    def TransformCoordinate(self, coordinate: float, change: float, sign: int) -> float:
        new_coordinate: float
        if sign == 0:
            new_coordinate = coordinate - change
        else:
            new_coordinate = coordinate + change

        return new_coordinate

    def TransformSTLFile(self, fn_destination_stl: str):
        print('TransformSTLFile')
        capacity = self.carrier_stl.FacetsCount() / 8
        print('Vertex Capacity .: ' + str(capacity) + ' bytes')

        old_new_pair: list[OldNewPair] = self.GenerateSTLTransormation()

        secret_sequence: bytes = self.EncodeLQ2HQSequence(old_new_pair)

        print('Secret length ...: ' + str(len(secret_sequence)))
        if len(secret_sequence) > capacity:
            print('ERROR: Capacity exceeded')
            return

        encoder = EncoderSTL(self.fn_original_stl)  # fake loading
        encoder.carrier_stl = self.carrier_stl  # switching
        encoder.fn_original_stl = self.fn_original_stl

        print(secret_sequence.hex())

        encoder.EncodeBytesInSTL(secret_sequence, fn_destination_stl, base2)

        print('    Transformation successful')
        return

    # This function is supposed to be called in a separate class
    def RestoreOriginalHQSTL(self, fn_destination_stl: str):
        print('RestoreSTLFile')
        print('    Carrier ..: ' + self.fn_original_stl)
        print('    Save As ..: ' + fn_destination_stl)
        capacity = self.carrier_stl.FacetsCount() / 8
        print('Vertex Capacity .: ' + str(capacity) + ' bytes')
        print("\n")

        decoder = DecoderSTL(self.fn_original_stl)

        sequence = decoder.DecodeBytesFromSTL(base2)

        print('Secret length ...: ' + str(len(sequence)))

        old_new_pairs: list[OldNewPair] = self.DecodeLQ2HQSequence(sequence)

        for pair in old_new_pairs:
            self.ApplyTransformationToRespectiveVertices(pair.v_new, pair.v_old)

        self.SaveTransformedSTL(fn_destination_stl)
        print('    Restoring successful')
        return

    def EncodeLQ2HQSequence(self, lq2hq: list[OldNewPair]) -> bytes:
        secret: bytes = bytes()
        for pair in lq2hq:
            method: bytearray = bytearray(b'\x05')
            old_x: bytearray = bytearray(struct.pack("d", float(pair.v_old.x)))
            old_y: bytearray = bytearray(struct.pack("d", float(pair.v_old.y)))
            old_z: bytearray = bytearray(struct.pack("d", float(pair.v_old.z)))

            new_x: bytearray = bytearray(struct.pack("d", float(pair.v_new.x)))
            new_y: bytearray = bytearray(struct.pack("d", float(pair.v_new.y)))
            new_z: bytearray = bytearray(struct.pack("d", float(pair.v_new.z)))

            secret += method + old_x + old_y + old_z + new_x + new_y + new_z


        return secret

    def DecodeLQ2HQSequence(self, lq2hq: bytes) -> list[OldNewPair]:

        old_new_pair: list[OldNewPair] = []

        chunks: list[bytes] = list(funcy.chunks(self.single_sequence_size, lq2hq))
        for ch in chunks:
            if len(ch) != self.single_sequence_size:
                exit("ERROR: sequence size is wrong. Expected " + str(self.single_sequence_size) + " got " + str(
                    len(ch)))

            method = ch[0]
            [old_x] = struct.unpack("d", ch[1:9])
            [old_y] = struct.unpack("d", ch[9:17])
            [old_z] = struct.unpack("d", ch[17:25])

            [new_x] = struct.unpack("d", ch[25:33])
            [new_y] = struct.unpack("d", ch[33:41])
            [new_z] = struct.unpack("d", ch[41:49])

            old_vertex: Vertex = Vertex(str(old_x), str(old_y), str(old_z))
            new_vertex: Vertex = Vertex(str(new_x), str(new_y), str(new_z))

            old_new_pair.append(OldNewPair(old_vertex, new_vertex))

        return old_new_pair

    def SaveTransformedSTL(self, fn_destination):
        file = open(fn_destination, "w")
        file.write(self.carrier_stl.string())
        file.flush()
        os.fsync(file)
        file.close()


def LoadSTL(filepath: str) -> STLObject:
    return STLObject(filepath)

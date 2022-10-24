import random
from string import Template
import typing
import array
import hashlib
import numpy as np
import secrets
import struct
import math

base3 = "base3"
base2 = "base2"
byte_len_base3 = 6


class Vertex:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.Affected = False

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

    def IsAffected(self):
        if self.vertex_1.Affected or self.vertex_2.Affected or self.vertex_3.Affected:
            return True
        else:
            return False
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


class CoordinateRecovery:
    def __init__(self, change: int, sign: str):
        self.change = change
        self.sign = sign


class VertexRecovery:
    def __init__(self, x_rec: CoordinateRecovery, y_rec: CoordinateRecovery, z_rec: CoordinateRecovery, new_x: float):
        self.x_rec = x_rec
        self.y_rec = y_rec
        self.z_rec = z_rec
        self.new_x: float = new_x


class FacetRecovery:
    def __init__(self, facet_num: int, v1: VertexRecovery, v2: VertexRecovery, v3: VertexRecovery):
        self.facet_num: int = facet_num
        self.v1: VertexRecovery = v1
        self.v2: VertexRecovery = v2
        self.v3: VertexRecovery = v3


class RecoveredFacet:
    def __init__(self, facet_idx: int, f: Facet):
        self.facet_idx = facet_idx
        self.facet = f


class TransformationPair:
    def __init__(self, facet_recovery: FacetRecovery, new_facet: Facet):
        self.facet_recovery: FacetRecovery = facet_recovery
        self.new_facet = new_facet


class TranformatorHQ2LQ:
    def __init__(self, fn_original_stl: str):
        carrier_stl: STLObject = LoadSTL(fn_original_stl)
        self.carrier_stl: STLObject = carrier_stl
        self.fn_original_stl = fn_original_stl
        self.LQ2HQ_List: list[FacetRecovery] = []

        self.same_value_dict = {}
        self.same_value_dict_recovery = {}

        self.SingleSequenceSize = 34  # the size of a facet recovery sequence

        self.IsGenericFacet = True

    # vertex stego channel
    def GenerateFullSTLTransformation(self):
        number_of_facets = self.carrier_stl.FacetsCount()

        while number_of_facets > 1:
            cur_facet = self.carrier_stl.GetNextFacet()

            transformation_pair: TransformationPair = self.GenTransformedFacet(cur_facet)

            self.ApplySingleTranformation(transformation_pair.new_facet)

            number_of_facets -= 1

        return

    def GenerateSomeSTLTransformation(self) -> list[FacetRecovery]:
        capacity = self.carrier_stl.FacetsCount() / 8
        capacity = capacity - 4  # the first thing we do is to ensure space for the size of the secret

        while capacity > self.SingleSequenceSize + 4:  # single sequence size + the size of the secret
            affected = True
            cur_facet = self.carrier_stl.GetNextFacet()

            transformation_pair: TransformationPair = self.GenTransformedFacet(cur_facet, self.carrier_stl.facet_idx)

            self.ApplySingleTranformation(transformation_pair.new_facet)

            if affected:
                self.LQ2HQ_List.append(transformation_pair.facet_recovery)

            capacity -= self.SingleSequenceSize

            self.IsGenericFacet = False

        return self.LQ2HQ_List

    def ApplySingleTranformation(self, new_facet: Facet):
        self.carrier_stl.WriteToCurrentFacet(new_facet)

    # normal vector is the same
    def GenTransformedFacet(self, facet: Facet, facet_idx: int) -> TransformationPair:

        vertices_recovery: list[VertexRecovery] = []
        vertices: list[Vertex] = [facet.vertex_1, facet.vertex_2, facet.vertex_3]
        new_vertices: list[Vertex] = []
        for v in vertices:
            new_v, v_recovery = self.TransformVertex(v)
            new_vertices.append(new_v)
            vertices_recovery.append(v_recovery)

        facet_recovery: FacetRecovery = FacetRecovery(facet_idx, vertices_recovery[0], vertices_recovery[1],
                                                      vertices_recovery[2])
        new_facet = Facet(new_vertices[0], new_vertices[1], new_vertices[2], facet.normal)
        return TransformationPair(facet_recovery, new_facet)

    def IsAtLeastOneVertexCached(self, f: Facet) -> bool:
        if f.vertex_1.string() in self.same_value_dict:
            return True
        if f.vertex_2.string() in self.same_value_dict:
            return True
        if f.vertex_3.string() in self.same_value_dict:
            return True
        return False
    def TransformVertex(self, v: Vertex):

        if v.string() in self.same_value_dict:
            vertex_from_cache = self.same_value_dict.get(v.string())
            recovery_from_cache = self.same_value_dict_recovery.get(v.string())
            v.Affected = True
            return vertex_from_cache, recovery_from_cache
        else:

            coordinates: list[float] = [float(v.x), float(v.y), float(v.z)]
            new_coordinates: list[float] = []
            coordinates_recovery: list[CoordinateRecovery] = []

            for coordinate in coordinates:
                sign: int = secrets.choice([0, 1])  # 0 is "-", 1 is "+"
                number = random.choice(range(1, 9))
                change = number / 100  # 0.0001 - 0.0009
                new_coordinate = self.TransformCoordinate(coordinate, change, sign)
                new_coordinates.append(new_coordinate)

                operation: str
                if sign == 0:
                    operation = "+"  # the opposite
                else:
                    operation = "-"

                coordinates_recovery.append(CoordinateRecovery(number, operation))

            vertex_recovery = VertexRecovery(coordinates_recovery[0], coordinates_recovery[1], coordinates_recovery[2],
                                             new_coordinates[0])

            new_vertex = Vertex(str(new_coordinates[0]), str(new_coordinates[1]), str(new_coordinates[2]))

            self.same_value_dict[v.string()] = new_vertex
            self.same_value_dict_recovery[v.string()] = vertex_recovery

            return new_vertex, vertex_recovery

    def TransformCoordinate(self, coordinate: float, change: float, sign: int) -> float:
        new_coordinate: float
        if sign == 0:
            new_coordinate = coordinate - change
        else:
            new_coordinate = coordinate + change

        return new_coordinate  # check if it's updatable

    def TransformSTLFile(self, fn_destination_stl: str):
        print('TransformSTLFile')
        print('    Carrier ..: ' + self.fn_original_stl)
        print('    Save As ..: ' + fn_destination_stl)

        print('    Capacity .: ' + str(self.carrier_stl.FacetsCount() / 8) + ' bytes')

        # self.GenerateFullSTLTransformation()
        facets_recovery: list[FacetRecovery] = self.GenerateSomeSTLTransformation()

        secret_sequence: bytearray = self.EncodeLQ2HQSequence(facets_recovery)

        facets_recovery_decoded = self.DecodeLQ2HQSequence(secret_sequence) # TODO run some tests to compare

        # check if enough capacity for encoding the sequence

        self.SaveTransformedSTL(fn_destination_stl)
        print('    Transformation successful')
        return

    #
    # def GetLQ2HQSequence(self, lq2hq: list[Facet]):

    def EncodeLQ2HQSequence(self, lq2hq: list[FacetRecovery]) -> bytearray:
        secret: bytearray = bytearray()
        for f_recovery in lq2hq:
            facet_num_bytes: bytes = f_recovery.facet_num.to_bytes(4, 'big')

            vertices_recovery: list[VertexRecovery] = [f_recovery.v1, f_recovery.v2, f_recovery.v3]

            secret += facet_num_bytes

            for v_recovery in vertices_recovery:
                vertex_change_x: bytes = v_recovery.x_rec.change.to_bytes(1, 'big')
                change_sign_x: bytes = bytes(v_recovery.x_rec.sign, 'ascii')

                vertex_change_y: bytes = v_recovery.y_rec.change.to_bytes(1, 'big')
                change_sign_y: bytes = bytes(v_recovery.y_rec.sign, 'ascii')

                vertex_change_z: bytes = v_recovery.z_rec.change.to_bytes(1, 'big')
                change_sign_z: bytes = bytes(v_recovery.z_rec.sign, 'ascii')

                new_x: bytes = struct.pack('f', v_recovery.new_x)

                secret += vertex_change_x + change_sign_x + vertex_change_y + change_sign_y + vertex_change_z + change_sign_z + new_x

        return secret

    def RestoreFacetOrder(self, modified_facet: Facet, new_x1: float) -> Facet:
        if math.isclose(float(modified_facet.vertex_1.x), new_x1):
            return modified_facet
        if math.isclose(float(modified_facet.vertex_2.x), new_x1):
            # Rotate left
            modified_facet.vertex_1, modified_facet.vertex_2, modified_facet.vertex_3 = modified_facet.vertex_2, modified_facet.vertex_3, modified_facet.vertex_1
            return modified_facet
        if math.isclose(float(modified_facet.vertex_3.x), new_x1):
            # Rotate right
            modified_facet.vertex_1, modified_facet.vertex_2, modified_facet.vertex_3 = modified_facet.vertex_3, modified_facet.vertex_1, modified_facet.vertex_2
            return modified_facet

        print("Unexpected error, float numbers are not equal themselves")
        exit()

    def RestoreVertex(self, sequence: bytearray) -> VertexRecovery:
        i = 0
        change_x = int.from_bytes(sequence[i:i+1], "big")

        sign_x = sequence[i+1:i+2].decode("ascii")

        change_y = int.from_bytes(sequence[i+2:i+3], "big")
        sign_y = sequence[i+3:i+4].decode("ascii")

        change_z = int.from_bytes(sequence[i+4:i+5], "big")
        sign_z = sequence[i+5:i+6].decode("ascii")

        new_x_bytes: bytearray = bytearray()
        new_x_bytes.append(sequence[i + 6])
        new_x_bytes.append(sequence[i + 7])
        new_x_bytes.append(sequence[i + 8])
        new_x_bytes.append(sequence[i + 9])

        [new_x] = struct.unpack("f", new_x_bytes)

        x_recovery = CoordinateRecovery(change_x, sign_x)
        y_recovery = CoordinateRecovery(change_y, sign_y)
        z_recovery = CoordinateRecovery(change_z, sign_z)

        return VertexRecovery(x_recovery, y_recovery, z_recovery, new_x)

    def DecodeLQ2HQSequence(self, lq2hq: bytearray) -> list[FacetRecovery]:
        facet_recovery: list[FacetRecovery] = []
        i = 0
        while i < len(lq2hq):
            facet_num_bytes: bytearray = bytearray()
            facet_num_bytes.append(lq2hq[i])
            facet_num_bytes.append(lq2hq[i + 1])
            facet_num_bytes.append(lq2hq[i + 2])
            facet_num_bytes.append(lq2hq[i + 3])

            facet_num: int = int.from_bytes(facet_num_bytes, "big")

            v1_recovery = self.RestoreVertex(lq2hq[i+4:i+14])
            v2_recovery = self.RestoreVertex(lq2hq[i+14:i+24])
            v3_recovery = self.RestoreVertex(lq2hq[i+24:i+34])

            f = FacetRecovery(facet_num, v1_recovery, v2_recovery, v3_recovery)
            facet_recovery.append(f)
            i = i + 34

        return facet_recovery

    # def RestoreHQ(self, facets_recovery: list[FacetRecovery], stl_obj: ):


    def SaveTransformedSTL(self, fn_destination):
        file = open(fn_destination, "w")
        file.write(self.carrier_stl.string())
        file.close()


def LoadSTL(filepath: str) -> STLObject:
    return STLObject(filepath)

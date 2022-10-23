import random
from string import Template
import typing
import array
import hashlib
import numpy as np
import secrets

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


class TransformationPair:
    def __init__(self, orig_facet: Facet, new_facet: Facet):
        self.orig_facet: Facet = orig_facet
        self.new_facet = new_facet


class TranformatorHQ2LQ:
    def __init__(self, fn_original_stl: str):
        carrier_stl: STLObject = LoadSTL(fn_original_stl)
        self.carrier_stl: STLObject = carrier_stl
        self.fn_original_stl = fn_original_stl
        self.LQ2HQ_List: list[Facet] = []

        self.same_value_dict = {}

    # vertex stego channel
    def GenerateSTLTransformation(self) -> list[Facet]:
        number_of_facets = self.carrier_stl.FacetsCount()

        while number_of_facets > 1:
            cur_facet = self.carrier_stl.GetNextFacet()
            transformation_pair: TransformationPair = self.GenTransformedFacet(cur_facet)

            self.ApplySingleTranformation(transformation_pair.new_facet)

            self.LQ2HQ_List.append(transformation_pair.new_facet)

            number_of_facets -= 1

        return self.LQ2HQ_List

    def ApplySingleTranformation(self, new_facet: Facet):
        self.carrier_stl.WriteToCurrentFacet(new_facet)

    # normal vector is the same
    def GenTransformedFacet(self, facet: Facet) -> TransformationPair:
            vertices: list[Vertex] = [facet.vertex_1, facet.vertex_2, facet.vertex_3]
            new_vertices: list[Vertex] = []
            for v in vertices:
                new_v = self.TransformVertex(v)
                new_vertices.append(new_v)

            new_facet = Facet(new_vertices[0], new_vertices[1], new_vertices[2], facet.normal)
            return TransformationPair(facet, new_facet)

    def TransformVertex(self, v: Vertex) -> Vertex:
        if v.string() in self.same_value_dict:
            vertex_from_cache = self.same_value_dict.get(v.string())
            print('from cache')
            return vertex_from_cache
        else:

            coordinates: list[float] = [float(v.x), float(v.y), float(v.z)]
            new_coordinates: list[float] = []
            for coordinate in coordinates:
                sign: int = secrets.choice([0, 1])  # 0 is "-", 1 is "+"
                number = random.choice(range(1000, 80000))  # range(0.1,1) # 1000 - 10000 / 10000000
                change = number / 10000000

                new_coordinate = self.TransformCoordinate(coordinate, change, sign)
                new_coordinates.append(new_coordinate)

            new_vertex = Vertex(str(new_coordinates[0]), str(new_coordinates[1]), str(new_coordinates[2]))

            self.same_value_dict[v.string()] = new_vertex

            return new_vertex

    def TransformCoordinate(self, coordinate: float, change: float, sign: int) -> float:
        new_coordinate: float
        if sign == 0:
            new_coordinate = coordinate + change
        else:
            new_coordinate = coordinate - change

        return new_coordinate  # check if it's updatable

    def TransformSTLFile(self, fn_destination_stl: str):
        print('TransformSTLFile')
        print('    Carrier ..: ' + self.fn_original_stl)
        print('    Save As ..: ' + fn_destination_stl)

        LQ2HQ: list[Facet] = self.GenerateSTLTransformation()

        self.SaveTransformedSTL(fn_destination_stl)
        print('    Transformation successful')
        return

    def SaveTransformedSTL(self, fn_destination):
        file = open(fn_destination, "w")
        file.write(self.carrier_stl.string())
        file.close()


def LoadSTL(filepath: str) -> STLObject:
    return STLObject(filepath)

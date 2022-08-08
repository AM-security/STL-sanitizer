# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from string import Template


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

    def string(self):
        facets_string = ""
        for facet in self.facets:
            f = facet.string()
            facets_string += facet.string() + "\n"

        facets_string = facets_string[:-1]
        stl_file_string = Template('solid $obj_name\n$facets\n' + 'endsolid $obj_name\n')
        stl_file_string = stl_file_string.safe_substitute(obj_name=self.obj_name, facets=facets_string)
        return stl_file_string


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    obj = STLObject("1250_polygon_sphere_100mm.STL")
    string_obj = obj.string()
    f = open("new_obj.STL", "w")
    f.write(string_obj)
    f.close()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/

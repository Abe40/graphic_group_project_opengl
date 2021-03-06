import numpy as np


class ObjLoader:
    buffer = []

    def __int__(self,object_name):
        self.object_name = object_name

    def search_data(self, data_values, coordinates, skip, data_type):
        for d in data_values:
            if d == skip:
                continue
            if data_type == 'float':
                coordinates.append(float(d))
            elif data_type == 'int':
                coordinates.append(int(d) - 1)

    def create_sorted_vertex_buffer(self, indices_data, vertices, textures, normals):
        for i, ind in enumerate(indices_data):
            if i % 3 == 0:  # sort the vertex coordinates
                start = ind * 3
                end = start + 3
                ObjLoader.buffer.extend(vertices[start:end])
            elif i % 3 == 1:  # sort the texture coordinates
                start = ind * 2
                end = start + 2
                ObjLoader.buffer.extend(textures[start:end])
            elif i % 3 == 2:  # sort the normal vectors
                start = ind * 3
                end = start + 3
                ObjLoader.buffer.extend(normals[start:end])

    def create_unsorted_vertex_buffer(self, indices_data, vertices, textures, normals):
        num_verts = len(vertices) // 3

        for i1 in range(num_verts):
            start = i1 * 3
            end = start + 3
            ObjLoader.buffer.extend(vertices[start:end])

            for i2, data in enumerate(indices_data):
                if i2 % 3 == 0 and data == i1:
                    start = indices_data[i2 + 1] * 2
                    end = start + 2
                    ObjLoader.buffer.extend(textures[start:end])

                    start = indices_data[i2 + 2] * 3
                    end = start + 3
                    ObjLoader.buffer.extend(normals[start:end])

                    break

    def load_model(self, file, sorted=True):
        vert_coords = []
        tex_coords = []
        norm_coords = []

        all_indices = []
        indices = []
        with open(file, 'r') as f:
            line = f.readline()
            while line:
                values = line.split()
                if values[0] == 'v':
                    self.search_data(values, vert_coords, 'v', 'float')
                elif values[0] == 'vt':
                    self.search_data(values, tex_coords, 'vt', 'float')
                elif values[0] == 'vn':
                    self.search_data(values, norm_coords, 'vn', 'float')
                elif values[0] == 'f':
                    for value in values[1:]:
                        val = value.split('/')
                        self.search_data(val, all_indices, 'f', 'int')
                        indices.append(int(val[0]) - 1)
                line = f.readline()
        if sorted:
            self.create_sorted_vertex_buffer(all_indices, vert_coords, tex_coords, norm_coords)
        else:
            self.create_unsorted_vertex_buffer(all_indices, vert_coords, tex_coords, norm_coords)
        buffer = ObjLoader.buffer.copy()
        ObjLoader.buffer = []

        return np.array(indices, dtype='uint32'), np.array(buffer, dtype='float32')

class ReadMXC:
    def __init__(self, mxcfile):
        self.mxcfile = mxcfile
        self.materials = self.get_mat()

    def get_mat(self):
        materials = []
        with open(self.mxcfile, 'r') as f:
            material = None
            data = None
            for line in f:
                line = line.strip()
                if line == '<MAT>':
                    material = {}
                elif line == '<DATA>':
                    data = {}
                elif line == '<ENDDATA>':
                    if 'data' not in material:
                        material['data'] = []
                    material['data'].append(data)
                    data = None
                elif line == '<ENDMAT>':
                    materials.append(material)
                    material = None
                elif '=' in line and (material is not None or data is not None):
                    key, value = line.split('=', 1)
                    if data is not None:
                        data[key] = value
                    else:
                        material[key] = value
        return materials

    def find_material_by_muid(self, muid):
        for material in self.materials:
            if material['MUID'] == muid:
                return material
        return None

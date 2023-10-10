import re


def read_hha(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:

        parts_list = []
        materials_list = []

        content = f.read()

        for line in content.split('\n'):
            if line.strip().startswith('E'):
                # This regular expression matches either sequences of non-space characters
                # or sequences of characters inside double quotes.
                parts = re.findall(r'\"[^\"]+\"|\S+', line)

                part_dictionary = {
                    'e': parts[0],
                    'element_name': parts[2],
                    'part_name': parts[3],
                    'material_code': parts[4],
                    'material_name': parts[5],
                    'quantity': parts[6],
                    'length': parts[7],
                    'width': parts[8]
                                   }

                parts_list.append(part_dictionary)

            if line.strip().startswith('M'):
                materials = line.split('"')
                materials_list.append(materials[1])

        return {'materials': materials_list, 'parts': parts_list}

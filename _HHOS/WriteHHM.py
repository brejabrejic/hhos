from ReadCorpus.ReadCorpus import ReadMXC
import glob
import os


class ElmtexToHHM:
    def __init__(self, elmtex_folder, raw_board_path):
        super(ElmtexToHHM, self).__init__()
        self.elmtex_folder = elmtex_folder
        self.raw_board_path = raw_board_path
        self.mxc_files = self.get_mxc_files()

    @staticmethod
    def create_new_material(material_name, format_length, format_width, quantity, thickness):
        file_string = f""""HHOS 2.3.1.5 " 16
OO600.0 400.0 0.000 0.0 0.0 0.0 0.0 1 2 4 1 -1 -1 0 -1 -1 0 {thickness}.0 0 0.00 30.0 655 600.0 1500.0 0.000 0 9999.0 9999.0 9999.0 9999.0 0.300 0
OE-1 10.0 10.0 10.0 10.0 "" "" "" "" "" "{material_name}" "" ""
OM-1 -1 -1 0 0 25.0 0 4200 6500 0 1 0 -1 0 20.0 5.0 -1 1.0 -50.0 0 -1 1 500 0 500 0 15
OH"" 0 0.0 0.0 "" 0
OV"" 0 0.0 0.0 "" 0
OS0.0 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0 0
M0 "" {format_length}.0 {format_width}.0 {quantity} 0 100 10.0 10.0 10.0 10.0 -1 0 0 0 0.00 0"""

        return file_string


    def get_mxc_files(self):
        # Returns the path to all the MXC files inside of elmtex
        return [ReadMXC(mxc_file) for mxc_file in glob.glob(self.elmtex_folder + '/**/*.mxc', recursive=True)]


    def generate_raw_boards(self):
        for material_group in self.get_mxc_files():

            # Create path that follow the grouped materials from elmtex
            group_path = self.raw_board_path
            os.makedirs(group_path, exist_ok=True)

            for material in material_group.get_mat():

                # Initiate material path
                material_path = group_path

                # DATA
                for i, data in enumerate(material['data']):

                    # Get board dimensions
                    try:
                        length = data['DUZINA']
                        width = data['SIRINA']
                        thickness = data['DEB']
                    except KeyError:
                        # If there's no dimensions - 2800x2070x0mm will be the default value
                        length = '2800'
                        width = '2070'
                        thickness = '0'

                    # Path to the file we're going to write
                    new_hop_raw_board = os.path.join(material_path, f"{material['NAZIV'].replace(' ', '_')}_{thickness}mm.HHM")

                    with open(new_hop_raw_board, 'w') as nhrb:
                        # Initiate the string for writing inside the raw board .hop file
                        new_raw_board_material = self.create_new_material(f"{material['NAZIV'].replace(' ', '_')}_{thickness}mm",
                                                                          length,
                                                                          width,
                                                                          '1',
                                                                          thickness)
                        # Write the file
                        nhrb.write(new_raw_board_material)


# Test
# ElmtexToHHM('C:/Documents/Corpus 5/Elmtex', 'C:/TestHHM').generate_raw_boards()


class ModifyHHMFiles:
    def __init__(self, file_path):
        super(ModifyHHMFiles, self).__init__()
        self.file_path = file_path

    def open_file(self):
        with open(self.file_path, 'r', encoding='utf-8-sig') as f:
            new_content = []
            content = f.read()
            split_content = content.split('\n')

            for line in split_content:
                if line == '':
                    pass
                else:
                    new_content.append(line)

            return new_content

    def return_rest_parts(self):
        content = self.open_file()
        rest_parts = []
        for line in content:
            if line.strip().startswith('R'):
                rest_parts.append(line.split(' '))
        return rest_parts

    def next_rest_number(self):
        existing_rest_parts = self.return_rest_parts()
        next_rest_nr = 1
        for rest_part in existing_rest_parts:
            next_rest_nr = int(rest_part[0].replace('R', '')) + 1

        return next_rest_nr

    @staticmethod
    def rest_string(r_nr, leng, wid, quantity):
        r_string = f'R{r_nr} {leng}.0 {wid}.0 {quantity} 0 -1'
        return r_string

    def append_new_rest(self, length, width, quantity):
        content = self.open_file()
        new_rest = self.rest_string(self.next_rest_number(), str(length), str(width), str(quantity))

        # Find the first "B" line's index
        index_of_first_B = next((i for i, line in enumerate(content) if line.startswith('B')), None)

        if index_of_first_B is not None:
            # Insert the new_rest line before the first "B" line
            content.insert(index_of_first_B, new_rest)
        else:
            # If no "B" line was found, append to the end
            content.append(new_rest)

        # Write back to the file
        with open(self.file_path, 'w', encoding='utf-8-sig') as f:
            f.write('\n'.join(content))
        return new_rest



# Test
# ModifyHHMFiles('C:/TestHHM/w908_18mm.HHM').append_new_rest(300, 321, 1)

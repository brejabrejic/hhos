import re


class ReadHHMFiles:
    def __init__(self, file_path):
        super(ReadHHMFiles, self).__init__()
        self.file_path = file_path


    def open_file(self):
        with open(self.file_path, 'r', encoding='utf-8') as f:
            new_content = []
            content = f.read()
            split_content = content.split('\n')

            for line in split_content:
                if line == '':
                    pass
                else:
                    new_content.append(line)

            return new_content


    def return_thickness(self):
        content = self.open_file()
        return content[1].split(' ')[17]


    def return_material_name(self):
        content = self.open_file()
        material_info = re.findall(r'\"[^\"]+\"|\S+', content[2])
        return material_info

    def return_board_format(self):
        content = self.open_file()
        board_formats = []
        for line in content:
            if line.strip().startswith('M'):
                board_formats.append(line.split(' '))
        return board_formats

    def return_rest_parts(self):
        content = self.open_file()
        rest_parts = []
        for line in content:
            if line.strip().startswith('R'):
                rest_parts.append(line.split(' '))
        return rest_parts

    def return_jobs(self):
        content = self.open_file()
        jobs = []
        for line in content:
            if line.strip().startswith('B'):
                # Split the string by spaces not inside double quotes.
                job = [part.replace('"', '') for part in re.split(r' (?=(?:[^"]*"[^"]*")*[^"]*$)', line)]
                jobs.append(job)
        return jobs


def custom_split(line):
    words = []
    in_quotes = False  # Flag to check if we're inside quotes.
    word = ''
    for char in line:
        if char == '"':
            in_quotes = not in_quotes
        if char == ' ' and not in_quotes:
            words.append(word)
            word = ''
        else:
            word += char
    if word:  # Append any remaining word to the result.
        words.append(word)
    return words


def handle_a_line(line):
    boards_info = custom_split(line)
    boards_info = [board_info.strip('"') for board_info in boards_info]
    return boards_info


class ReadNcr:
    def __init__(self, file_path):
        self.file_path = file_path

    def read_ncr(self):
        with open(self.file_path, 'r', encoding='utf-8') as f:
            board_list = []
            board_status = []
            parts_list = []
            content = f.readlines()

            # Flags
            capture_next_line = False
            skip_next = False  # Flag to skip next line if it was already captured after 'I'

            a_output = []

            for index, line in enumerate(content):
                stripped_line = line.strip()

                if skip_next:  # Skip the line if it was already captured and reset the flag
                    skip_next = False
                    continue

                if stripped_line.startswith('I'):
                    try:
                        next_line = content[index + 1].strip()  # Check the line after 'I'
                        if next_line.startswith('A'):
                            a_output.append(handle_a_line(next_line + 'sranje2'))
                            skip_next = True  # After capturing the 'A' line, set skip_next to True
                    except IndexError:
                        pass

                if stripped_line.startswith('SA'):
                    customer_infos = custom_split(line)
                    customer_infos = [customer_info.strip('"') for customer_info in customer_infos]
                    job_name = customer_infos[0].replace('SA"', '')

                if stripped_line.startswith('M'):
                    boards = custom_split(line)
                    boards = [board.strip('"') for board in boards]
                    material_name = boards[20]
                    length = str(int(boards[4].replace('L', '')) / 10)
                    width = str(int(boards[5].replace('B', '')) / 10)
                    quantity = boards[7].replace('i', '')
                    board_dictionary = {
                        'material_name': material_name,
                        'length': length,
                        'width': width,
                        'quantity': quantity
                    }
                    board_list.append(board_dictionary)

                if stripped_line.startswith('I'):
                    parts = custom_split(line)
                    parts = [part.strip('"') for part in parts]
                    part_no = str(parts[0]).replace('I', '')
                    status = parts[1]
                    part_element = str(parts[2]).replace('Z"', '')
                    part_name = str(parts[9]).replace('p"', '')
                    length = str(int(str(parts[3]).replace('L', '')) / 10)
                    width = str(int(str(parts[4]).replace('B', '')) / 10)

                    parts_dictionary = {
                        'part_no': part_no,
                        'status': status,
                        'part_element': part_element,
                        'part_name': part_name,
                        'length': length,
                        'width': width
                    }
                    parts_list.append(parts_dictionary)

                if capture_next_line and (stripped_line.startswith('A1') or stripped_line.startswith('A0')):
                    a_output.append(handle_a_line(line))
                    capture_next_line = False  # Reset the flag

                # 'e' line logic
                if stripped_line == 'e' and not skip_next and content[index + 1].strip().startswith('A'):
                    capture_next_line = True

            for boards_status in a_output:
                status = boards_status[1]
                length = str(int(str(boards_status[8]).replace('L', '')) / 10)
                width = str(int(str(boards_status[9]).replace('B', '')) / 10)
                board_status_dictionary = {'status': status, 'length': length, 'width': width}
                board_status.append(board_status_dictionary)

        return {'job': job_name,
                'material_list': board_list,
                'parts_status': parts_list,
                'board_status': board_status,
                'total_parts': len(parts_list)
                }

    def read_ncr_work_order_info(self):
        with open(self.file_path, 'r', encoding='utf-8') as f:
            board_list = []
            board_status = []
            parts_list = []
            finished_parts = []
            non_finished_parts = []
            finished_boards = []
            non_finished_boards = []
            content = f.readlines()

            # Flags
            capture_next_line = False
            skip_next = False  # Flag to skip next line if it was already captured after 'I'

            a_output = []



            for index, line in enumerate(content):
                stripped_line = line.strip()

                if skip_next:  # Skip the line if it was already captured and reset the flag
                    skip_next = False
                    continue

                if stripped_line.startswith('I'):
                    try:
                        next_line = content[index + 1].strip()  # Check the line after 'I'
                        if next_line.startswith('A'):
                            a_output.append(handle_a_line(next_line+'sranje2'))
                            skip_next = True  # After capturing the 'A' line, set skip_next to True
                    except IndexError:
                        pass

                if stripped_line.startswith('SA'):
                    customer_infos = custom_split(line)
                    customer_infos = [customer_info.strip('"') for customer_info in customer_infos]
                    job_name = customer_infos[0].replace('SA"', '')


                if stripped_line.startswith('M'):
                    boards = custom_split(line)
                    boards = [board.strip('"') for board in boards]
                    material_name = boards[20]
                    length = str(int(boards[4].replace('L', ''))/10)
                    width = str(int(boards[5].replace('B', ''))/10)
                    quantity = boards[7].replace('i', '')
                    board_dictionary = {
                        'material_name': material_name,
                        'length': length,
                        'width': width,
                        'quantity': quantity
                    }
                    board_list.append(board_dictionary)


                if stripped_line.startswith('I'):
                    parts = custom_split(line)
                    parts = [part.strip('"') for part in parts]
                    part_no = str(parts[0]).replace('I', '')
                    status = parts[1]
                    part_element = str(parts[2]).replace('Z"', '')
                    part_name = str(parts[9]).replace('p"', '')
                    length = str(int(str(parts[3]).replace('L', ''))/10)
                    width = str(int(str(parts[4]).replace('B', ''))/10)

                    parts_dictionary = {
                        'part_no': part_no,
                        'status': status,
                        'part_element': part_element,
                        'part_name': part_name,
                        'length': length,
                        'width': width,
                        'timestamp': None
                    }
                    if parts_dictionary['status'] == 'S00000':
                        non_finished_parts.append(parts_dictionary)
                    else:
                        finished_parts.append(parts_dictionary)

                    parts_list.append(parts_dictionary)


                if capture_next_line and (stripped_line.startswith('A1') or stripped_line.startswith('A0')):
                    a_output.append(handle_a_line(line))
                    capture_next_line = False  # Reset the flag

                # Adjusted 'e' line logic
                if stripped_line == 'e' and not skip_next and content[index + 1].strip().startswith('A'):
                    capture_next_line = True


            for boards_status in a_output:
                status = boards_status[1]
                length = str(int(str(boards_status[14]).replace('L', ''))/10)
                width = str(int(str(boards_status[15]).replace('B', ''))/10)
                board_status_dictionary = {'status': status, 'length': length, 'width': width, 'timestamp': None}
                if board_status_dictionary['status'] == '0000':
                    non_finished_boards.append(board_status_dictionary)
                else:
                    finished_boards.append(board_status_dictionary)

                board_status.append(board_status_dictionary)

        return {'job': job_name,
                'material_list': board_list,
                'parts_status': parts_list,
                'board_status': board_status,
                'total_parts': len(parts_list),
                'total_boards': len(board_status),
                'finished_parts': finished_parts,
                'non_finished_parts': non_finished_parts,
                'finished_boards': finished_boards,
                'non_finished_boards': non_finished_boards
                }



    def read_ncr_part_info(self):
        with open(self.file_path, 'r', encoding='utf-8') as f:
            board_list = []
            board_status = []
            parts_list = []
            content = f.readlines()

            # Flags
            capture_next_line = False
            skip_next = False  # Flag to skip next line if it was already captured after 'I'

            a_output = []



            for index, line in enumerate(content):
                stripped_line = line.strip()

                if skip_next:  # Skip the line if it was already captured and reset the flag
                    skip_next = False
                    continue

                if stripped_line.startswith('I'):
                    try:
                        next_line = content[index + 1].strip()  # Check the line after 'I'
                        if next_line.startswith('A'):
                            a_output.append(handle_a_line(next_line+'sranje2'))
                            skip_next = True  # After capturing the 'A' line, set skip_next to True
                    except IndexError:
                        pass

                if stripped_line.startswith('SA'):
                    customer_infos = custom_split(line)
                    customer_infos = [customer_info.strip('"') for customer_info in customer_infos]
                    job_name = customer_infos[0].replace('SA"', '')


                if stripped_line.startswith('M'):
                    boards = custom_split(line)
                    boards = [board.strip('"') for board in boards]
                    material_name = boards[20]
                    length = str(int(boards[4].replace('L', ''))/10)
                    width = str(int(boards[5].replace('B', ''))/10)
                    quantity = boards[7].replace('i', '')
                    board_dictionary = {
                        'material_name': material_name,
                        'length': length,
                        'width': width,
                        'quantity': quantity
                    }
                    board_list.append(board_dictionary)


                if stripped_line.startswith('I'):
                    parts = custom_split(line)
                    parts = [part.strip('"') for part in parts]
                    part_no = str(parts[0]).replace('I', '')
                    status = parts[1]
                    part_element = str(parts[2]).replace('Z"', '')
                    part_name = str(parts[9]).replace('p"', '')
                    length = str(int(str(parts[3]).replace('L', ''))/10)
                    width = str(int(str(parts[4]).replace('B', ''))/10)

                    parts_dictionary = {
                        'part_no': part_no,
                        'status': status,
                        'part_element': part_element,
                        'part_name': part_name,
                        'length': length,
                        'width': width
                    }
                    # print(parts_dictionary)
                    parts_list.append(parts_dictionary)


                if capture_next_line and (stripped_line.startswith('A1') or stripped_line.startswith('A0')):
                    a_output.append(handle_a_line(line))
                    capture_next_line = False  # Reset the flag

                # Adjusted 'e' line logic
                if stripped_line == 'e' and not skip_next and content[index + 1].strip().startswith('A'):
                    capture_next_line = True


            for boards_status in a_output:
                status = boards_status[1]
                length = str(int(str(boards_status[8]).replace('L', ''))/10)
                width = str(int(str(boards_status[9]).replace('B', ''))/10)
                board_status_dictionary = {'status': status, 'length': length, 'width': width}
                board_status.append(board_status_dictionary)

        return {'job': job_name, 'material_list': board_list, 'parts_status': parts_list, 'board_status': board_status}

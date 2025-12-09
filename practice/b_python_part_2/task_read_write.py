"""
Read files from ./files and extract values from them.
Write one file with all values separated by commas.

Example:
    Input:

    file_1.txt (content: "23")
    file_2.txt (content: "78")
    file_3.txt (content: "3")

    Output:

    result.txt(content: "23, 78, 3")
"""

import os

def read_write(base_dir):
    """
    Reads files from the specified base_dir, extracts values, and
    writes one file ('result.txt') with all values separated by commas.
    """
    input_dir = base_dir + '/files'

    content = []

    for i in range(20):
        filename = f'file_{i + 1}.txt'
        file_path = os.path.join(input_dir, filename)

        if os.path.exists(file_path):
            with open(file_path, 'r', encoding="utf-8") as f:
                text = f.read().strip()
                content.append(text)
        else:
            pass

    output_file_path = os.path.join(input_dir, 'result.txt')

    os.makedirs(input_dir, exist_ok=True)

    with open(output_file_path, 'w', encoding="utf-8") as f:
        f.write(', '.join(content))

    return output_file_path
"""
Write tests for b_python_part_2/task_read_write.py task.
To write files during tests use temporary files:
https://docs.python.org/3/library/tempfile.html
https://docs.pytest.org/en/6.2.x/tmpdir.html
"""

import sys
from pathlib import Path

relative_module_path = Path('practice') / 'b_python_part_2'

absolute_module_dir = Path.cwd() / relative_module_path

if str(absolute_module_dir) not in sys.path:
    sys.path.insert(0, str(absolute_module_dir))

from task_read_write import read_write

def test_read_write_standard_case(tmp_path):
    """
    Tests the case where multiple input files exist and their content is correctly joined.
    We will only create a few files (1, 2, 3) to mimic the example and ensure
    the loop handles the missing files (4-20) correctly.
    """

    input_dir = tmp_path / 'files'
    input_dir.mkdir()

    file_data = {
        'file_1.txt': '23',
        'file_2.txt': '78',
        'file_3.txt': '3',
    }

    for name, content in file_data.items():
        (input_dir / name).write_text(content, encoding="utf-8")

    expected_output = "23, 78, 3"

    result_file_path = read_write(str(tmp_path))
    assert result_file_path == str(input_dir / 'result.txt')

    actual_output = (input_dir / 'result.txt').read_text(encoding="utf-8")
    assert actual_output == expected_output


def test_read_write_with_missing_files(tmp_path):
    """
    Tests that the script handles the 20-file loop correctly when only files 1 and 20 exist.
    """

    # Arrange: Setup the directory and only create files 1 and 20
    input_dir = tmp_path / 'files'
    input_dir.mkdir()

    (input_dir / 'file_1.txt').write_text("START", encoding="utf-8")
    (input_dir / 'file_20.txt').write_text("END", encoding="utf-8")

    expected_output = "START, END"

    read_write(str(tmp_path))
    actual_output = (input_dir / 'result.txt').read_text(encoding="utf-8")

    assert actual_output == expected_output


def test_read_write_no_input_files(tmp_path):
    """
    Tests the edge case where the './files' directory exists but is empty.
    """

    input_dir = tmp_path / 'files'
    input_dir.mkdir()

    expected_output = ""

    read_write(str(tmp_path))
    actual_output = (input_dir / 'result.txt').read_text(encoding="utf-8")

    assert actual_output == expected_output
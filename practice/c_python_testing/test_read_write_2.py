"""
Write tests for b_python_part_2/task_read_write_2.py task.
To write files during tests use temporary files:
https://docs.python.org/3/library/tempfile.html
https://docs.pytest.org/en/6.2.x/tmpdir.html
"""

import os
import pytest
import string
import random

def _generate_random_words(n=20):
    words = list()
    for _ in range(n):
        word = "".join(
            random.choices(string.ascii_lowercase, k=random.randint(3, 10))
        )
        words.append(word)
    return words


def generate_words(base_dir, words_to_write=None):
    if words_to_write is None:
        words = _generate_random_words(20)
    else:
        words = words_to_write

    files_dir = os.path.join(base_dir, 'files')
    os.makedirs(files_dir, exist_ok=True)

    content1 = "\n".join(words)
    file1_path = os.path.join(files_dir, "file1.txt")

    with open(file1_path, "w", encoding="utf-8", newline="\n") as file1:
        file1.write(content1)

    content2 = ",".join(words[::-1])
    file2_path = os.path.join(files_dir, "file2.txt")

    with open(file2_path, "w", encoding="cp1252", newline="") as file2:
        file2.write(content2)

    return words


TEST_WORDS = ['alpha', 'beta', 'gamma', 'delta', 'epsilon']


@pytest.fixture
def input_output_dir(tmp_path):
    return tmp_path / 'files'


def test_generate_words_content_and_encoding(tmp_path, input_output_dir):
    expected_content1 = "alpha\nbeta\ngamma\ndelta\nepsilon"
    expected_content2 = "epsilon,delta,gamma,beta,alpha"

    words_used = generate_words(str(tmp_path), words_to_write=TEST_WORDS)

    assert words_used == TEST_WORDS

    file1_path = input_output_dir / 'file1.txt'
    actual_content1 = file1_path.read_text(encoding="utf-8")
    assert actual_content1 == expected_content1

    file2_path = input_output_dir / 'file2.txt'
    actual_content2 = file2_path.read_text(encoding="cp1252")
    assert actual_content2 == expected_content2


def test_generate_words_encoding_edge_case(tmp_path, input_output_dir):
    cp1252_supported_word = ['fiancé']

    generate_words(str(tmp_path), words_to_write=cp1252_supported_word)

    file2_path = input_output_dir / 'file2.txt'
    actual_content2 = file2_path.read_text(encoding="cp1252")

    assert actual_content2 == 'fiancé'


def test_generate_words_empty_list(tmp_path, input_output_dir):
    generate_words(str(tmp_path), words_to_write=[])

    file1_path = input_output_dir / 'file1.txt'
    assert file1_path.read_text(encoding="utf-8") == ""

    file2_path = input_output_dir / 'file2.txt'
    assert file2_path.read_text(encoding="cp1252") == ""


def test_generate_words_single_word(tmp_path, input_output_dir):
    single_word = ['test']

    generate_words(str(tmp_path), words_to_write=single_word)

    file1_path = input_output_dir / 'file1.txt'
    assert file1_path.read_text(encoding="utf-8") == "test"

    file2_path = input_output_dir / 'file2.txt'
    assert file2_path.read_text(encoding="cp1252") == "test"
"""
Use function 'generate_words' to generate random words.
Write them to a new file encoded in UTF-8. Separator - '\n'.
Write second file encoded in CP1252, reverse words order. Separator - ','.

Example:
    Input: ['abc', 'def', 'xyz']

    Output:
        file1.txt (content: "abc\ndef\nxyz", encoding: UTF-8)
        file2.txt (content: "xyz,def,abc", encoding: CP1252)
"""

import os
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
    os.makedirs(files_dir, exist_ok=True)  # Ensure the directory exists

    content1 = "\n".join(words)
    file1_path = os.path.join(files_dir, "file1.txt")

    with open(file1_path, "w", encoding="utf-8", newline="\n") as file1:
        file1.write(content1)

    content2 = ",".join(words[::-1])  # words[::-1] reverses the list
    file2_path = os.path.join(files_dir, "file2.txt")

    with open(file2_path, "w", encoding="cp1252", newline="") as file2:
        file2.write(content2)

    return words
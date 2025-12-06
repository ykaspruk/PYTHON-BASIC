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


def generate_words(n=20):
    import string
    import random

    words = list()
    for _ in range(n):
        word = "".join(
            random.choices(string.ascii_lowercase, k=random.randint(3, 10))
        )
        words.append(word)

    content1 = "\n".join(words)
    file1 = open("./files/file1.txt", "w", encoding="utf-8", newline="\n")
    file1.write(content1)
    file1.close()

    content2 = ",".join(words[::-1])
    file2 = open("./files/file2.txt", "w", encoding="cp1252", newline="")
    file2.write(content2)
    file2.close()

    return words

if __name__ == "__main__":
    sample_words = generate_words(20)
    print("Wrote file1.txt (UTF-8) and file2.txt (CP1252).")
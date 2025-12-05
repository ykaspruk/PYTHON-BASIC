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

content = []

for i in range(20):
    f = open(f'./files/file_{i+1}.txt', 'r', encoding="utf-8")
    text = f.read()
    content.append(text)
    print(f'file_{i+1}.txt (content: "{text}")')
    f.close()

f = open('./files/result.txt', 'w', encoding="utf-8")
f.write(', '.join(content))
f.close()

f = open('./files/result.txt', 'r', encoding="utf-8")
print(f'result.txt (content: "{f.read()}"')
f.close()

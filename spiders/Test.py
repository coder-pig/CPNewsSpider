import re
import os

file_path = "test.xml"

test_pattern = re.compile('"news_li(.*?)', re.S)


def read_file(filename):
    with open(filename, encoding='UTF-8') as f:
        text = f.read()
        return text


if __name__ == '__main__':
    content = read_file(file_path)
    results = test_pattern.findall(content)
    for result in results:
        print(result[1])

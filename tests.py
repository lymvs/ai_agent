import unittest
from functions.get_files_info import get_file_content

def test():
    print(get_file_content("calculator", "main.py"))
    print(get_file_content("calculator", "pkg/calculator.py"))
    print(get_file_content("calculator", "/bin/cat"))

if __name__ == "__main__":
    test()
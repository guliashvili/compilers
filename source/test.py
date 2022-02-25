import json
from os import listdir
from os.path import isfile, join
from helper import execute, add_result, check_files, print_output
from hw1 import test_hw1

def main():
  msg = check_files()
  if msg:
    print_output(0, None, msg)

  test_hw1(False)
  print_output(None, None, None)


if __name__ == "__main__":
  main()






from helper import check_files, print_output
from hw1 import test_hw1
import os

def main():
  msg = check_files()
  if msg:
    print_output(0, None, msg)
  hw = os.getenv('hw')
  if hw == '1':
    test_hw1(True)
  elif hw == '2':
    pass
  else:
    pass
  print_output(None, None, None)


if __name__ == "__main__":
  main()




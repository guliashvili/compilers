from helper import check_files, print_output
from hw1 import test_hw1

def main():
  msg = check_files()
  if msg:
    print_output(0, None, msg)

  test_hw1(True)
  print_output(None, None, None)


if __name__ == "__main__":
  main()




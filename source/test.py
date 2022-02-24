import os
import sys
import json
from os.path import exists

CPP = "C++"
JAVA = "JAVA"


def print_output(tests, score, execution_time, output):
  output = {
    "execution_time": execution_time,
    "visibility": "visible",
    "stdout_visibility": "visible",
    "score": score,
    "output": output,
    "tests": tests
  }

  with open("results/results.json", "w") as f:
    f.write(json.dumps(output))

  quit()



def execute():
  pass

def test_homework_1():
  pass


def main():
  executable_type = None

  if exists("submission/tigerc"):
    executable_type = CPP
  elif exists("submission/tigerc.jar"):
    executable_type = JAVA
  else:
    print_output([], 0, None, "No binary found")




if __name__ == "__main__":
  main()


# execution_time = 0
tests = []





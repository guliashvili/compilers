import json
from os import listdir
from os.path import isfile, join

CPP = "C++"
CPP_FILE = "submission/tigerc"

JAVA = "JAVA"
JAVA_FILE = "submission/tigerc.jar"

G4_FILE = "submission/Tiger.g4"

tests = []

def print_output(score, execution_time, output):

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


from os.path import exists
def get_type():

  if exists(CPP_FILE):
    return CPP

  if exists(JAVA_FILE):
    return JAVA
  return None


def check_files():
  if get_type() is None:
    return "No binary found"

  if not exists(G4_FILE):
    return "No Tiger.g4 found"

  return None

def run_thing(commands):
  import subprocess

  process = subprocess.Popen(commands,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
  stdout, stderr = process.communicate()

  return stdout, stderr, process.returncode

def execute(args, f):
  commands = []
  if f is not None:
      commands.extend(['-i', f])

  executable_type = get_type()
  if executable_type == CPP:
    commands.append(CPP_FILE)
  else:
    commands.extend(["javac", JAVA_FILE])

  commands.extend(args)

  return run_thing(commands)


def add_result(score, max_score, name, number, output):
  tests.append({
            "score": score,
            "max_score": max_score,
            "name": name,
            "number": number,
            "output": output,
            "visibility": "visible",
        })


def executor(files, checker, title, chapter, max_score, args, is_test):
    counter = 1
    for f in files:
        f_name = f.replace(".tiger")
        f_name = f_name[f_name.rindex('/'):]

        message, success = "Unknown Exception", False
        try:
            stdout, stderr, retcode = execute(args, f)
            message, success = checker(f, stdout, stderr, retcode)
        except:
            pass

        if is_test:
            add_result(max_score * int(success),
                       max_score,
                       f"{chapter}.{counter}) {title}: {f_name}",
                       f"{chapter}.{counter}",
                       json.dumps({"stdout": stdout, "stderr": stderr, "retcode": retcode, "message": message})
                       )

        counter += 1
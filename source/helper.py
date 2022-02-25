import json
from os import listdir
from os.path import isfile, join

CPP = "C++"
CPP_FILE = "submission/cs8803_bin/tigerc"

JAVA = "JAVA"
JAVA_FILE = "submission/cs8803_bin/tigerc.jar"

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
    f.write(json.dumps(output,indent=4, sort_keys=True))

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

  executable_type = get_type()
  if executable_type == CPP:
    commands.append(CPP_FILE)
  else:
    commands.extend(["javac", JAVA_FILE])

  commands.extend(args)
  if f is not None:
      commands.extend(['-i', f])

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


def executor(files, checker, title, chapter, max_score, args, is_test, append_path):
    counter = 1
    for f_name in files:
        message, success = "Unknown Exception", False
        try:
            stdout, stderr, retcode = execute(args, append_path + f_name + ".tiger")
            if is_test:
                message, success = checker(f_name, stdout, stderr, retcode, append_path)
        except:
            pass

        if is_test:
            add_result(max_score * int(success),
                       max_score,
                       f"{title}: {f_name}",
                       f"{chapter}.{counter}",
                       json.dumps({
                           "stdout": stdout.decode("utf-8"),
                           "stderr": stderr.decode("utf-8"),
                           "retcode": retcode,
                           "message": message
                       },
                       indent=4, sort_keys=True)
                       )

        counter += 1
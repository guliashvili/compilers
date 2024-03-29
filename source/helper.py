import json
import uuid
import logging
import boto3
from botocore.exceptions import ClientError

CPP = "C++"
CPP_FILE = "../submission/cs8803_bin/tigerc"

JAVA = "JAVA"
JAVA_FILE = "../submission/cs8803_bin/tigerc.jar"

G4_FILE = "../submission/Tiger.g4"

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

  with open("../results/results.json", "w") as f:
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

def execute(args, f, irf):
  commands = []

  executable_type = get_type()
  if executable_type == CPP:
    commands.append(CPP_FILE)
  else:
    commands.extend(["java", "-jar", JAVA_FILE])

  commands.extend(args)
  if f is not None:
      commands.extend(['-i', f])
  if irf is not None:
      commands.extend(['-r', irf])
  return run_thing(commands)


def upload_file(file_name):
    object_name = str(uuid.uuid1())
    bucket = "compilers-h1"

    try:
        s3_client = boto3.client('s3')
        s3_client.upload_file(file_name, bucket, object_name)
        location = 'us-east-2'
        return "https://s3-%s.amazonaws.com/%s/%s" % (location, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return "Could not upload image"


def generate_image_gv(file_name):
    image_f = f"{file_name}.png"
    _stdout, _stderr, ret = run_thing(["dot", "-Tpng", "-o", image_f, file_name])
    if ret != 0:
        return ret, ''
    return ret, image_f


def add_result(score, max_score, name, number, output):
  tests.append({
            "score": score,
            "max_score": max_score,
            "name": name,
            "number": number,
            "output": output,
            "visibility": "visible",
        })

def executor(files, checker, title, chapter, max_score, args, is_test, append_path, overrides=None, save_err=None, ir_files=None, skip_print=None):
    counter = 1
    for i, f_name in enumerate(files):
        message, success = '', False
        try:
            if ir_files is not None:
                ir_f = ir_files[i]
            else:
                ir_f = None

            stdout, stderr, retcode = execute(args, append_path + f_name + ".tiger", ir_f)
            if save_err:
                with open(f"../results/{f_name}.err", "w") as f:
                    f.write(stderr.decode("utf-8"))
            if is_test:
                message, success = checker(f_name, stdout, stderr, retcode, append_path)
        except Exception as e:
            message = {"message": str(e)}

        my_max_score = overrides[f_name] if overrides is not None and f_name in overrides else max_score
        if is_test and not skip_print:
            dump = json.dumps({
                           "stdout": stdout.decode("utf-8"),
                           "stderr": stderr.decode("utf-8"),
                           "retcode": retcode,
                           **message
                       },
                       indent=4, sort_keys=True)

            if 'only_message' in message:
                dump = message['only_message']

            add_result(my_max_score * int(success),
                       my_max_score,
                       f"{title}: {f_name}",
                       f"{chapter}.{counter}",
                       dump
                       )

        counter += 1

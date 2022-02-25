import json
from helper import execute, executor, add_result, check_files, print_output
from os.path import exists

BAD_TESTS = ["bad_scan", "bad_parse1", "bad_parse2", "bad_parse3"];
LEXER_TESTS = ["basic", "math1", "math2", "fib", "sort"]
PARSER_TESTS = ["basic", "math1", "math2", "fib", "sort"]


def check_error_code_1():
  _, _, exit_code1 = execute(["-i", "giviko"], None)
  _, _, exit_code2 = execute(["-z", "giviko"], None)
  _, _, exit_code3 = execute(["-i"], None)

  max_score = 3
  current_score = max_score if exit_code3 == exit_code2 and exit_code2 == exit_code1 and exit_code1 == 1 else 0

  add_result(current_score, max_score, "Check invalid commands", "1.1", "")


def check_bad_test(f, _stdout, _stderr, retcode, _append_path):
  expected_ret_code = 3 if f.find("parse") != -1 else 2
  if retcode == expected_ret_code:
    return "Good Job", True

  return f"Incorrect return code, expected {expected_ret_code} got {retcode}", False


def check_lexer_test(f, stdout, stderr, retcode, append_path):
  if retcode != 0:
    return f"Incorrect return code, expected 0 got {retcode}", False

  expected_lines = open(append_path.replace('source', 'answers') + f + ".tokens").read().split('\n')
  cur_lines = open(append_path + f + ".tokens").read().split('\n')

  if len(expected_lines) != len(cur_lines):
    return f"Expected {expected_lines} tokens, got {cur_lines}", False

  line = 0
  for expected, cur in zip(expected_lines, cur_lines):
    expected = "".join(expected.split())
    cur = "".join(cur.split())

    if expected != cur:
      return f"At line {line}, expected token {expected}, got {cur}", False

    line += 1

  return "Good job", True


def check_parser_test(f, stdout, stderr, retcode, append_path):
  from os.path import exists

  if retcode != 0:
    return f"Incorrect return code, expected 0 got {retcode}", False

  if not exists(append_path + f + ".gv"):
    return f"Can not find file {f}", False

  return "Found file, it will be manually graded", True


def test_hw1(is_test):
  check_error_code_1()
  executor(BAD_TESTS, check_bad_test, "Bad", "2", 3, [], is_test, "source/1/")
  executor(LEXER_TESTS, check_lexer_test, "Lexer", "3", 2, ["-l"], is_test, "source/1/")
  executor(PARSER_TESTS, check_parser_test, "Parser Manually Graded", "4", 0, ["-l", "-p"], is_test, "source/1/")

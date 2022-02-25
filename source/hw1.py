import json
from helper import execute, executor, add_result, check_files, print_output


BAD_TESTS = ["bad_scan", "bad_parse1", "bad_parse2", "bad_parse3"];
LEXER_TESTS = ["basic", "math1", "math2", "fib", "sort"]
PARSER_TESTS = ["basic", "math1", "math2", "fib", "sort"]


def check_error_code_1():
  _, _, exit_code1 = execute(["-i", "giviko"])
  _, _, exit_code2 = execute(["-z", "giviko"])
  _, _, exit_code3 = execute(["-i"])

  max_score = 3
  current_score = max_score if exit_code3 == exit_code2 and exit_code2 == exit_code1 and exit_code1 == 1 else 0

  add_result(current_score, max_score, "Check invalid commands", "1.1", "")


def check_bad_test(f, stdout, stderr, retcode):
  if retcode == 1:
    return ("Good Job", True)

  return ("Incorrected return code, expected 1 got " + retcode, False)


def check_lexer_test(f, stdout, stderr, retcode):
  if retcode != 0:
    return ("Incorrected return code, expected 0 got " + retcode, False)

  raise "Need to implement"


def check_parser_test(f, stdout, stderr, retcode):
  if retcode != 0:
    return ("Incorrected return code, expected 0 got " + retcode, False)

  raise "Need to implement"


def test_hw1(is_test):
  executor(BAD_TESTS, check_bad_test, "Bad", "2", 3, [], is_test)
  executor(LEXER_TESTS, check_lexer_test, "Lexer", "3", 2, ["-l"], is_test)
  executor(BAD_TESTS, check_bad_test, "Parser Manually Graded", "4", 0, ["-l", "-p"], is_test)

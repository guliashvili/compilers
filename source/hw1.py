import json
from helper import execute, executor, add_result, check_files, print_output, generate_image_gv, upload_file
from os.path import exists
import uuid

BAD_TESTS = ["bad_scan", "bad_parse1", "bad_parse2", "bad_parse3"];
LEXER_TESTS = ["basic", "math1", "math2", "fib", "sort"]
PARSER_TESTS = ["basic", "math1", "math2", "fib", "sort"]


def check_error_code_1():
    _, _, exit_code1 = execute(["-i", "giviko"], None)
    _, _, exit_code2 = execute(["-z", "giviko"], None)
    _, _, exit_code3 = execute(["-i"], None)

    max_score = 3
    if exit_code3 == exit_code2 and exit_code2 == exit_code1 and exit_code1 == 1:
        current_score = max_score
        out = f'Expected error code 1, but got {exit_code1}, {exit_code2}, {exit_code3}'
    else:
        current_score = 0
        out = "Good job"

    add_result(current_score, max_score, "Check invalid commands", "1.1", out)


def check_bad_test(f, _stdout, _stderr, retcode, _append_path):
    expected_ret_code = 3 if f.find("parse") != -1 else 2
    if retcode == expected_ret_code:
        return {"message": "Good Job"}, True

    return {"message": f"Incorrect return code, expected {expected_ret_code} got {retcode}"}, False


def check_lexer_test(f, stdout, stderr, retcode, append_path):
    if retcode != 0:
        return {"message": f"Incorrect return code, expected 0 got {retcode}"}, False

    expected_lines = open(append_path.replace('source', 'answers') + f + ".tokens").read().split('\n')
    cur_lines = open(append_path + f + ".tokens").read().split('\n')

    if len(expected_lines) != len(cur_lines):
        return {"message": f"Expected {expected_lines} tokens, got {cur_lines}"}, False

    line = 0
    for expected, cur in zip(expected_lines, cur_lines):
        expected = "".join(expected.split())
        cur = "".join(cur.split())

        if expected != cur:
            return {"message": f"At line {line}, expected token {expected}, got {cur}"}, False

        line += 1

    return {"message": "Good job"}, True


def check_parser_test(f, stdout, stderr, retcode, append_path):
    from os.path import exists

    if retcode != 0:
        return {"message": f"Incorrect return code, expected 0 got {retcode}"}, False

    gv_f = append_path + f + ".gv"
    if not exists(gv_f):
        return {"message": f"Can not find file {f}"}, False

    ret, img_f = generate_image_gv(gv_f)
    if ret != 0:
        return {"message": f"Can not generate image of {gv_f}"}, False

    url = upload_file(img_f)

    return {"message": "Found file, it will be manually graded", "url": url}, True


def test_hw1(is_test):
    check_error_code_1()
    executor(BAD_TESTS, check_bad_test, "Bad", "2", 3, [], is_test, "source/1/")
    executor(LEXER_TESTS, check_lexer_test, "Lexer", "3", 2, ["-l"], is_test, "source/1/")
    executor(PARSER_TESTS, check_parser_test, "Parser Manually Graded", "4", 0, ["-l", "-p"], is_test, "source/1/")

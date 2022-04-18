import json
import os.path

from helper import execute, executor, add_result, check_files, print_output, generate_image_gv, upload_file, run_thing
from os.path import exists
import uuid

# ls -l1 | sort -n |  awk '{print "\""$0"\","}' | tr -d "\n"
SEMANTIC_TESTS = ["1_err_undefined_var", "2_err_undefined_type", "3_err_undefined_function",
                  "4_err_redefine_var", "5_err_redefine_type", "6_err_redefine_func",
                  "7_err_storage_class_global_var", "8_err_storage_class_local_static",
                  "9_err_assign_array_size", "10_err_assign_array_type",
                  "11_err_assign_narrowing_return", "12_err_assign_narrowing",
                  "13_err_power_op_float", "14_err_relational_associate", "15_err_relational_mixed",
                  "16_err_conditional_array", "17_err_conditional_float", "18_err_break_outside_loop",
                  "19_err_for_exp_array", "20_err_for_exp_float", "21_err_while_expr_array",
                  "22_err_while_expr_float", "23_err_func_call_narrowing",
                  "24_err_func_call_array_arg", "25_err_func_call_too_few_args",
                  "26_err_func_call_too_many_args", "27_err_func_no_return",
                  "28_err_func_return_array", "29_err_func_return_narrowing",
                  "30_err_func_return_proc", "31_err_func_return_void", "32_err_array_add",
                  "33_err_array_index_array", "34_err_array_index_float", "35_err_array_without_type"]

IR_TESTS = ["array_assign", "array_basic_ops", "array_basic_ops_static", "array_combo_ops",
            "basic_break_stmt", "basic_conditional", "basic_conditional_nested_if",
            "basic_conditional_nested_if_else", "basic_int_assign", "basic_logical_ops",
            "basic_logical_relational_mixed", "basic_loop_forloop", "basic_loop_whileloop",
            "basic_math", "basic_math_combo", "basic_math_power_op", "basic_relational_ops",
            "basic_scope_global", "basic_scope_hiding", "basic_scope_nested", "basic_type",
            "basic_type_of_type", "benchmark1", "benchmark2", "demo_jacobi",
            "demo_matrix", "demo_motor", "demo_priority_queue", "demo_prng",
            "demo_selection_sort", "demo_slope", "demo_square_root", "float_assign",
            "float_math", "float_math_combo", "float_math_mixed", "float_math_power_op",
            "function_call_1_arg", "function_call_4_arg", "function_call_8_arg",
            "function_call_chain", "function_call_void_ret", "function_global_scope",
            "function_recursive_6_arg", "function_recursive_factorial", "function_recursive_fib",
            "lib_call_exit", "lib_call_not", "lib_call_printf", "lib_call_printi"]

ST_TESTS = ["demo_slope", "demo_square_root", "basic_scope_global", "basic_scope_hiding",
            "demo_jacobi"]


def check_files_hw2():
    max_score = .5
    report = exists('../submission/phase2_design.pdf')
    executables = check_files()

    if not report:
        score = 0
        out = "No report found"
    elif executables:
        score = 0
        out = "No executable or grammar found"
    else:
        score = max_score
        out = "Good job"

    add_result(score, max_score, "Check submitted files", "1.1", out)


def check_semantic_test(f, _stdout, stderr, retcode, append_path):
    if retcode != 4:
        return {"message": f"Incorrect return code, expected 4 got {retcode}"}, False

    expected_lines = open(append_path.replace('source', 'answers') + f + ".err").read().split('\n')
    cur_lines = stderr.decode("utf-8").split('\n')

    def flt(ln):
        idx = ln.find(':')
        if idx == -1:
            return None
        return ln[:idx]

    expected_lines = list(sorted(list(filter(None, list(map(flt, expected_lines))))))
    cur_lines = list(sorted(list(filter(None, list(map(flt, cur_lines))))))

    for line in range(max(len(cur_lines), len(expected_lines))):
        if line >= len(expected_lines):
            return {"message": f"There are less errors expected than found, last error that was not expected is {cur_lines[line]}"}, False
        elif line >= len(cur_lines):
            return {"message": f"There are more errors expected than found, last error that was expected is {expected_lines[line]}"}, False

        expected, cur = expected_lines[line], cur_lines[line]
        if expected != cur:
            return {"message": f"In sorted list of errors, next error was expected {expected}..., but got {cur}..."}, False

    return {"message": "Good job"}, True


def check_ir_test(f, _stdout, _stderr, retcode, append_path):
    if retcode != 0:
        return {"message": f"Incorrect return code, expected 0 got {retcode}"}, False

    ret = run_thing(['java', '-jar', os.path.join(append_path, 'tigerc-ir.jar'), '-r', os.path.join(append_path, f'{f}.ir')])
    ret = ret[0].decode("utf-8")
    # if is test
    # with open(os.path.join(append_path.replace('source', 'answers'), f"{f}.ir_answer"), "w") as fff:
    #     fff.write(ret)
    with open(os.path.join(append_path.replace('source', 'answers'), f"{f}.ir_answer"), "r") as fff:
        content = fff.read().split('\n')

    if ret == content:
        return {"message": f"IR produces incorrect output, expected {content} got {ret}"}, False

    return {"message": "Good job"}, True


def check_st_test(f, _stdout, _stderr, retcode, append_path):
    if retcode != 0:
        return {"message": f"Incorrect return code, expected 0 got {retcode}"}, False

    with open(os.path.join(append_path, f"{f}.st"), "r") as fff:
        content = fff.read().strip()

    if len(content) == 0:
        return {"message": f"No content found return code, expected something"}, False

    return {"only_message": content}, True



def test_hw2(is_test):
    check_files_hw2()
    executor(SEMANTIC_TESTS, check_semantic_test, "Semantic Test", "2", 1, [], is_test, "source/2/semantic_tests_v2/", {t: .5 for t in SEMANTIC_TESTS[:1]}, not is_test)
    executor(IR_TESTS, check_ir_test, "IR Test", "3", 1, ["--ir"], is_test, "source/2/tiger_tests_v3/", {t: .5 for t in IR_TESTS[:10]})
    executor(ST_TESTS, check_st_test, "Symbol Table Manually Graded Test", "4", 0, ["--st"], is_test, "source/2/tiger_tests_v3/")

    # check_error_code_1()
    # executor(BAD_TESTS, check_bad_test, "Bad", "2", 3, [], is_test, "source/1/")
    # executor(LEXER_TESTS, check_lexer_test, "Lexer", "3", 2, ["-l"], is_test, "source/1/")
    # executor(PARSER_TESTS, check_parser_test, "Parser Manually Graded", "4", 0, ["-l", "-p"], is_test, "source/1/")

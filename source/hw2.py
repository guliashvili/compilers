import json
from helper import execute, executor, add_result, check_files, print_output, generate_image_gv, upload_file
from os.path import exists
import uuid

# BAD_TESTS = ["bad_scan", "bad_parse1", "bad_parse2", "bad_parse3"];
# LEXER_TESTS = ["basic", "math1", "math2", "fib", "sort"]
# PARSER_TESTS = ["basic", "math1", "math2", "fib", "sort"]


# def check_error_code_1():
#   _, _, exit_code1 = execute(["-i", "giviko"], None)
#   _, _, exit_code2 = execute(["-z", "giviko"], None)
#   _, _, exit_code3 = execute(["-i"], None)
#
#   max_score = 3
#   current_score = max_score if exit_code3 == exit_code2 and exit_code2 == exit_code1 and exit_code1 == 1 else 0
#
#   add_result(current_score, max_score, "Check invalid commands", "1.1", "")
#
#
# def check_bad_test(f, _stdout, _stderr, retcode, _append_path):
#   expected_ret_code = 3 if f.find("parse") != -1 else 2
#   if retcode == expected_ret_code:
#     return {"message": "Good Job"}, True
#
#   return {"message": f"Incorrect return code, expected {expected_ret_code} got {retcode}"}, False
#
#
# def check_lexer_test(f, stdout, stderr, retcode, append_path):
#   if retcode != 0:
#     return {"message": f"Incorrect return code, expected 0 got {retcode}"}, False
#
#   expected_lines = open(append_path.replace('source', 'answers') + f + ".tokens").read().split('\n')
#   cur_lines = open(append_path + f + ".tokens").read().split('\n')
#
#   if len(expected_lines) != len(cur_lines):
#     return {"message": f"Expected {expected_lines} tokens, got {cur_lines}"}, False
#
#   line = 0
#   for expected, cur in zip(expected_lines, cur_lines):
#     expected = "".join(expected.split())
#     cur = "".join(cur.split())
#
#     if expected != cur:
#       return {"message": f"At line {line}, expected token {expected}, got {cur}"}, False
#
#     line += 1
#
#   return {"message": "Good job"}, True
#
#
# def check_parser_test(f, stdout, stderr, retcode, append_path):
#   from os.path import exists
#
#   if retcode != 0:
#     return {"message": f"Incorrect return code, expected 0 got {retcode}"}, False
#
#   gv_f = append_path + f + ".gv"
#   if not exists(gv_f):
#     return {"message": f"Can not find file {f}"}, False
#
#   ret, img_f = generate_image_gv(gv_f)
#   if ret != 0:
#     return {"message": f"Can not generate image of {gv_f}"}, False
#
#   url = upload_file(img_f)
#
#
#   return {"message": "Found file, it will be manually graded", "url": url}, True

# ls -l1 | sort -n |  awk '{print "\""$0"\","}' | tr -d "\n"
SEMANTIC_TESTS = ["1_err_undefined_var.tiger", "2_err_undefined_type.tiger", "3_err_undefined_function.tiger",
                  "4_err_redefine_var.tiger", "5_err_redefine_type.tiger", "6_err_redefine_func.tiger",
                  "7_err_storage_class_global_var.tiger", "8_err_storage_class_local_static.tiger",
                  "9_err_assign_array_size.tiger", "10_err_assign_array_type.tiger",
                  "11_err_assign_narrowing_return.tiger", "12_err_assign_narrowing.tiger",
                  "13_err_power_op_float.tiger", "14_err_relational_associate.tiger", "15_err_relational_mixed.tiger",
                  "16_err_conditional_array.tiger", "17_err_conditional_float.tiger", "18_err_break_outside_loop.tiger",
                  "19_err_for_exp_array.tiger", "20_err_for_exp_float.tiger", "21_err_while_expr_array.tiger",
                  "22_err_while_expr_float.tiger", "23_err_func_call_narrowing.tiger",
                  "24_err_func_call_array_arg.tiger", "25_err_func_call_too_few_args.tiger",
                  "26_err_func_call_too_many_args.tiger", "27_err_func_no_return.tiger",
                  "28_err_func_return_array.tiger", "29_err_func_return_narrowing.tiger",
                  "30_err_func_return_proc.tiger", "31_err_func_return_void.tiger", "32_err_array_add.tiger",
                  "33_err_array_index_array.tiger", "34_err_array_index_float.tiger", "35_err_array_without_type.tiger"]
IR_TESTS = ["array_assign.tiger", "array_basic_ops.tiger", "array_basic_ops_static.tiger", "array_combo_ops.tiger",
            "basic_break_stmt.tiger", "basic_conditional.tiger", "basic_conditional_nested_if.tiger",
            "basic_conditional_nested_if_else.tiger", "basic_int_assign.tiger", "basic_logical_ops.tiger",
            "basic_logical_relational_mixed.tiger", "basic_loop_forloop.tiger", "basic_loop_whileloop.tiger",
            "basic_math.tiger", "basic_math_combo.tiger", "basic_math_power_op.tiger", "basic_relational_ops.tiger",
            "basic_scope_global.tiger", "basic_scope_hiding.tiger", "basic_scope_nested.tiger", "basic_type.tiger",
            "basic_type_of_type.tiger", "benchmark1.tiger", "benchmark2.tiger", "demo_jacobi.tiger",
            "demo_matrix.tiger", "demo_motor.tiger", "demo_priority_queue.tiger", "demo_prng.tiger",
            "demo_selection_sort.tiger", "demo_slope.tiger", "demo_square_root.tiger", "float_assign.tiger",
            "float_math.tiger", "float_math_combo.tiger", "float_math_mixed.tiger", "float_math_power_op.tiger",
            "function_call_1_arg.tiger", "function_call_4_arg.tiger", "function_call_8_arg.tiger",
            "function_call_chain.tiger", "function_call_void_ret.tiger", "function_global_scope.tiger",
            "function_recursive_6_arg.tiger", "function_recursive_factorial.tiger", "function_recursive_fib.tiger",
            "lib_call_exit.tiger", "lib_call_not.tiger", "lib_call_printf.tiger", "lib_call_printi.tiger"]
ST_TESTS = ["demo_slope.tiger", "demo_square_root.tiger", "basic_scope_global.tiger", "basic_scope_hiding.tiger",
            "demo_jacobi.tiger"]


def check_files_hw2():
    max_score = .5
    report = exists('submission/phase2_design.pdf')
    executables = check_files()

    if not report:
        score = 0
        out = "No report found"
    elif not executables:
        score = 0
        out = "No executable or grammar found"
    else:
        score = max_score
        out = "Good job"

    add_result(score, max_score, "Check submitted files", "1.1", out)


def check_semantic_test():
    pass


def check_ir_test():
    pass


def check_st_test():
    pass


def test_hw2(is_test):
    check_files_hw2()
    executor(SEMANTIC_TESTS, check_semantic_test, "Semantic Test", "2", 1, [], is_test, "source/2/")
    executor(IR_TESTS, check_ir_test, "IR Test", "3", [], 1, is_test, "source/2/", {t: .5 for t in IR_TESTS[:2]})
    executor(ST_TESTS, check_st_test, "Symbol Table Test", "2", 0, [], is_test, "source/2/")

    # check_error_code_1()
    # executor(BAD_TESTS, check_bad_test, "Bad", "2", 3, [], is_test, "source/1/")
    # executor(LEXER_TESTS, check_lexer_test, "Lexer", "3", 2, ["-l"], is_test, "source/1/")
    # executor(PARSER_TESTS, check_parser_test, "Parser Manually Graded", "4", 0, ["-l", "-p"], is_test, "source/1/")

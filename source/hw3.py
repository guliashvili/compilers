import os.path

from helper import executor, add_result, check_files, run_thing
from os.path import exists

# ls -l1 | sort -n |  awk '{print "\""$0"\","}' | tr -d "\n"
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

CFG_TESTS = ["demo_selection_sort", "demo_motor"]

LIVENESS_TESTS = ["demo_selection_sort", "demo_motor", ]

ALLOCATION_TESTS = ["benchmark1", "benchmark2", "demo_selection_sort", "demo_motor", "demo_priority_queue", "demo_tak"]

def check_files_hw3():
    max_score = .1
    fs = ['phase3_analysis.pdf', 'phase3_design.pdf']
    for f in fs:
        report = exists(f'../submission/{f}')
        executables = check_files()

        if not report:
            score = 0
            out = f"No report file {f} found"
            break
        elif executables:
            score = 0
            out = "No executable or grammar found"
            break
        else:
            score = max_score
            out = "Good job"

    add_result(score, max_score, "Check submitted files", "1.1", out)


def check_naive_test(f, _stdout, _stderr, retcode, append_path):
    if retcode != 0:
        return {"message": f"Incorrect return code, expected 0 got {retcode}"}, False

    ret = run_thing(['spim', '-file', os.path.join(append_path, f'{f}.s')])
    ret = ret[0].decode("utf-8")
    ret = '\n'.join(ret.split('\n')[1:])
    # if is test
    # with open(os.path.join(append_path.replace('source', 'answers'), f"{f}.native_answer"), "w") as fff:
    #     fff.write(ret)
    with open(os.path.join(append_path.replace('source', 'answers'), f"{f}.native_answer"), "r") as fff:
        content = fff.read().split('\n')

    if ret == content:
        return {"message": f"MIPS produces incorrect output, expected {content} got {ret}"}, False

    return {"message": "Good job"}, True





def test_hw3(is_test):
    check_files_hw3()
    ir_files = map(lambda f: f'source/3/ir/{f}.ir' , IR_TESTS)
    executor(IR_TESTS, check_naive_test, "Naive Test", "2", 1, ["-n", "--mips"], is_test, "source/3/tiger/", {t: .9 for t in IR_TESTS[:1]}, ir_files)
    # executor(ST_TESTS, check_st_test, "Symbol Table Manually Graded Test", "4", 0, ["--st"], is_test, "source/2/tiger_tests_v3/")


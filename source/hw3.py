import os.path
import collections
from helper import executor, add_result, check_files, run_thing, generate_image_gv, upload_file
from os.path import exists
from functools import partial

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


def check_cfg_test(f, _stdout, _stderr, retcode, append_path):
    if retcode != 0:
        return {"message": f"Incorrect return code, expected 0 got {retcode}"}, False
    f += '.cfg.gv'
    gv_f = append_path + f
    if not exists(gv_f):
        return {"message": f"Can not find file {f}"}, False

    ret, img_f = generate_image_gv(gv_f)
    if ret != 0:
        return {"message": f"Can not generate image of {gv_f}"}, False

    url = upload_file(img_f)

    return {"message": "Found file, it will be manually graded", "url": url}, True



def check_liveness_test(f, _stdout, _stderr, retcode, append_path):
    if retcode != 0:
        return {"message": f"Incorrect return code, expected 0 got {retcode}"}, False

    with open(os.path.join(append_path, f"{f}.liveness"), "r") as fff:
        content = fff.read().strip()

    if len(content) == 0:
        return {"message": f"No content found return code, expected something"}, False

    return {"only_message": content}, True


def extract_needed_tests(needed_tests, to_extract):
    return list(filter(lambda x: any(map(lambda needed_name: needed_name in x, needed_tests)) , to_extract))


save = collections.defaultdict(str)
NAIVE = 'naive'
IB = 'ib'
BRIGGS = 'briggs'

def check_benchmark(asm_type, f, _stdout, _stderr, retcode, append_path):
    if retcode != 0:
        return {"message": f"Incorrect return code, expected 0 got {retcode}"}, False

    ret = run_thing(['spim', '-file', os.path.join(append_path, f'{f}.{asm_type}.s')])
    ret = ret[0].decode("utf-8")
    ret = '\n'.join(ret.split('\n')[1:])
    with open(os.path.join(append_path.replace('source', 'answers'), f"{f}.native_answer"), "r") as fff:
        content = fff.read().split('\n')

    correct = ret == content

    ret = run_thing(['spim', '-keepstats', '-file', os.path.join(append_path, f'{f}.{asm_type}.s')])
    ret = ret[0].decode("utf-8")
    ret = '\n'.join(ret.split('\n')[1:])[-1]

    save[f] += asm_type + ' : ' + ret + " " + 'CORRECT Program' if correct else 'INCORRECT Program, CHECK IT' + '\n'

    return {"only_message": save[f]}, True


def test_hw3(is_test):
    check_files_hw3()
    ir_files = map(lambda f: f'source/3/ir/{f}.ir', IR_TESTS)
    executor(IR_TESTS, check_naive_test, "Naive Test", "2", 1, ["-n", "--mips"], is_test, "source/3/tiger/", {t: .9 for t in IR_TESTS[:1]}, ir_files)

    CFG_LIVENESS_TESTS = ('demo_selection_sort', 'demo_motor')
    cfg_liveness_code_files = extract_needed_tests(CFG_LIVENESS_TESTS, IR_TESTS)
    cfg_liveness_ir_files = extract_needed_tests(CFG_LIVENESS_TESTS, ir_files)

    executor(cfg_liveness_code_files, check_cfg_test, "CFG Test", "3", 0, ["-b", "--cfg"], is_test, "source/3/tiger/", None, cfg_liveness_ir_files)
    executor(cfg_liveness_code_files, check_liveness_test, "Liveness Test", "4", 0, ["-g", "--liveness"], is_test, "source/3/tiger/", None, cfg_liveness_ir_files)

    BENCHMARK_TESTS = ('benchmark1', 'benchmark2', 'demo_selection_sort', 'demo_motor', 'demo_priority_queue')
    benchmark_code_files = extract_needed_tests(BENCHMARK_TESTS, IR_TESTS)
    benchmark_ir_files = extract_needed_tests(BENCHMARK_TESTS, ir_files)

    executor(benchmark_code_files,  partial(check_benchmark, NAIVE), "", "4", 0, ["-n", "--mips"], False,
             "source/3/tiger/", None, benchmark_ir_files)
    executor(benchmark_code_files, partial(check_benchmark, IB), "", "4", 0, ["-b", "--mips"], False,
             "source/3/tiger/", None, benchmark_ir_files)
    executor(benchmark_code_files, partial(check_benchmark, BRIGGS), "Benchmark Test", "4", 0, ["-g", "--mips"], True,
         "source/3/tiger/", None, benchmark_ir_files)

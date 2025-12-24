from functions.run_python_file import run_python_file

def test_run_python_file(working_dir, target_file, args=None):
    res = run_python_file(working_dir, target_file, args)

    print(res)

    print("")

test_run_python_file("calculator", "main.py")

test_run_python_file("calculator", "main.py", ["3 + 5"])

test_run_python_file("calculator", "tests.py")

test_run_python_file("calculator", "../main.py")

test_run_python_file("calculator", "nonexistent.py")

test_run_python_file("calculator", "lorem.txt")

from functions.get_file_content import get_file_content

def test_get_file_content(working_dir, target_file):
    res = get_file_content(working_dir, target_file)
    res_chars = len(res)

    if res.startswith("Error: "):
        print(res)
    else:
        print(f"[Number of chars: {res_chars}]\n")

        if res.endswith(" characters]"):
            print("[text has been truncated]")
        else:
            print(res)

    print("")

test_get_file_content("calculator", "main.py")

test_get_file_content("calculator", "lorem.txt")

test_get_file_content("calculator", "pkg/calculator.py")

test_get_file_content("calculator", "/bin/cat")

test_get_file_content("calculator", "pkg/does_not_exist.py")

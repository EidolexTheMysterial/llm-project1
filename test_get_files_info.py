from functions.get_files_info import get_files_info

def test_get_files_info(working_dir, target_dir):
    res = get_files_info(working_dir, target_dir)

    print(res)

test_get_files_info("calculator", ".")

test_get_files_info("calculator", "pkg")

test_get_files_info("calculator", "/bin")

test_get_files_info("calculator", "../")

# test_get_files_info("test", ".")

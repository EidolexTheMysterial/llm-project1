from functions.write_file import write_file

def test_write_file(working_dir, target_file, content):
    res = write_file(working_dir, target_file, content)

    print(res)

    print("")

test_write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")

test_write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")

test_write_file("calculator", "/tmp/temp.txt", "this should not be allowed")

test_write_file("calculator", "pkg", "this should fail")

import os

from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write the specified contents to the specified file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to file to write contents to",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write to the file",
            ),
        },
    ),
)

def write_file(working_directory, file_path, content):
    str = ""

    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

        # print(f"[target_file: {target_file}]")
        # print(f"[target_file os.path.dirname: {os.path.dirname(target_file)}]")

        # Will be True or False
        valid_target_dir = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs

        if valid_target_dir is False:
            str += f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        elif os.path.isdir(target_file):
            str += f'Error: Cannot write to "{file_path}" as it is a directory'
        else:
            # ensure all dirs exist
            os.makedirs(os.path.dirname(target_file), exist_ok=True)

            with open(target_file, "w") as f:
                f.write(content)
                f.close()

            str += f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

        return str
    except Exception as e:
        return f'Error: Exception occurred - {e}'

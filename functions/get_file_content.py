import os

from google.genai import types

from constants import *

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Returns the text contents of the specified file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to file to have its contents read",
            ),
        },
    ),
)

def get_file_content(working_directory, file_path):
    contents = ""

    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

        print(f"\n[attempting to retrieve the contents of: {target_file}]\n")

        # Will be True or False
        valid_target_dir = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs

        # print(f"[working_dir_abs: {working_dir_abs}]")
        # print(f"[target_file: {target_file}]")

        # print(f"[valid_target_dir: {valid_target_dir}]")

        if valid_target_dir is False:
            contents += f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        elif not os.path.isfile(target_file):
            contents += f'Error: File not found or is not a regular file: "{file_path}"'
        else:
            with open(target_file) as f:
                contents += f.read(MAX_CHARS)

                # After reading the first MAX_CHARS...
                if f.read(1):
                    contents += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

        return contents
    except Exception as e:
        return f'Error: Exception occurred - {e}'

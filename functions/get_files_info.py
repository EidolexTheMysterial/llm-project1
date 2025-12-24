import os

from google.genai import types

default_dir = "."

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)

def get_files_info(working_directory, directory=default_dir):
    str = "Result for "

    str += "current" if directory == default_dir else f"'{directory}'"

    str += " directory:\n"

    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

        # Will be True or False
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

        if valid_target_dir is False:
            str += f'\tError: Cannot list "{directory}" as it is outside the permitted working directory\n'
        elif not os.path.isdir(target_dir):
            str += f'\tError: "{directory}" is not a directory\n'
        else:
            for itm in os.listdir(target_dir):
                itm_path = os.path.join(target_dir, itm)
                is_dir = os.path.isdir(itm_path)
                sz = os.path.getsize(itm_path)

                str+= f"\t- {itm}: file_size={sz} bytes, is_dir={is_dir}\n"

        str += "\n"

        return str
    except Exception as e:
        return f'Error: Exception occurred - {e}'

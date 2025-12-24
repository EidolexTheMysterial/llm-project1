import os
import subprocess

from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run the specified Python script (files ending in .py) and retrieve the results",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python script to be run",
            ),
        },
    ),
)

def run_python_file(working_directory, file_path, args=None):
    str = ""

    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

        # print(f"[target_file: {target_file}]")
        # print(f"[target_file os.path.dirname: {os.path.dirname(target_file)}]")

        # Will be True or False
        valid_target_dir = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs

        if valid_target_dir is False:
            str += f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        elif not os.path.isfile(target_file):
            str += f'Error: "{file_path}" does not exist or is not a regular file'
        elif not file_path.endswith(".py"):
            str += f'Error: "{file_path}" is not a Python file'
        else:
            fout, ferr = None, None
            command = ["python", target_file]

            if args:
                command.extend(args)

            # print(f"--command: {command}")

            proc = subprocess.run(
                command,
                capture_output=True,
                cwd=working_dir_abs,
                text=True,
                timeout=30,
            )

            fout, ferr = proc.stdout, proc.stderr

            # print(f"\n--STDOUT: {fout}")
            # print(f"--STDERR: {ferr}")

            if proc.returncode != 0:
                str += f"\n[ Process exited with code {proc.returncode} ]\n\n"

            if not fout and not ferr:
                str += "\n[ No output produced ]\n\n"
            else:
                if fout:
                    str += f"[ STDOUT: {fout} ]"

                if ferr :
                    str += f"[ STDERR: {ferr} ]"

        return str
    except Exception as e:
        return f"Error: executing Python file: {e}"

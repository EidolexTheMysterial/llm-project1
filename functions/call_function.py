from google.genai import types

from functions.get_files_info import *
from functions.get_file_content import *
from functions.write_file import *
from functions.run_python_file import *

from constants import *

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file,
    ],
)

fn_map = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "write_file": write_file,
    "run_python_file": run_python_file
}

def call_function(function_call, verbose=False):
    fn_name = function_call.name or ""
    fn_args = dict(function_call.args) if function_call.args else {}

    if verbose:
        print(f"Calling function: {fn_name}({fn_args})")
    else:
        print(f" - Calling function: {fn_name}")

    if fn_map[fn_name]:
        fn = fn_map[fn_name]

        fn_call_args = { "working_directory": AI_WORKING_DIR }

        if fn_args:
            fn_call_args.update(fn_args)

        res = fn(**fn_call_args)

        # print(f"[res: {res}]")

        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=fn_name,
                    response={"result": res},
                )
            ],
        )
    else:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=fn_name,
                    response={"error": f"Unknown function: {fn_name}"},
                )
            ],
        )

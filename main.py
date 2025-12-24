import os
import argparse

from dotenv import load_dotenv
from google import genai
from google.genai import types

from constants import *
from prompts import *

from functions.call_function import *

def main():
    response = None

    # default contents
    contents = '"Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."'

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    # Now we can access `args.user_prompt`

    print("[Hello from llm-project1!]")

    contents = args.user_prompt
    print(f"\n[User Prompt: {contents}]")

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    if api_key is None:
        raise RuntimeError("[GEMINI_API_KEY] was not found")

    print(f"\n\nAPI Key found: {api_key}")

    print("\nCreating Gemini client:")
    client = genai.Client(api_key=api_key)

    if args.verbose:
        print(f"\n\n[User prompt: {contents}]")

    i, should_continue = 0, True

    while should_continue and i < MAX_CALLS:
        # print(f"\n[call #{i}]\n")

        try:
            response = client.models.generate_content(
                model=AI_MODEL,
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions],
                    system_instruction=system_prompt,
                ),
            )
        except Exception as e:
            raise RuntimeError(f"Failure on calling 'generate_content' - {e}")

        if response.usage_metadata is None:
            raise RuntimeError("API called failed")
        elif args.verbose:
            prompt_count = response.usage_metadata.prompt_token_count
            candidates_count = response.usage_metadata.candidates_token_count

            print(f"Prompt tokens: {prompt_count}")
            print(f"Response tokens: {candidates_count}")

        fns = response.function_calls

        res_lst = []

        if fns:
            for function_call in fns:
                # fn_name = function_call.name
                # fn_args = function_call.args

                # print(f"Calling function: {fn_name}({fn_args})")

                res = call_function(function_call, args.verbose)

                if res.parts:
                    res_part0 = res.parts[0]

                    if not res_part0.function_response:
                        raise RuntimeError("Invalid response - missing 'parts.function_response'")
                    elif not res_part0.function_response.response:
                        raise RuntimeError("Invalid response - missing 'parts.function_response.response'")

                    res_lst.append(res_part0)

                    if args.verbose:
                        print(f"-> {res_part0.function_response.response}")
                else:
                    raise RuntimeError("Invalid response - missing '.parts'")
        else:
            print("--Response:")
            print(response.text)

        candidates = response.candidates

        if candidates:
            for cand in candidates:
                # print(f"{cand}")

                has_fn_call = False

                for part in cand.content.parts:
                    if part.function_call:
                        has_fn_call = True
                        break

                if has_fn_call:
                    messages.append(cand.content)
                elif response.text:
                    print("Final response:")
                    print(f"{response.text}\n")
                    should_continue = False
                    break
    
        msg = types.Content(role = "user", parts = res_lst)
        messages.append(msg)

        i += 1

    print("\n\n[end of run - main.py]")

if __name__ == "__main__":
    main()

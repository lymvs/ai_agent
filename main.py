import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import system_prompt
from call_function import available_functions

def main():
    load_dotenv()

    verbose = "--verbose" in sys.argv
    api_key = os.environ.get("GEMINI_API_KEY")

    args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]

    if not args:
        print("Tip:")
        print('Usage: python3 main.py "your prompt here"')
        print('Example: python3 main.py "How do I build a calculator app?"')
        sys.exit(1)

    prompt = " ".join(args)

    if verbose:
        print(f"User prompt: {prompt}\n")

    messages = [
        types.Content(
            role="user",
            parts=[types.Part(text=prompt)],
            ),
    ]

    schema_get_files_info = types.FunctionDeclaration(
        name="get_files_info",
        description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "directory": types.Schema(
                    type=types.Type.STRING,
                    description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
                ),
            },
        ),
    )

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            ],
            )

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt),
        )

    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count
    function_call_list = response.function_calls

    print(f"User prompt: {prompt}")
    print(f"Prompt tokens: {prompt_tokens}")
    print(f"Response tokens: {response_tokens}")
    print(f"Response text: {response.text}")
    if function_call_list is not None:
        for function_call_part in function_call_list:
            print(f"Calling function: {function_call_part.name}({function_call_part.args})")

if __name__ == "__main__":
    main()

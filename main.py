import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import system_prompt
from call_function import available_functions, call_function

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

    for i in range(20):
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

        if response.candidates is not None:
            for candidate in response.candidates:
                if candidate is not None:
                    messages.append(candidate.content)

        print(f"User prompt: {prompt}")
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")
        print(f"Response text: {response.text}")
        if function_call_list is not None:
            for function_call_part in function_call_list:
                # print(f"Calling function: {function_call_part.name}({function_call_part.args})")
                function_call_result = call_function(function_call_part, verbose)
                if not function_call_result.parts[0].function_response.response:
                    raise Exception("Error: Function couldn't be called")
                print(f"-> {function_call_result.parts[0].function_response.response}")
                messages.append(function_call_result)
        else:
            break

    print(response.text)

if __name__ == "__main__":
    main()

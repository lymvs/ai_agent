import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import system_prompt

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
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(system_instruction=system_prompt),
        )

    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count

    print(f"User prompt: {prompt}")
    print(f"Prompt tokens: {prompt_tokens}")
    print(f"Response tokens: {response_tokens}")
    print(f"Response text: {response.text}")

if __name__ == "__main__":
    main()

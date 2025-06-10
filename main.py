import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    args = sys.argv[1:]

    if not args:
        print("Tip:")
        print('Usage: python3 main.py "your prompt here"')
        print('Example: python3 main.py "How do I build a calculator app?"')
        sys.exit(1)

    if "--verbose" not in args:
        sys.exit(2)

    prompt = " ".join(args)

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
        )

    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count

    print(f"User prompt: {prompt}")
    print(f"Prompt tokens: {prompt_tokens}")
    print(f"Response tokens: {response_tokens}")
    print(f"Response text: {response.text}")

if __name__ == "__main__":
    main()

import os

from config import MAX_CHARS
from google.genai import types


def get_file_content(working_directory, file_path):
    abs_file_path = os.path.abspath(f"{working_directory}/{file_path}")
    abs_working_dir = os.path.abspath(working_directory)

    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(abs_file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        with open(abs_file_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
    except Exception as e:
        return f"Error: {e}"

    return file_content_string

schema_get_file_content = types.FunctionDeclarationDict(
    name="get_file_content",
    description="Read the contents of the specified file and limit the size of the file to 10000 max characters, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The directory to read the contents of the file, relative to the working directory.",
            ),
        },
    ),
)

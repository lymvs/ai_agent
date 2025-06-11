import os

from google.genai import types


def get_files_info(working_directory, directory=None):
    abs_dir = os.path.abspath(f"{working_directory}/{directory}")
    abs_working_dir = os.path.abspath(working_directory)

    if not abs_dir.startswith(abs_working_dir):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(abs_dir):
        return f'Error: "{directory}" is not a directory'

    try:
        contents = os.listdir(abs_dir)
        response = []
        for i in contents:
            path = os.path.join(abs_dir, i)
            file_size = os.path.getsize(path)
            is_dir = False if os.path.isfile(path) else True
            response.append(f"- {i}: file_size={file_size}, is_dir={is_dir}")
        return "\n".join(response)
    except Exception as e:
        return f"Error: {e}"

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
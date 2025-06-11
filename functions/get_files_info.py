import os


def get_files_info(working_directory, directory=None):
    abs_dir = os.path.abspath(f"{working_directory}/{directory}")
    abs_working_dir = os.path.abspath(working_directory)

    if not abs_dir.startswith(abs_working_dir):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(abs_dir):
        return f'Error: "{directory}" is not a directory'

    contents = os.listdir(abs_dir)
    response = []
    for i in contents:
        try:
            path = os.path.join(abs_dir, i)
            file_size = os.path.getsize(path)
            is_dir = False if os.path.isfile(path) else True
            response.append(f"- {i}: file_size={file_size}, is_dir={is_dir}")
        except Exception as e:
            return f"Error: {e}"

    return "\n".join(response)

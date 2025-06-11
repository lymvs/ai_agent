import os
import subprocess

def run_python_file(working_directory, file_path):
    abs_file_path = os.path.abspath(f"{working_directory}/{file_path}")
    abs_working_dir = os.path.abspath(working_directory)

    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(abs_file_path):
        return f'Error: File "{file_path}" not found.'
    if not abs_file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        execution = subprocess.run(
            ["python3", f"{abs_file_path}"],
            timeout=30,
            capture_output=True,
            text=True,
            )

        stdout = execution.stdout
        if stdout is None:
            return "No output produced."

        output = []
        output.append(f"STDOUT: {stdout}")

        stderr = execution.stderr
        output.append(f"STDERR: {stderr}")

        return_code = execution.returncode
        if return_code != 0:
            output.append(f"Process exited with code {return_code}")

        return "\n".join(output)
    except Exception as e:
        return f"Error: executing Python file: {e}"

import os

def paste_files_content(output_file, file_types):
    script_directory = os.path.dirname(__file__)
    with open(output_file, 'w') as output:
        for file_name in os.listdir(script_directory):
            if any(file_name.endswith(file_type) for file_type in file_types):
                with open(os.path.join(script_directory, file_name), 'r') as file:
                    file_content = file.read()
                    output.write(f"File Name: {file_name}\n")
                    output.write(f"File Content:\n{file_content}\n\n")

output_file = 'output.txt'
file_types = ['.html']

paste_files_content(output_file, file_types)

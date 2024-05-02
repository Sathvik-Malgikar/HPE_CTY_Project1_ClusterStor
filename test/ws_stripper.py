def strip_trailing_whitespace(file_path):
    # Open the file in read mode
    with open(file_path, 'r') as file:
        # Read all lines from the file
        lines = file.readlines()

    # Strip trailing whitespace from each line
    stripped_lines = [line.rstrip() + '\n' for line in lines]

    # Open the file in write mode
    with open(file_path, 'w') as file:
        # Write the modified lines back to the file
        file.writelines(stripped_lines)

import sys 

# Example usage:
file_path = sys.argv[1]  # Replace 'example.py' with the path to your Python file
strip_trailing_whitespace(file_path)

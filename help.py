import json
import sys
import difflib  # For finding similar command suggestions

# Path to tools.json file
tools_json_path = 'tools.json'


# Load available tools from tools.json
def load_tools():
    with open(tools_json_path, 'r') as f:
        return json.load(f)


# Help messages for common errors
ERROR_HELP = {
    "FileNotFoundError": "The specified file could not be found. Check that the file path is correct, "
                         "or try placing the file in the current or parent directory.",
    "AttributeError": "An unexpected attribute error occurred. This often means an object is missing an attribute or "
                      "method.\n"
                      "Check for typos in attribute names, and ensure required libraries are installed and imported "
                      "correctly.",
    "PermissionError": "The program doesn't have permission to perform this action. Try running the command with "
                       "appropriate permissions"
                       "(e.g., as an administrator), or check file permissions to ensure read/write access.",
    "ZeroDivisionError": "A division by zero occurred. Make sure that denominators in calculations are non-zero, "
                         "and check for any variables that might unexpectedly hold zero values.",
    "ImportError": "A required library could not be imported. Make sure all necessary packages are installed.\n"
                   "If a package is missing, install it using pip (e.g., `pip install <package_name>`).",
    "ModuleNotFoundError": "A specified module could not be found. Verify that the module name is correct, "
                           "and that the library is installed in your environment.",
    "KeyError": "A KeyError occurred. This typically happens when trying to access a dictionary key that does not "
                "exist.\n"
                "Ensure the key is correct, or use `.get()` to access dictionary values safely.",
    "TypeError": "A TypeError occurred. This often happens when an operation is attempted on incompatible types ("
                 "e.g., adding a string to an integer).\n"
                 "Check variable types and ensure compatibility before performing operations.",
    "ValueError": "A ValueError occurred. This typically happens when a function receives an argument of the right "
                  "type but with an inappropriate value.\n"
                  "Ensure input values are within expected ranges or formats.",
    "IndexError": "An IndexError occurred. This usually happens when trying to access an index that is out of range "
                  "for a list or other sequence.\n"
                  "Check that index values are within the valid range for the sequence.",
    "MemoryError": "A MemoryError occurred. The program tried to use more memory than is available. Consider "
                   "optimizing your code or handling smaller data chunks.",
    "OSError": "An OS-related error occurred. This could be due to file access issues, insufficient permissions, "
               "or incorrect file paths.\n"
               "Check the specific message for more details and try running with elevated permissions if needed.",
    "TimeoutError": "A TimeoutError occurred. An operation took too long to complete. Try increasing timeout values "
                    "or optimizing the code for performance.",
    "OverflowError": "An OverflowError occurred. This usually happens when a number is too large to be represented in "
                     "memory.\n"
                     "Consider using smaller numbers or handling large numbers more efficiently.",
    "RuntimeError": "A generic runtime error occurred. This could be due to various reasons, often specific to the "
                    "library or function in use.\n"
                    "Check the error message for more details and consult documentation for possible causes.",
    "StopIteration": "A StopIteration error occurred. This usually happens when an iterator has no more items.\n"
                     "Check loops and iterator usage to ensure they don't go beyond available items.",
    "IndentationError": "An IndentationError occurred. Ensure consistent use of spaces or tabs for indentation, "
                        "especially in nested blocks.\n"
                        "Python requires consistent indentation to define code blocks.",
    "SyntaxError": "A SyntaxError occurred. This indicates an error in the Python syntax. Check for typos, "
                   "missing colons, or unmatched parentheses.",
    "NameError": "A NameError occurred. This usually means a variable or function is not defined before being used.\n"
                 "Ensure all variables and functions are declared and properly spelled before use.",
    "UnboundLocalError": "An UnboundLocalError occurred. This typically happens when a local variable is used before "
                         "being assigned.\n"
                         "Ensure variables are assigned values before using them in expressions."
}

VALID_COMMANDS = ['lw', 'ow', 'help']
VALID_ARGS = {
    'lw': ['-p', '-c', '-m', '-d', '-n', '-sd'],
    'ow': []
}


def get_user_confirmation(prompt="View the help page? [y/n]: "):
    """Prompt the user for a yes/no answer, validating the input."""
    while True:
        user_input = input(prompt).strip().lower()
        if user_input in ["y", "n"]:
            return user_input == "y"  # Returns True for 'y' and False for 'n'
        else:
            print("Invalid input. Please enter 'y' for yes or 'n' for no.")


def display_help(command=None):
    tools = load_tools()

    # Show general usage if no specific command is given
    if not command:
        print("\nAvailable Commands:")
        for acronym, tool_info in tools.items():
            print(f"  {acronym} - {tool_info['description']}")
        print("\nUsage:\n  python main.py [command] [additional arguments]\n")
        return

    # Show specific help for a command
    if command in tools:
        tool = tools[command]
        print(f"\nHelp for '{command}' - {tool['description']}")
        print(f"Script: {tool.get('filename', '[Unknown]')}")
        print("Required packages:", ', '.join(tool.get('packages', [])))
        print("\nUsage:")
        if command == "lw":
            print("  python main.py lw -p   # List top processes")
            print("  python main.py lw -c   # List processes ordered by CPU usage")
            print("  python main.py lw -m   # List processes ordered by Memory usage")
            print("  python main.py lw -d   # List processes ordered by Disk usage")
            print("  python main.py lw -n   # List processes ordered by Network usage")
            print("  python main.py lw -sd [number] # Specify significant digits for output")
        elif command == "ow":
            print("  python main.py ow [filename] [num_windows] [viewer]  # Open file with viewer in multiple windows")
            print("Example:\n  python main.py ow output.txt 4 Notepad")
        else:
            print("  Refer to tools.json for additional details.")


def suggest_correction(argument, command):
    """Suggest similar arguments based on valid options."""
    suggestions = difflib.get_close_matches(argument, VALID_ARGS.get(command, []), n=1)
    if suggestions:
        print(f"Did you mean '{suggestions[0]}' instead of '{argument}'?")


def handle_error(error_message):
    # Analyze the error and offer help if available
    for error_type, help_message in ERROR_HELP.items():
        if error_type in error_message:
            print(f"\nError Detected: {error_type}")
            print(help_message)
            if get_user_confirmation("\nView the help page? [y/n]: "):
                display_help()  # Show general help
            return

    print("Error: No specific help available for this error.")
    if get_user_confirmation("Would you like to see the general help page? [y/n]: "):
        display_help()


if __name__ == "__main__":
    # Get error message passed in from other scripts (if any)
    error_message = sys.argv[1] if len(sys.argv) > 1 else ""
    if error_message:
        handle_error(error_message)
    else:
        # Show general help if no error message is passed
        display_help()

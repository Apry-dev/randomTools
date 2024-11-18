import argparse
import subprocess
import json
import os
import importlib.util
import ast

# Path to tools.json file
tools_json_path = 'tools.json'

# Valid commands and arguments, with specific args that expect values
VALID_COMMANDS = ['lw', 'ow', 'help']
VALID_ARGS = {
    'lw': ['-p', '-c', '-m', '-d', '-n', '-sd'],
    'ow': []  # ow has no flags; it only has positional arguments
}
ARGS_WITH_VALUES = ['-sd']  # Define arguments that require a value
REQUIRED_POSITIONAL_ARGS = {
    'ow': 2  # 'ow' expects two positional arguments: filename and viewer
}


def load_tools():
    if os.path.exists(tools_json_path):
        with open(tools_json_path, 'r') as f:
            return json.load(f)
    else:
        print(f"Error: '{tools_json_path}' not found.")
        return {}


def detect_imports(script_path):
    with open(script_path, 'r') as f:
        tree = ast.parse(f.read())
    imports = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.add(alias.name)
        elif isinstance(node, ast.ImportFrom):
            imports.add(node.module)
    return list(imports)


def update_tools_json():
    if os.path.exists(tools_json_path):
        with open(tools_json_path, 'r') as f:
            tools_data = json.load(f)
    else:
        tools_data = {}

    for tool_acronym, tool_info in tools_data.items():
        script_path = tool_info.get("filename", f"{tool_acronym}.py")
        if os.path.exists(script_path):
            detected_imports = detect_imports(script_path)
            tool_info['packages'] = detected_imports
        else:
            print(f"Warning: {script_path} not found")

    with open(tools_json_path, 'w') as f:
        json.dump(tools_data, f, indent=4)
    print("tools.json has been updated with detected imports.")


def check_package_installed(package):
    spec = importlib.util.find_spec(package)
    return spec is not None


def check_dependencies():
    missing_packages = {}

    tools_data = load_tools()

    for tool, tool_info in tools_data.items():
        packages = tool_info.get('packages', [])
        for package in packages:
            if not check_package_installed(package):
                if tool not in missing_packages:
                    missing_packages[tool] = []
                missing_packages[tool].append(package)

    if missing_packages:
        print("\nWarning: Some packages are missing!")
        for tool, packages in missing_packages.items():
            print(f"{tool} is missing the following packages: {', '.join(packages)}")
        print("\nThe program will continue, but these tools may not work as expected.")


def validate_arguments(command, extra_args):
    """Validate arguments, accounting for flags and positional arguments."""
    expected_positional_args = REQUIRED_POSITIONAL_ARGS.get(command, 0)
    flags_and_values = extra_args[:len(extra_args) - expected_positional_args]
    positional_args = extra_args[len(extra_args) - expected_positional_args:]

    # Validate each flag
    i = 0
    while i < len(flags_and_values):
        arg = flags_and_values[i]

        # Check if argument is valid for the command
        if arg not in VALID_ARGS.get(command, []):
            print(f"Invalid argument '{arg}' for command '{command}'")
            subprocess.run(['python', 'help.py', f"Invalid argument: {arg} for {command}"])
            return False

        # Check if argument requires a value
        if arg in ARGS_WITH_VALUES:
            if i + 1 >= len(flags_and_values) or flags_and_values[i + 1].startswith("-"):
                print(f"Error: '{arg}' requires a value.")
                subprocess.run(['python', 'help.py', f"Missing value for argument: {arg}"])
                return False
            i += 1  # Skip the next item as it is the value for this arg

        i += 1  # Move to the next argument

    # Ensure the correct number of positional arguments
    if len(positional_args) < expected_positional_args:
        print(
            f"Error: '{command}' requires {expected_positional_args} positional arguments, but only {len(positional_args)} were provided.")
        subprocess.run(['python', 'help.py', f"Missing positional arguments for {command}"])
        return False

    return True


def main():
    update_tools_json()
    check_dependencies()

    parser = argparse.ArgumentParser(description="Tool Manager - List available tools or run a specific tool.")

    tools = load_tools()

    parser.add_argument(
        'command',
        choices=list(tools.keys()) + ['list'],
        nargs='?',
        default=None,
        help="Choose a tool or use 'list' to show available tools."
    )

    parser.add_argument(
        'extra_args',
        nargs=argparse.REMAINDER,
        help="Additional arguments to pass to the tool."
    )

    args = parser.parse_args()

    # Prompt user for input if no command is given
    if not args.command:
        print("\nNo command provided. Please choose a tool from the available list:\n")
        print("Available Tools:")
        for acronym, tool_info in tools.items():
            print(f"  {acronym} - {tool_info['description']}")

        user_input = input("\nEnter the tool acronym followed by any options: ").strip().split()

        # Separate the command and additional arguments from user input
        args.command = user_input[0] if user_input else None
        args.extra_args = user_input[1:] if len(user_input) > 1 else []

        # Validate the command itself
        if args.command not in tools.keys() and args.command != 'list':
            print(f"Error: '{args.command}' is not a valid tool.")
            subprocess.run(['python', 'help.py', "Invalid command"])
            return

    # Handle 'list' or 'help' command
    if args.command == 'list' or args.command == 'help':
        subprocess.run(['python', 'help.py'])
        return

    # Validate command arguments if it’s a valid command
    if args.command in VALID_COMMANDS and not validate_arguments(args.command, args.extra_args):
        return

    # Execute the specified command if valid
    if args.command in tools:
        script_filename = tools[args.command].get("filename", f"{args.command}.py")
        if os.path.exists(script_filename):
            subprocess.run(['python', script_filename] + args.extra_args)
        else:
            print(f"Error: Script '{script_filename}' not found.")
            subprocess.run(['python', 'help.py', f"Script '{script_filename}' not found"])


if __name__ == "__main__":
    main()

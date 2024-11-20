import argparse
import subprocess
import os

def main():
    parser = argparse.ArgumentParser(description="Random Tools Manager")
    parser.add_argument(
        'command',
        nargs='?',
        help="Command to run (e.g., lw, ow) or start the GUI if not provided."
    )
    parser.add_argument(
        'extra_args',
        nargs=argparse.REMAINDER,
        help="Additional arguments for the command."
    )
    args = parser.parse_args()

    # If no command is given, launch the GUI
    if not args.command:
        print("No command provided. Launching GUI...")
        subprocess.run(["python", "gui.py"])
        return

    # Handle commands
    if args.command == "lw":
        subprocess.run(["python", "listWindows.py"] + args.extra_args)
    elif args.command == "ow":
        subprocess.run(["python", "openwindows.py"] + args.extra_args)
    elif args.command == "help":
        subprocess.run(["python", "help.py"])
    else:
        print(f"Error: Unknown command '{args.command}'")
        subprocess.run(["python", "help.py"])

if __name__ == "__main__":
    main()

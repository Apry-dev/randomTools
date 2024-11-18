import os
import subprocess
import time
import argparse
import pygetwindow as gw
from ctypes import windll

def get_screen_size():
    # Use ctypes to get the screen size on Windows
    user32 = windll.user32
    screen_width = user32.GetSystemMetrics(0)
    screen_height = user32.GetSystemMetrics(1)
    return screen_width, screen_height

def open_file(filename, num_windows=5, viewer='Notepad'):
    current_dir = os.getcwd()  # Get current directory
    test = os.path.join(current_dir, filename)  # Create full path

    # Check if the file exists in the current directory or parent directory
    if os.path.isfile(test):
        print(f"The file '{filename}' exists in the current directory.")
    else:
        # Go up one level in the directory and check there
        parent_dir = os.path.dirname(current_dir)
        test_parent = os.path.join(parent_dir, filename)

        if os.path.isfile(test_parent):
            print(f"The file '{filename}' exists in the parent directory: {parent_dir}")
            test = test_parent  # Update the path to the file in the parent directory
        else:
            print(f"The file '{filename}' does not exist in the current or parent directory.")
            exit()

    # Open the file in multiple windows with the specified viewer
    for _ in range(num_windows):
        subprocess.Popen([viewer, test], shell=True)
        print("Window Opened")
        time.sleep(0.5)  # Delay to ensure each window opens and registers on the taskbar

    # Get screen size
    screen_width, screen_height = get_screen_size()
    cols = int(num_windows ** 0.5)
    rows = (num_windows // cols) + (num_windows % cols > 0)

    win_width = screen_width // cols
    win_height = screen_height // rows

    # Position each window in a grid layout
    open_windows = gw.getWindowsWithTitle(os.path.basename(filename))
    for index, window in enumerate(open_windows[:num_windows]):
        row, col = divmod(index, cols)
        x = col * win_width
        y = row * win_height
        window.moveTo(x, y)
        window.resizeTo(win_width, win_height)

    print(f"Opened {num_windows} instances of '{filename}' with {viewer}.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Open a file in multiple windows with specified viewer."
    )
    parser.add_argument('filename', help="The name of the file to open.")
    parser.add_argument('num_windows', nargs='?', type=int, default=5, help="Number of windows to open (default is 5).")
    parser.add_argument('viewer', nargs='?', default='Notepad', help="Application to use for opening the file (default is Notepad).")
    args = parser.parse_args()

    open_file(args.filename, args.num_windows, args.viewer)

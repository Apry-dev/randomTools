import math
import os
import pygetwindow as gw
import psutil
import argparse
import subprocess

# Function to count and list open windows
def count_open_windows():
    windows = gw.getAllTitles()
    open_windows = [win for win in windows if win.strip()]
    return open_windows

# Function to print the matrix of open windows
def print_matrix_windows(windows, output_file="output.txt"):
    num_windows = len(windows)
    if num_windows == 0:
        output_str = "No Open Windows :3\n"
    else:
        max_length = max(len(win) for win in windows)
        half_length = max_length // 2
        cols = math.ceil(math.sqrt(num_windows))
        rows = math.ceil(num_windows / cols)

        separator = "+-" + ("-" * half_length) + "|" + ("-" * half_length) + "-+"
        output_str = f"{separator * cols}\n"

        for i in range(rows):
            row_str = ""
            for j in range(cols):
                index = i * cols + j
                if index < num_windows:
                    row_str += f"{windows[index]:<{max_length + 4}}"
            output_str += row_str + "\n"
            output_str += f"{separator * cols}\n"

    with open(output_file, 'w') as f:
        f.write(output_str)
    print(f"Matrix of windows written to {output_file}")
    prompt_open_file(output_file)

# Function to get top 10 processes
def get_top_processes(order_by=None):
    processes = []
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            cpu_percent = proc.cpu_percent(interval=None)
            memory_percent = proc.memory_percent()
            io_counters = proc.io_counters() if proc.io_counters() else None
            disk_usage = io_counters.read_bytes + io_counters.write_bytes if io_counters else 0
            net_usage = io_counters.read_count + io_counters.write_count if io_counters else 0

            processes.append({
                'pid': proc.pid,
                'name': proc.name(),
                'cpu_percent': cpu_percent,
                'memory_percent': memory_percent,
                'disk_usage': disk_usage,
                'net_usage': net_usage
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    if order_by == 'cpu':
        processes.sort(key=lambda p: p['cpu_percent'], reverse=True)
    elif order_by == 'memory':
        processes.sort(key=lambda p: p['memory_percent'], reverse=True)
    elif order_by == 'disk':
        processes.sort(key=lambda p: p['disk_usage'], reverse=True)
    elif order_by == 'network':
        processes.sort(key=lambda p: p['net_usage'], reverse=True)

    return processes[:10]

# Display top processes with optional digit formatting
def display_top_processes(order_by=None, significant_digits=None, output_file="output.txt"):
    windows = gw.getAllTitles()
    max_length = max(len(win) for win in windows)
    output_str = f"\nTop 10 Processes (ordered by {order_by if order_by else 'default'}):\n"
    processes = get_top_processes(order_by)

    for proc in processes:
        memory_display = f"{proc['memory_percent']:.{significant_digits}f}%" if significant_digits else f"{proc['memory_percent']}%"
        disk_display = f"{proc['disk_usage'] / (10 ** (len(str(proc['disk_usage'])) - significant_digits)):.{significant_digits}f}" if significant_digits else f"{proc['disk_usage']:,} bytes"
        net_display = f"{proc['net_usage'] / (10 ** (len(str(proc['net_usage'])) - significant_digits)):.{significant_digits}f}" if significant_digits else f"{proc['net_usage']:,} "

        output_str += (f"PID: {proc['pid']}, Name: {proc['name']}, CPU: {proc['cpu_percent']}%, "
                       f"Memory: {memory_display}, Disk Usage: {disk_display} bytes, "
                       f"Net Usage: {net_display} counts\n")

    with open(output_file, 'w') as f:
        f.write(output_str)
    print(f"Process information written to {output_file}")
    prompt_open_file(output_file)

# Function to prompt user and open the file if requested
def prompt_open_file(file_path):
    open_file = input("Would you like to open the output file? [y/n]: ").strip().lower()
    if open_file == 'y':
        try:
            # Use the default viewer to open the file
            if os.name == 'nt':  # For Windows
                os.startfile(file_path)
            elif os.name == 'posix':  # For macOS and Linux
                subprocess.run(['open' if os.uname().sysname == 'Darwin' else 'xdg-open', file_path])
            print("Output file opened.")
        except Exception as e:
            print(f"Error opening file: {e}")
    else:
        print("File not opened.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="List open windows and top processes.")
    parser.add_argument('-p', '--processes', action='store_true', help="List the top 10 processes.")
    parser.add_argument('-c', '--cpu', action='store_true', help="Order processes by CPU usage.")
    parser.add_argument('-m', '--memory', action='store_true', help="Order processes by Memory usage.")
    parser.add_argument('-d', '--disk', action='store_true', help="Order processes by Disk usage.")
    parser.add_argument('-n', '--network', action='store_true', help="Order processes by Network usage.")
    parser.add_argument('-sd', '--significant_digits', type=int, help="Number of significant digits for numerical output.")

    args = parser.parse_args()

    # Determine sorting based on arguments
    order_by = None
    if args.cpu:
        order_by = 'cpu'
    elif args.memory:
        order_by = 'memory'
    elif args.disk:
        order_by = 'disk'
    elif args.network:
        order_by = 'network'

    # If any process-related option is specified, show sorted processes
    if args.processes or order_by:
        display_top_processes(order_by, args.significant_digits, "output.txt")
    else:
        # Otherwise, list open windows and print matrix to output.txt
        open_windows = count_open_windows()
        print_matrix_windows(open_windows, "output.txt")

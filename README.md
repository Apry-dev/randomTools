
# randomTools

**randomTools** is a dynamic, extensible project designed to provide a variety of utilities, such as listing open windows, opening files, and more. This project is actively under development, and new features will be added over time.

---

## Features

- **List Open Windows**: Displays all open windows and their titles in a structured format.
- **Open Files**: Opens a specified file in multiple windows with a chosen viewer application.
- **Dynamic CLI**: Includes command-line arguments for flexible usage.
- **Error Handling**: Provides detailed help pages for fixing errors encountered during runtime.

---

## Installation

To get started with **randomTools**, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/YOUR-USERNAME/randomTools.git
   ```

2. Navigate to the project directory:
   ```bash
   cd randomTools
   ```

3. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. (Optional) For Linux/WSL users: Install additional tools like `xdg-open` if not already installed:
   ```bash
   sudo apt install xdg-utils
   ```

---

## Commands and Usage

### `lw` - List Open Windows

The `lw` command provides a list of open windows on the toolbar or top processes running on your system. 

#### Usage:
```bash
python main.py lw [OPTIONS]
```

#### Options:
- `-p` : Lists the top 10 processes.
- `-c` : Orders processes by CPU usage.
- `-m` : Orders processes by memory usage.
- `-d` : Orders processes by disk usage.
- `-n` : Orders processes by network usage.
- `-sd [DIGITS]` : Limits the significant digits in numerical output.

#### Example Commands:
- List the top 10 processes:
  ```bash
  python main.py lw -p
  ```
- List the top 10 processes ordered by memory usage:
  ```bash
  python main.py lw -m
  ```
- List open windows and print the output to `output.txt`:
  ```bash
  python main.py lw
  ```

---

### `ow` - Open Windows

The `ow` command opens a specified file in multiple windows using a selected viewer application.

#### Usage:
```bash
python main.py ow [FILENAME] [NUM_WINDOWS] [VIEWER]
```

#### Parameters:
- `FILENAME` : The name of the file to open.
- `NUM_WINDOWS` : The number of windows to open.
- `VIEWER` : The application to open the file with (e.g., `notepad`, `code`).

#### Example Commands:
- Open `output.txt` in 3 windows using `notepad`:
  ```bash
  python main.py ow output.txt 3 notepad
  ```
- Open `README.md` in 2 windows using `code` (VSCode):
  ```bash
  python main.py ow README.md 2 code
  ```

---

### `help` - Help Page

The `help` command provides detailed assistance for using the project and resolving errors.

#### Usage:
```bash
python main.py help
```

If an error occurs during execution, the program will prompt:
```plaintext
Error: [Error Description]
Would you like to view the help page? [y/n]
```

Selecting `y` will display the relevant help message.

---

## Development

**randomTools** is an ongoing project, and contributions are welcome! To add new tools:
1. Create a new script file (e.g., `newTool.py`).
2. Update `tools.json` with the tool’s description and filename.
3. Add functionality and test thoroughly.

---

## Planned Features

- Integration with GitHub Actions for CI/CD.
- Unit tests to ensure stability.
- Enhanced error handling and logging.
- Additional tools to improve productivity.

---

## Issues and Contributions

If you encounter issues or have ideas for improvement:
1. Check the [Issues](https://github.com/YOUR-USERNAME/randomTools/issues) page.
2. Submit a detailed bug report or feature request.

To contribute:
1. Fork the repository.
2. Create a new branch for your feature/fix:
   ```bash
   git checkout -b feature-branch
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add new feature/fix"
   ```
4. Push the branch and open a pull request:
   ```bash
   git push origin feature-branch
   ```

---

## License

This project is licensed under the MIT License. See `LICENSE` for more details.

---

## Author

Developed and maintained by **Apry**. :3


---

### Key Features of the `README.md`:
1. **Clear Structure**: Sections are divided into features, commands, installation, and contribution guidelines.
2. **Detailed Commands**: Each command and its options are explained with examples.
3. **Contributor-Friendly**: Encourages others to contribute with clear instructions.
4. **Formatted for GitHub**: Optimized for rendering on GitHub.

Let me know if you'd like to make further adjustments! :3

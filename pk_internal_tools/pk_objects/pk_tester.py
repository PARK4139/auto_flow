import os
import shutil
from pathlib import Path
import logging
import pytest
from typing import List, Dict

# Custom plugin for pytest to capture results
class ResultCapturePlugin:
    def __init__(self):
        self.results = []

    @pytest.hookimpl(hookwrapper=True)
    def pytest_runtest_makereport(self, item, call):
        outcome = yield
        report = outcome.get_result()

        if report.when == 'call':
            # Safely represent funcargs
            try:
                # item.funcargs contains the arguments passed to the test function
                args_repr = {k: repr(v) for k, v in item.funcargs.items()}
            except Exception as e:
                args_repr = "Could not represent args."

            self.results.append({
                "file": Path(item.fspath).name,
                "function": item.name,
                "outcome": report.outcome.upper(),
                "duration": report.duration,
                "arguments": str(args_repr),
                "traceback": None
            })

class PkTester:
    """
    A helper class for testing purposes.
    Provides methods to create dummy files, directories, and directory trees,
    and to verify their properties.
    Extended to include test discovery, execution, and reporting.
    """
    def __init__(self, root_path: Path):
        """
        Initializes the PkTester with a root directory for test artifacts.

        Args:
            root_path (Path): The root directory where all dummy files/dirs will be created.
        """
        self.root_path = Path(root_path)
        self.root_path.mkdir(parents=True, exist_ok=True)
        logging.info(f"PkTester initialized with root path: {self.root_path}")

    def create_dummy_file(self, file_path: str, size_kb: int = 1, content: bytes = None):
        """
        Creates a dummy file with a specified size.

        Args:
            file_path (str): The relative path of the file to create within the root_path.
            size_kb (int): The size of the file in kilobytes.
            content (bytes, optional): If provided, this content is written to the file.
                                       The size_kb parameter is ignored. Defaults to None.
        """
        full_path = self.root_path / file_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        
        if content is not None:
            full_path.write_bytes(content)
        else:
            with open(full_path, 'wb') as f:
                f.write(b'\0' * (size_kb * 1024))
        logging.debug(f"Created dummy file: {full_path} (Size: {size_kb} KB)")
        return full_path

    def create_dummy_directory(self, dir_path: str):
        """
        Creates an empty dummy directory.

        Args:
            dir_path (str): The relative path of the directory to create.
        """
        full_path = self.root_path / dir_path
        full_path.mkdir(parents=True, exist_ok=True)
        logging.debug(f"Created dummy directory: {full_path}")
        return full_path

    def create_dummy_tree(self, structure: dict):
        """
        Creates a directory tree based on a dictionary structure.

        Args:
            structure (dict): A dict representing the directory structure.
                              Keys are file/dir names.
                              Value for a file is its size in KB (int).
                              Value for a directory is another dict (can be empty).
        """
        logging.info(f"Creating dummy tree in {self.root_path}")
        self._create_tree_recursive(self.root_path, structure)

    def _create_tree_recursive(self, current_path: Path, structure: dict):
        """Recursively creates the directory tree."""
        for name, value in structure.items():
            path = current_path / name
            if isinstance(value, dict):
                path.mkdir(exist_ok=True)
                self._create_tree_recursive(path, value)
            elif isinstance(value, (int, float)):
                self.create_dummy_file(str(path.relative_to(self.root_path)), size_kb=value)
            else:
                logging.warning(f"Unsupported type in structure: {type(value)} for name {name}")

    def get_tree_stats(self):
        """
        Calculates statistics for the directory tree under the root path.

        Returns:
            dict: A dictionary with 'file_count', 'total_size_bytes', and 'dir_count'.
        """
        file_count = 0
        total_size_bytes = 0
        dir_count = 0
        for root, dirs, files in os.walk(self.root_path):
            dir_count += len(dirs)
            file_count += len(files)
            for file in files:
                try:
                    total_size_bytes += (Path(root) / file).stat().st_size
                except FileNotFoundError:
                    # File might be gone during walk, rare but possible
                    pass
        stats = {
            'file_count': file_count,
            'total_size_bytes': total_size_bytes,
            'dir_count': dir_count
        }
        logging.debug(f"Tree stats for {self.root_path}: {stats}")
        return stats
    
    def compare_tree_stats(self, expected_stats: dict):
        """
        Compares the actual tree statistics with expected values.

        Args:
            expected_stats (dict): A dictionary with expected values for
                                   'file_count', 'total_size_bytes', 'dir_count'.

        Returns:
            tuple[bool, dict]: A tuple containing a boolean (True if all stats match)
                               and a dictionary with the comparison details.
        """
        actual_stats = self.get_tree_stats()
        comparison = {}
        all_match = True

        for key, expected_value in expected_stats.items():
            actual_value = actual_stats.get(key)
            match = actual_value == expected_value
            comparison[key] = {'expected': expected_value, 'actual': actual_value, 'match': match}
            if not match:
                all_match = False
        
        logging.info(f"Tree stats comparison result: {'Success' if all_match else 'Failure'}")
        logging.debug(f"Comparison details: {comparison}")
        return all_match, comparison

    def get_test_files(self, test_root_dir: Path) -> List[Path]:
        """
        Discovers Python test files under a given test root directory.
        Test files are assumed to be Python files starting with 'test_'.
        """
        logging.info(f"Discovering test files in: {test_root_dir}")
        # Assuming test files are directly in test_root_dir or its subdirectories
        test_files = [f for f in test_root_dir.rglob('test_*.py') if f.is_file() and not f.name.startswith('__')]
        logging.debug(f"Found {len(test_files)} test files.")
        return test_files

    def run_selected_tests(self, test_file_paths: List[Path], verbose: bool = False) -> List[Dict]:
        """
        Runs selected pytest files programmatically and captures results.
        Returns a list of dictionaries with test results.
        """
        import pytest
        import io
        import sys

        logging.info(f"Running {len(test_file_paths)} selected tests...")

        capture_plugin = ResultCapturePlugin()
        
        # Construct pytest arguments
        pytest_args = [str(f) for f in test_file_paths]
        if verbose:
            pytest_args.append("-v") # Verbose output from pytest
            pytest_args.append("-s") # Allow stdout/stderr to pass through

        # Run pytest and capture its output for debugging
        original_stdout = sys.stdout
        original_stderr = sys.stderr
        captured_stdout = io.StringIO()
        captured_stderr = io.StringIO()
        sys.stdout = captured_stdout
        sys.stderr = captured_stderr

        exit_code = -1
        try:
            # pytest.main returns an exit code. Results are captured by our plugin.
            exit_code = pytest.main(pytest_args, plugins=[capture_plugin])
        finally:
            sys.stdout = original_stdout
            sys.stderr = original_stderr

        stdout_val = captured_stdout.getvalue()
        stderr_val = captured_stderr.getvalue()

        if stdout_val:
            logging.debug(f"Pytest stdout:\n{stdout_val}")
        if stderr_val:
            logging.error(f"Pytest stderr:\n{stderr_val}")
        
        logging.debug(f"Pytest exit code: {exit_code}")
        logging.debug(f"Pytest run completed. Captured {len(capture_plugin.results)} test results.")
        return capture_plugin.results

    def display_results(self, results: List[Dict], view_mode: str = "simple"):
        """
        Displays test results using rich.table.Table for better readability.
        """
        import json
        import ast
        from rich.console import Console
        from rich.table import Table
        from rich.text import Text
        import rich.box

        console = Console()
        table = Table(
            title=Text("Test Results", style="bold white"),
            style="white",
            box=rich.box.MINIMAL_DOUBLE_HEAD
        )

        # Define columns based on view_mode
        if view_mode == "simple":
            table.add_column(Text("Outcome", style="bold white"), justify="left", no_wrap=True)
            table.add_column(Text("Test File", style="bold white"), justify="left", min_width=30, overflow="fold")
            table.add_column(Text("Test Function", style="bold white"), justify="left", min_width=30, overflow="fold")
        else:  # detailed
            table.add_column(Text("Outcome", style="bold white"), justify="left", no_wrap=True, width=8)
            table.add_column(Text("Test File", style="bold white"), justify="left", no_wrap=True, min_width=20)
            table.add_column(Text("Test Function", style="bold white"), justify="left", no_wrap=True, min_width=20)
            table.add_column(Text("Arguments", style="bold white"), justify="left", min_width=30)
            table.add_column(Text("Duration (s)", style="bold white"), justify="right", no_wrap=True)
            table.add_column(Text("Traceback", style="bold white"), justify="left")

        for result in results:
            outcome_text = Text(result["outcome"])
            if result["outcome"] == "PASSED":
                outcome_text.stylize("green")
            elif result["outcome"] == "FAILED":
                outcome_text.stylize("bold red")
            elif result["outcome"] == "SKIPPED":
                outcome_text.stylize("yellow")
            else:
                outcome_text.stylize("blue")

            function_name = result.get("function", "N/A")
            file_name = result.get("file", "N/A")
            duration = result.get("duration", 0.0)
            arguments_info_str = result.get("arguments", "{}")
            traceback_info = result.get("traceback", "")

            # Pretty-print arguments
            try:
                # Safely evaluate the string representation of the dictionary
                args_dict = ast.literal_eval(arguments_info_str)
                # Format to a readable JSON string
                arguments_pretty = json.dumps(args_dict, indent=2)
            except (ValueError, SyntaxError):
                # Fallback for malformed strings
                arguments_pretty = arguments_info_str

            if view_mode == "simple":
                table.add_row(
                    outcome_text,
                    Text(file_name, style="cyan"),
                    Text(function_name, style="white")
                )
            else:
                table.add_row(
                    outcome_text,
                    Text(file_name, style="white"),
                    Text(function_name, style="white"),
                    Text(arguments_pretty, style="cyan"),
                    Text(f"{duration:.4f}", style="magenta"),
                    Text(traceback_info, style="red") if traceback_info else Text(""),
                )

        console.print(table)


    def cleanup(self):
        """
        Removes the root directory and all its contents.
        """
        if self.root_path.exists():
            shutil.rmtree(self.root_path)
            logging.info(f"Cleaned up test directory: {self.root_path}")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cleanup()

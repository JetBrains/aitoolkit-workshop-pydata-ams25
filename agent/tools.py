import os
import textwrap
from typing import Optional

import pytest
from langchain_core.tools import tool


from .run_dir import ensure_run_dir as _ensure_run_dir


@tool
def run_tests_inproc() -> Optional[str]:
    """
    Run pytest against the current per-run output directory managed by this tool.

    Behavior:
    - Uses the single run folder created under <project_root>/out/<timestamp>/.
    - Expects that code and tests have already been saved via save_code and save_tests.
    - Executes pytest targeting the explicit tests.py path in the run directory.
    - Returns None if all tests pass; otherwise returns the JUnit XML report text.
    - Clean-up: Ensures any stale JUnit report is removed before running, and deletes the report
      after reading/returning it to avoid stale state on subsequent runs.
    """
    run_dir = _ensure_run_dir()
    sol = os.path.join(run_dir, "solution.py")
    tst = os.path.join(run_dir, "tests.py")
    xml = os.path.join(run_dir, "report.xml")

    # Validate presence of required files
    if not os.path.exists(sol):
        return "No solution.py found in the current run directory. Use save_code first."
    if not os.path.exists(tst):
        return "No tests.py found in the current run directory. Use save_tests first."

    # Remove any stale report before running
    try:
        if os.path.exists(xml):
            os.remove(xml)
    except Exception:
        # Non-fatal; continue running tests
        pass

    # Request a structured report we can parse (target the tests file directly so pytest doesn't rely on filename patterns)
    ret = pytest.main([tst, "--maxfail=1", "--disable-warnings", f"--junitxml={xml}", "--tb=short"])

    if ret == 0:
        # On success, ensure no leftover report remains
        try:
            if os.path.exists(xml):
                os.remove(xml)
        except Exception:
            pass
        return None

    # Read the XML text so the caller can inspect errors/failures, then clean up the file
    try:
        with open(xml, "r", encoding="utf-8") as f:
            report = f.read()
        try:
            os.remove(xml)
        except Exception:
            pass
        return report
    except Exception:
        return "Tests failed (could not read JUnit report)."


@tool
def check_code_executes() -> str:
    """
    Execute the saved solution.py from the current per-run directory.

    Behavior:
    - Expects that code has already been saved via save_code.
    - Executes solution.py and reports success or returns the exception string.

    Returns:
        str: Exception string if execution fails, otherwise a success message.
    """
    try:
        run_dir = _ensure_run_dir()
        sol_path = os.path.join(run_dir, "solution.py")

        if not os.path.exists(sol_path):
            return "No solution.py found to execute. Use save_code first."

        with open(sol_path, "r", encoding="utf-8") as f:
            src = f.read()
        # Execute the code in a clean global namespace with the correct filename
        exec(compile(src, sol_path, "exec"), {})
        return "The program has been executed successfully!"
    except Exception as e:
        return str(e)


@tool
def think(thought: str) -> str:
    """Use the tool to think about something.
           This is perfect to start your workflow.
           It will not collect new information or take any actions, but just append the thought to the log and return the result.
           Use it when complex reasoning or some cache memory or a scratchpad is needed.


           :param thought: A thought to think about and log.
           :return: The full log of thoughts and the new thought.
    """
    return thought


@tool
def save_code(code: str) -> str:
    """Save solution code into a single controlled file for the current run.

    Behavior and constraints:
    - Creates a single per-run folder under <project_root>/out/<timestamp>/ on first use.
    - Writes ONLY to <run_folder>/solution.py (overwrites if already exists this run).
    - The folder name and file path are controlled by this tool and not configurable.

    Args:
        code: Python source to save as solution.py.

    Returns:
        Absolute file path to the saved solution.py.
    """
    run_dir = _ensure_run_dir()
    sol_path = os.path.join(run_dir, "solution.py")
    code_src = textwrap.dedent(code).lstrip("\n")
    with open(sol_path, "w", encoding="utf-8") as f:
        f.write(code_src)
    return sol_path


@tool
def save_tests(tests: str) -> str:
    """Save tests into a single controlled file for the current run.

    Behavior and constraints:
    - Creates a single per-run folder under <project_root>/out/<timestamp>/ on first use.
    - Writes ONLY to <run_folder>/tests.py (overwrites if already exists this run).
    - The folder name and file path are controlled by this tool and not configurable.

    Note: When used together with run_tests_inproc, ensure your tests import from
    solution.py accordingly (e.g., `from solution import my_func`).

    Args:
        tests: Python tests (e.g., pytest-style) to save as tests.py.

    Returns:
        Absolute file path to the saved tests.py.
    """
    run_dir = _ensure_run_dir()
    tests_path = os.path.join(run_dir, "tests.py")
    tests_src = textwrap.dedent(tests).lstrip("\n")
    with open(tests_path, "w", encoding="utf-8") as f:
        f.write(tests_src)
    return tests_path

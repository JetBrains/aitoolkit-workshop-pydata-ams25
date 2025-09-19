import os
import tempfile
import textwrap
from typing import Optional

import pytest
from langchain_core.tools import tool


@tool
def run_tests_inproc(solution: str, tests: str) -> Optional[str]:
    """
    Runs Python test cases alongside provided solution in an isolated environment and
    returns a JUnit XML report of the test results in case of failure. If all tests
    succeed, it returns None. The function leverages pytest for test execution and
    temporarily writes the code and tests to disk during processing.

    :param solution: The generated Python source code to be tested.
    :type solution: str
    :param tests: The generated Python test cases, written in a pytest-compatible format. Required solution functions should be imported from `solution.py`
    :type tests: str
    :return: A JUnit XML string containing the results if tests fail, or None if
             all tests pass.
    :rtype: Optional[str]
    :raises Exception: If an error occurs while reading the generated JUnit report.
    """
    code_src = textwrap.dedent(solution).lstrip("\n")
    tests_src = textwrap.dedent(tests).lstrip("\n")
    with tempfile.TemporaryDirectory(prefix="code_gen_") as tmp:
        sol = os.path.join(tmp, "solution.py")
        tst = os.path.join(tmp, "test_solution.py")
        xml = os.path.join(tmp, "report.xml")
        with open(sol, "w", encoding="utf-8") as f:
            f.write(code_src)
        with open(tst, "w", encoding="utf-8") as f:
            f.write(tests_src)
        # Request a structured report we can parse
        ret = pytest.main([tmp, "--maxfail=1", "--disable-warnings", f"--junitxml={xml}", "--tb=short"])
        if ret == 0:
            return None
        # Read the XML text so the caller can inspect errors/failures
        try:
            with open(xml, "r", encoding="utf-8") as f:
                return f.read()
        except Exception:
            return "Tests failed (could not read JUnit report)."


@tool
def check_code_executes(code: str) -> str:
    """
    Checks if the given code compiles and executes

    Args:
        code (str): The code which needs to be checked

    Returns:
        exception (str): Result of the check: exception string or "The program has been executed successfully!" if there's no exception
    """

    try:
        exec(code, {})
        return "The program has been executed successfully!"
    except Exception as e:
        return str(e)

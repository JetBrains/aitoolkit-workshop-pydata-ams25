from pathlib import Path

from langchain.agents import AgentExecutor
from langchain.agents import create_react_agent
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI


@tool
def check_code_executes(code: str) -> bool:
    """
    Checks if the given code compiles and executes

    Args:
        code (str): The code which needs to be checked

    Returns:
        result (bool): Result of the check: True if the code executes and compiles, False otherwise
    """

    try:
        exec(code)
        return True
    except Exception as e:
        error_message = [
            (
                "user",
                f"Your solution failed the code execution test: {e}) Reflect on this error and your prior attempt to solve the problem. (1) State what you think went wrong with the prior solution and (2) try to solve this problem again. Return the FULL SOLUTION. Use the code tool to structure the output with a prefix, imports, and code block:",
            )
        ]
        return False

def build_graph():
    tools = [check_code_executes]
    agent = create_react_agent(
        llm=ChatOpenAI(model="gpt-4o"),
        tools=tools,
        prompt=PromptTemplate.from_template(Path("agent/react.prompt").read_text()),
    )
    return AgentExecutor(agent=agent, tools=tools, verbose=True)

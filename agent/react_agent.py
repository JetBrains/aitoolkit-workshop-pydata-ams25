from pathlib import Path

from langchain_core.messages import SystemMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel
from pydantic import Field

from agent.tools import check_code_executes
from agent.tools import run_tests_inproc
from agent.tools import think


# Data model
class Code(BaseModel):
    """Schema for code solutions to coding questions split into 2 parts: Problem description and the Code block itself"""
    prefix: str = Field(description="Very brief description of the problem and approach")
    code: str = Field(description="Code block, save here code exclusively without any formatting!")
    tests: str = Field(description="Tests code block, save here code exclusively without any formatting!")


def build_prompt(tools):
    template = PromptTemplate.from_template(Path("agent/react.prompt").read_text())

    # Compose tool descriptions and names
    tool_names = ", ".join(getattr(t, "name", str(t)) for t in tools)
    tool_lines = []
    for t in tools:
        name = getattr(t, "name", t.__class__.__name__)
        desc = getattr(t, "description", "") or ""
        # Try to extract argument names if available
        args_list = []
        try:
            args = getattr(t, "args", None)
            if isinstance(args, dict):
                args_list = list(args.keys())
        except Exception:
            pass
        args_str = f" Args: {', '.join(args_list)}" if args_list else ""
        tool_lines.append(f"- {name}: {desc}{args_str}")
    tools_block = "\n".join(tool_lines)

    # Inject placeholders now using partial
    return str(template.invoke(input={"tools": tools_block, "tool_names": tool_names}))



def build_graph():
    tools = [check_code_executes, run_tests_inproc, think]
    agent = create_react_agent(
        ChatOpenAI(model="gpt-4o-mini"),
        tools,
        checkpointer=MemorySaver(),
        response_format=Code,
        prompt=SystemMessage(build_prompt(tools)),
    )
    return agent

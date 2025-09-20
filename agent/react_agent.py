from pathlib import Path

from langchain_core.messages import SystemMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

from agent.tools import think


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
    tools = [think]
    agent = create_react_agent(
        ChatOpenAI(model="gpt-4o-mini"),
        tools,
        checkpointer=MemorySaver(),
        prompt=SystemMessage(build_prompt(tools)),
    )
    return agent

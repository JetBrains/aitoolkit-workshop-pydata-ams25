from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from pydantic import BaseModel
from pydantic import Field

from agent.tools import check_code_executes
from agent.tools import run_tests_inproc


# Data model
class Code(BaseModel):
    """Schema for code solutions to coding questions split into 2 parts: Problem description and the Code block itself"""
    prefix: str = Field(description="Description of the problem and approach")
    code: str = Field(description="Code block, save here code exclusively without any formatting!")


def build_graph():
    tools = [check_code_executes, run_tests_inproc]
    agent = create_react_agent(
        ChatOpenAI(model="gpt-4o"),
        tools,
        checkpointer=MemorySaver(),
        response_format=Code,
        # prompt=PromptTemplate.from_template(Path("agent/react.prompt").read_text()),
    )
    return agent

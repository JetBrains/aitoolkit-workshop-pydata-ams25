from typing import Annotated, TypedDict

from langgraph.graph.message import AnyMessage, add_messages


class GraphState(TypedDict):
    """
    Represents the state of our graph.

    Attributes:
        error : Binary flag for control flow to indicate whether test error was tripped
        messages : With user question, error messages, reasoning
        code_block : Code solution
        test_block : Tests that test the code solution
        remaining_steps : Number of steps remaining
    """

    messages: Annotated[list[AnyMessage], add_messages]
    code_block: str
    test_block: str | None
    error: str | None
    remaining_steps: int

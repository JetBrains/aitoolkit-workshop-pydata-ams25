from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from .data_model import Code


def get_llm():
    model_name = "gpt-4o"
    llm = ChatOpenAI(model=model_name)

    # Prompt
    code_gen_prompt_claude = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are a coding assistant. Ensure any code you provide can be executed with all required imports and variables \n
                defined. Structure your answer: 1) a prefix describing the code solution, 2) the imports, 3) the functioning code block.
                \n Here is the user question:""",
            ),
            ("placeholder", "{messages}"),
        ]
    )

    # LLM
    result = llm.with_structured_output(Code, include_raw=False)
    return result
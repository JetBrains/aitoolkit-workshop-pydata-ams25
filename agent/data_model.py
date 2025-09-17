from langchain_core.pydantic_v1 import BaseModel, Field

# Data model
class Code(BaseModel):
    """Code output"""

    description = "Schema for code solutions to coding questions split into 3 parts: Problem description, Imports and the Code block itself"
    prefix: str = Field(description="Description of the problem and approach")
    imports: str = Field(description="Code block import statements")
    code: str = Field(description="Code block not including import statements")
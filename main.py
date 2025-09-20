from dotenv import load_dotenv
import asyncio

from langchain_core.messages import HumanMessage

from agent.react_agent import build_graph


async def main():
    # question = input("Your question about PyData schedule: ")
    question = "What would suit me best if I'm interested in observability tooling in PyCharm?"
    question = "Which talk has ambiguous topic which hard to understand without its description?"
    question = "What will be on the 'Untitled13.ipynb' talk?"

    graph = build_graph()
    result = await graph.ainvoke({"messages": [HumanMessage(content=question)]}, config={"configurable": {"thread_id": "1"}})
    answer = result["messages"][-1].content
    print(answer)

if __name__ == "__main__":
    load_dotenv()
    asyncio.run(main())

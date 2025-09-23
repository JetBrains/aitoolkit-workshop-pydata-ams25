from dotenv import load_dotenv
import asyncio

from langchain_core.messages import HumanMessage

from agent.react_agent import build_graph


async def main():
    question = "Which talk is first?"  # Task 1
    # question = "Which talk is happening right now?"  # Task 2
    # question = "What is the 'Untitled13.ipynb' talk about?"  # Task 3
    # question = "Which company does the speaker of the current talk?"  # Task 4

    # --- EXTRA TASKS! ---

    # # Task 5
    # question = "How long until lunch?"  # The agent doesn't know the lunchtime, but it can estimate it.
    # # However, the agent doesn't know that tomorrow you need to be at the venue at 08:30 for registration!
    # question = "What time should I be at the venue tomorrow?"
    # # Hint: provide the agent with a search tool.
    # # Use TavilySearchResults from langchain_community.tools, but you'll need to generate a token.
    # # Or simply hard-code the missing parts of the schedule. :)

    # # Task 6
    # question = "Give me the LinkedIn profile of the current speaker."
    # # Hint: use a search engine, since LinkedIn doesn't provide an API for this.


    graph = build_graph()
    result = await graph.ainvoke({"messages": [HumanMessage(content=question)]}, config={"configurable": {"thread_id": "1"}})
    answer = result["messages"][-1].content
    print(answer)

if __name__ == "__main__":
    load_dotenv()
    asyncio.run(main())

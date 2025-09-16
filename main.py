from dotenv import load_dotenv
import asyncio

from agent import build_graph


async def main():
    graph = build_graph()

    # ------
    question = """Create a Python program that allows two players to play a game of Tic-Tac-Toe. The game should be played on a 3x3 grid. The program should:

- Allow players to take turns to input their moves.
- Check for invalid moves (e.g., placing a marker on an already occupied space).
- Determine and announce the winner or if the game ends in a draw.

Requirements:
- Use a 2D list to represent the Tic-Tac-Toe board.
- Use functions to modularize the code.
- Validate player input.
- Check for win conditions and draw conditions after each move."""

    initial_input ={"messages": [("user", question)], "iterations": 0}
    config = {"configurable": {"thread_id": "1"}}

    print(f"Question: {question}")
    result = await graph.ainvoke(input=initial_input, config=config)
    answer = result["messages"][-1].content
    print(f"Answer: {answer}")
    # ------

if __name__ == "__main__":
    load_dotenv()
    asyncio.run(main())
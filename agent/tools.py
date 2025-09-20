import os
import json
from datetime import datetime

from langchain_core.tools import tool


@tool
def think(thought: str) -> str:
    """Use the tool to think about something.
           This is perfect to start your workflow.
           It will not collect new information or take any actions, but just append the thought to the log and return the result.
           Use it when complex reasoning or some cache memory or a scratchpad is needed.


           :param thought: A thought to think about and log.
           :return: The full log of thoughts and the new thought.
    """
    return thought


@tool
def read_schedule() -> str:
    """Use this tool to read the PyData schedule about which a user will ask questions.

    Returns:
        str: The PyData Amsterdam 2025 schedule data.
        The file is located in the 'data' directory.
    """
    schedule_path = os.path.join("data", "pydata_amsterdam_2025_schedule.csv")
    with open(schedule_path, "r") as f:
        schedule = f.read()
    return schedule


@tool
def get_current_datetime() -> str:
    """Get the current date and time.

    Returns:
        str: The current date and time in format YYYY-MM-DD HH:MM:SS
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


@tool
def get_event_details(event_id: str) -> str:
    """Get detailed information about a specific event.

    Args:
        event_id: The ID of the event to get details for.

    Returns:
        str: The detailed description of the event.
    """
    descriptions_path = os.path.join("data", "pydata_amsterdam_2025_descriptions.json")
    with open(descriptions_path, "r") as f:
        descriptions = json.load(f)
    return json.dumps(descriptions.get(event_id, {}))

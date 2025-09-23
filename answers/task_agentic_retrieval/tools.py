import json

from langchain_core.tools import tool

from utils.datetime import current_datetime
from utils.datetime import parse_iso
from utils.schedule import get_schedule, get_descriptions, get_speakers


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


# @tool
# def read_schedule() -> str:
#     """Use this tool to read the PyData schedule about which a user will ask questions.
#
#     Returns:
#         str: The PyData Amsterdam 2025 schedule data as JSON text.
#     """
#     schedule = get_schedule(out_format="dict")
#     return json.dumps(schedule, indent=4)


@tool
def get_event_details(event_name: str) -> str:
    """Get detailed information about a specific event.

    Args:
        event_name: The name of the event to get details for.

    Returns:
        str: The detailed description of the event.
    """
    schedule = get_schedule(out_format="dict")
    descriptions = get_descriptions(out_format="dict")

    event = next((event for event in schedule if event.get("title") == event_name), None)
    if not event:
        return json.dumps({"error": "Event not found"}, indent=4)

    event["description"] = descriptions.get(str(event.get("event_id")), "No description available")
    return json.dumps(event, indent=4)


@tool
def get_speaker_bio(speaker_name: str) -> str:
    """Get biography information about a specific speaker.

    Args:
        speaker_name: The name of the speaker to get biography for.

    Returns:
        str: The biography of the speaker if found, or error message if not found.
    """
    speakers = get_speakers(out_format="dict")
    speaker = speakers.get(speaker_name, None)
    if not speaker:
        return json.dumps({"error": "Speaker not found"}, indent=4)
    return json.dumps(speaker, indent=4)



@tool
def list_event_titles() -> str:
    """List all event titles from the PyData schedule. Sorted by starting datetime.

    Returns:
        str: A list of all event titles from the schedule. Sorted by starting datetime.
    """
    schedule = get_schedule(out_format="dict")
    titles = [event["title"] for event in schedule]
    return json.dumps(titles, indent=4)


@tool
def list_events_by_timeframe(start_datetime: str, end_datetime: str) -> str:
    """List event titles that occur within the specified time window.

    Args:
        start_datetime: Start datetime in format YYYY-MM-DDTHH:mm:ss+02:00
        end_datetime: End datetime in format YYYY-MM-DDTHH:mm:ss+02:00

    Returns:
        str: A list of event titles occurring within the specified timeframe
    """
    schedule = get_schedule(out_format="dict")

    filtered_events = [
        event["title"]
        for event in schedule
        if parse_iso(start_datetime) <= parse_iso(event.get("start")) <= parse_iso(end_datetime)
    ]
    return json.dumps(filtered_events, indent=4)


@tool
def get_current_datetime() -> str:
    """Get the current CET date and time.

    Returns:
        str: The current date and time in format YYYY-MM-DD HH:MM:SS
    """
    return current_datetime()

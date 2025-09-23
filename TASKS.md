# Tasks for the workshop

## Part 1: Building and debugging agent
Tasks 1–6 are listed as questions to be answered by the agent in `main.py`.

Tasks:
1. Which talk is first? 
   * Fix the `read_schedule() -> str` tool
3. Which talk is happening right now?
   * Implement the `get_current_datetime() -> str` tool
5. What is the 'Untitled13.ipynb' talk about?
   * Implement the `get_event_details(event_id: str) -> str` tool
7. Which company does the speaker of the current talk work for?
   * Implement the `get_speaker_bio(speaker_name: str) -> str` tool
9. EXTRA: How long until lunch? 
10. EXTRA: Give me the LinkedIn profile of the current speaker.


## Part 2: Optimizing and evaluating agent
Implement Agentic Retrieval.

Instead of `read_schedule() -> str` implement:
* `list_event_names() -> str`
* `get_event_details(event_name: str) -> str`
* `list_events_by_timeframe(start: str, end: str) -> str`

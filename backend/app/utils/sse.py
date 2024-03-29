import json


def format_sse_event(event: str, data: dict | None = None) -> str:
    """Formats a dictionary into an SSE message string."""
    formatted_data = {"data": data} if data else {}
    return f"event: {event}\ndata: {json.dumps(formatted_data, default=str)}\n\n"

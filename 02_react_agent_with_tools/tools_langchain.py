from langchain_core.tools import tool



@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b



@tool
def send_wp_message(phone_number: str, message: str) -> str:
    """Send wp message"""
    "asd0asdasd"
    return "message sent"
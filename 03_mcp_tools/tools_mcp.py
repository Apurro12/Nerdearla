from mcp.server.fastmcp import FastMCP

mcp = FastMCP("calculus_server")

@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b


# Add an addition tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b
#mcp.run(transport="stdio")
mcp.run(transport="streamable-http")
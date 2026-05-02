import logging
import time

from prefab_ui.app import PrefabApp
from prefab_ui.components import Column, Heading, Text, Badge, Row
from fastmcp import FastMCP
from fastmcp.tools import tool

#console logger setup
logger = logging.getLogger("mcp server")
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

class Calculator:
    def __init__(self, multiplier: int):
        self.multiplier = multiplier

    @tool()
    def multiply(self, x: int) -> int:
        """Multiply x by the instance multiplier."""
        return x * self.multiplier

calculator = Calculator(multiplier=3)
mcp = FastMCP(name="My MCP Server")
mcp.add_tool(calculator.multiply)

@mcp.tool(app=True)
def greet(name: str) -> PrefabApp:
    """Greet someone with a visual card."""
    with Column(gap=4, css_class="p-6") as view:
        Heading(f"Hello, {name}!")
        with Row(gap=2, align="center"):
            Text("Status")
            Badge("Greeted", variant="success")

    return PrefabApp(view=view)

@mcp.tool
def add(a:int, b:int) -> PrefabApp:
    """Add two numbers together with a visual card."""
    with Column(gap=4, css_class="p-6") as view:
        Heading(f"The sum of {a} + {b} is {a + b}!")
    return PrefabApp(view=view)

@mcp.tool(
    name="find_products",           # Custom tool name for the LLM
    description="Search the product catalog with optional category filtering.", # Custom description
    tags={"catalog", "search"},      # Optional tags for organization/filtering
    meta={"version": "1.2", "author": "product-team"},  # Custom metadata
    timeout=10
)
def search_products_implementation(query: str, category: str | None = None) -> list[dict]:
    """Internal function description (ignored if description is provided above)."""
    # Implementation...
    logger.info(f"Searching for '{query}' in category '{category}'")
    return [{"id": 2, "name": "Another Product"}]

@mcp.tool(
    name="sleep",
    description="Sleep some 2 seconds and return your number multiplied by 2.",
)
def slow_tool(x: int) -> int:
    """This sync function won't block other concurrent requests."""
    time.sleep(2)  # Runs in threadpool, not on the event loop
    return x * 2

if __name__ == "__main__":
    mcp.run()

# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Setup
uv venv && source .venv/Scripts/activate
uv pip install -e .

# Run MCP server
uv run main.py

# Run all tests
uv run pytest

# Run a single test
uv run pytest tests/test_document.py::TestBinaryDocumentToMarkdown::test_binary_document_to_markdown_with_docx
```

## Architecture

This is a **FastMCP server** that exposes document-processing tools via the Model Context Protocol.

- **`main.py`** — Creates the `FastMCP("docs")` instance and registers tools with `mcp.tool()(fn)`. This is the only place tool registration happens.
- **`tools/`** — One module per tool domain (e.g. `math.py`, `document.py`). Functions here are not automatically exposed — they must be explicitly registered in `main.py`.
- **`tests/fixtures/`** — Binary test files (`.docx`, `.pdf`) used by document tool tests.

## Defining MCP Tools

Register a function as a tool in `main.py`:

```python
from tools.mymodule import my_function
mcp.tool()(my_function)
```

Use `pydantic.Field` for every parameter description:

```python
from pydantic import Field

def my_tool(
    param1: str = Field(description="Detailed description of this parameter"),
    param2: int = Field(description="Explain what this parameter does")
) -> ReturnType:
    """One-line summary.

    Detailed explanation of functionality.
    When to use (and when NOT to use) the tool.

    Examples:
        my_tool("foo", 42) -> expected output
    """
    # implementation
```

Docstrings must include: one-line summary, detailed explanation, when to use/not use, and usage examples with expected input/output.

Always annotate all function parameters and return values with explicit types — FastMCP uses these annotations to generate the tool schema exposed to the MCP client.

## Current State

- `tools/math.py` — `add(a, b)` — registered in `main.py`
- `tools/document.py` — `binary_document_to_markdown(binary_data, file_type)` — **defined but not yet registered**; converts DOCX/PDF bytes to markdown via `markitdown`

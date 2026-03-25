"""
SoloOS V10 — Schema Converter

Transform MCP tool definitions into AI-specific schema formats.

All major LLMs use JSON Schema for parameter definitions.
The difference between OpenAI, Anthropic, and Gemini is only the wrapper.
We convert once from FastMCP's Tool objects and serve any format on demand.

Supported output formats:
  mcp       — MCP protocol standard (default)
  openai    — OpenAI function calling (also: Groq, Together, Mistral, Ollama, LiteLLM)
  anthropic — Anthropic Claude API direct (for agents calling SoloOS programmatically)
  gemini    — Google Gemini function declarations
  langchain — LangChain tool schema (JSON Schema with title/description at top)
"""

from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mcp.types import Tool


# ─────────────────────────────────────────────────────────────
# Schema cleaners
# ─────────────────────────────────────────────────────────────

def _clean_schema(schema: dict) -> dict:
    """
    Remove FastMCP-internal fields that confuse AI models.

    FastMCP generates titles like "get_stage_adviceArguments" — these are
    implementation artifacts, not useful to the LLM. Strip them.
    """
    if not schema:
        return {"type": "object", "properties": {}}

    clean = {}
    for k, v in schema.items():
        if k == "title":
            continue  # Strip top-level title (FastMCP artifact)
        if k == "properties" and isinstance(v, dict):
            # Strip title from each property
            clean_props = {}
            for prop_name, prop_val in v.items():
                if isinstance(prop_val, dict):
                    clean_props[prop_name] = {
                        pk: pv for pk, pv in prop_val.items()
                        if pk != "title"
                    }
                else:
                    clean_props[prop_name] = prop_val
            clean["properties"] = clean_props
        else:
            clean[k] = v

    # Ensure type is set
    if "type" not in clean:
        clean["type"] = "object"
    if "properties" not in clean:
        clean["properties"] = {}

    return clean


# ─────────────────────────────────────────────────────────────
# Format converters
# ─────────────────────────────────────────────────────────────

def to_mcp(tool: "Tool") -> dict:
    """MCP standard tool schema."""
    return {
        "name": tool.name,
        "description": (tool.description or "").strip(),
        "inputSchema": tool.inputSchema or {"type": "object", "properties": {}},
    }


def to_openai(tool: "Tool") -> dict:
    """
    OpenAI function calling format.

    Compatible with: OpenAI, Groq, Together AI, Mistral, Ollama (tools endpoint),
    LiteLLM, Perplexity, Anyscale, Fireworks, and any OpenAI-compatible API.
    """
    return {
        "type": "function",
        "function": {
            "name": tool.name,
            "description": (tool.description or "").strip(),
            "parameters": _clean_schema(tool.inputSchema),
        }
    }


def to_anthropic(tool: "Tool") -> dict:
    """
    Anthropic tools format for direct Claude API use.

    Use this when building agents that call SoloOS as a tool set
    via the Anthropic Python SDK (anthropic.Anthropic().messages.create(..., tools=[...]))
    """
    return {
        "name": tool.name,
        "description": (tool.description or "").strip(),
        "input_schema": _clean_schema(tool.inputSchema),
    }


def to_gemini(tool: "Tool") -> dict:
    """
    Google Gemini function declarations format.

    Compatible with: Gemini API (google-generativeai), Vertex AI,
    Google AI Studio function calling.
    """
    return {
        "name": tool.name,
        "description": (tool.description or "").strip(),
        "parameters": _clean_schema(tool.inputSchema),
    }


def to_langchain(tool: "Tool") -> dict:
    """
    LangChain / LlamaIndex tool schema format.

    Use with: LangChain StructuredTool, LlamaIndex FunctionTool,
    Haystack tools, and similar agent frameworks.
    """
    schema = _clean_schema(tool.inputSchema)
    schema["title"] = tool.name
    schema["description"] = (tool.description or "").strip()
    return {
        "name": tool.name,
        "description": (tool.description or "").strip(),
        "parameters": schema,
    }


# ─────────────────────────────────────────────────────────────
# Batch conversion
# ─────────────────────────────────────────────────────────────

CONVERTERS = {
    "mcp": to_mcp,
    "openai": to_openai,
    "anthropic": to_anthropic,
    "gemini": to_gemini,
    "langchain": to_langchain,
}

SUPPORTED_FORMATS = list(CONVERTERS.keys())


def convert_tools(tools: list["Tool"], format: str = "mcp") -> list[dict]:
    """
    Convert a list of FastMCP Tool objects to the requested schema format.

    Args:
        tools: List of mcp.types.Tool objects from mcp.list_tools()
        format: One of "mcp", "openai", "anthropic", "gemini", "langchain"

    Returns:
        List of dicts in the requested format, ready to pass to any LLM SDK.

    Example (OpenAI):
        tools = await mcp.list_tools()
        openai_tools = convert_tools(tools, "openai")
        client.chat.completions.create(model="gpt-4o", tools=openai_tools, ...)

    Example (Anthropic):
        tools = await mcp.list_tools()
        anthropic_tools = convert_tools(tools, "anthropic")
        client.messages.create(model="claude-opus-4-5", tools=anthropic_tools, ...)
    """
    converter = CONVERTERS.get(format, to_mcp)
    return [converter(t) for t in tools]

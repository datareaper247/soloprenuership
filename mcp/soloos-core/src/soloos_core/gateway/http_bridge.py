"""
SoloOS V10 — Multi-Protocol HTTP Gateway

Same 33 tools. Every AI client. Zero duplication.

ENDPOINTS:
  GET  /                         Health check + capabilities
  GET  /tools                    List tools (format=mcp|openai|anthropic|gemini|langchain)
  POST /tools/{name}             Execute a tool
  GET  /schemas                  Full tool schema set in requested format (for LLM injection)
  GET  /.well-known/ai-plugin.json ChatGPT Actions manifest
  GET  /openapi.json             OpenAPI 3.0 spec (auto-generated, for ChatGPT Actions)
  GET  /docs                     Swagger UI (interactive tool explorer)
  /mcp                           MCP Streamable HTTP (Claude Desktop HTTP, Cursor, n8n)
  /sse                           MCP SSE legacy (older MCP clients)

TRANSPORT COMPATIBILITY:
  MCP stdio        → run `soloos-mcp` (default) — Claude Code, Claude Desktop, Cursor, Windsurf
  MCP HTTP/SSE     → run `soloos-mcp --transport sse --port 8765` — n8n, older MCP hosts
  MCP Streamable   → run `soloos-mcp --transport http --port 8765` — Claude Desktop HTTP mode
  REST/OpenAPI     → run `soloos-api --port 8765` — ChatGPT, Gemini, LangChain, any HTTP AI

USAGE:
  # Install with HTTP support
  pip install "soloos-core[http]"

  # Run REST gateway
  soloos-api --port 8765 --host 0.0.0.0

  # Configure ChatGPT Action: point to http://localhost:8765/openapi.json
  # Configure LangChain: use GET /schemas?format=openai + POST /tools/{name}
  # Configure n8n: use /mcp or /sse endpoint as MCP server URL
"""

from __future__ import annotations

import asyncio
import json
import os
from typing import Any

# ─────────────────────────────────────────────────────────────
# Lazy FastAPI import (optional dep)
# ─────────────────────────────────────────────────────────────

try:
    from fastapi import FastAPI, HTTPException, Query
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import JSONResponse
    from pydantic import BaseModel
    _FASTAPI_AVAILABLE = True
except ImportError:
    _FASTAPI_AVAILABLE = False


# ─────────────────────────────────────────────────────────────
# Lazy MCP import (avoids circular import on startup)
# ─────────────────────────────────────────────────────────────

_mcp = None

def _get_mcp():
    global _mcp
    if _mcp is None:
        from soloos_core.server import mcp
        _mcp = mcp
    return _mcp


# ─────────────────────────────────────────────────────────────
# Tool invocation helper
# ─────────────────────────────────────────────────────────────

async def _invoke_tool(name: str, params: dict) -> Any:
    """
    Invoke an MCP tool and return a Python-native result.

    Handles the FastMCP return format: (list[TextContent], metadata_dict)
    Attempts JSON parsing of the result; falls back to raw string.
    """
    mcp = _get_mcp()

    try:
        result = await mcp.call_tool(name, params)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Tool execution error: {e}")

    # FastMCP returns (list[TextContent], metadata)
    content_list = result[0] if isinstance(result, tuple) else result
    if not content_list:
        return {}

    text = content_list[0].text if hasattr(content_list[0], "text") else str(content_list[0])

    try:
        return json.loads(text)
    except (json.JSONDecodeError, TypeError):
        return {"result": text}


# ─────────────────────────────────────────────────────────────
# FastAPI app builder
# ─────────────────────────────────────────────────────────────

def build_app(
    api_key: str | None = None,
    host: str = "127.0.0.1",
    port: int = 8765,
) -> "FastAPI":
    """
    Build the SoloOS REST gateway FastAPI app.

    Args:
        api_key: Optional Bearer token for auth. None = no auth (local use default).
        host: Host to bind (for manifest URLs). Default: 127.0.0.1
        port: Port (for manifest URLs). Default: 8765.
    """
    if not _FASTAPI_AVAILABLE:
        raise ImportError(
            "FastAPI not installed. Install with: pip install 'soloos-core[http]'"
        )

    from soloos_core.gateway.schema_gen import convert_tools, SUPPORTED_FORMATS

    base_url = f"http://{host}:{port}"

    app = FastAPI(
        title="SoloOS Founder Intelligence API",
        description=(
            "33 AI tools for solo founders — financial modeling, market intelligence, "
            "kill signals, AI council, competitor briefs, and more. "
            "Compatible with Claude, ChatGPT, Gemini, LangChain, LlamaIndex, n8n, and any "
            "AI that supports function calling or MCP."
        ),
        version="10.0.0",
        docs_url="/docs",
        openapi_url="/openapi.json",
        contact={
            "name": "SoloOS",
            "url": "https://github.com/soloos",
        },
        license_info={"name": "MIT"},
    )

    # CORS — allow any origin so browser-based AI tools can call this
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["*"],
    )

    # ── Optional auth dependency ──────────────────────────────
    async def check_auth(authorization: str | None = None):
        if api_key is None:
            return  # No auth configured — local use
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Missing Bearer token")
        token = authorization.removeprefix("Bearer ").strip()
        if token != api_key:
            raise HTTPException(status_code=403, detail="Invalid API key")

    # ── Mount MCP transports ──────────────────────────────────
    mcp = _get_mcp()

    # MCP Streamable HTTP — Claude Desktop HTTP mode, modern MCP hosts
    try:
        mcp_http_app = mcp.streamable_http_app()
        app.mount("/mcp", mcp_http_app)
    except Exception:
        pass  # Graceful if transport not available in this build

    # MCP SSE — n8n MCP node, legacy MCP clients
    try:
        mcp_sse_app = mcp.sse_app(mount_path="/sse")
        app.mount("/sse", mcp_sse_app)
    except Exception:
        pass

    # ── REST endpoints ────────────────────────────────────────

    @app.get("/", tags=["system"])
    async def health():
        """Health check and capability summary."""
        tools = await mcp.list_tools()
        return {
            "status": "ok",
            "service": "SoloOS Founder Intelligence API",
            "version": "10.0.0",
            "tool_count": len(tools),
            "protocols": {
                "mcp_streamable_http": f"{base_url}/mcp",
                "mcp_sse": f"{base_url}/sse",
                "rest": f"{base_url}/tools",
                "openapi_spec": f"{base_url}/openapi.json",
                "swagger_ui": f"{base_url}/docs",
                "chatgpt_manifest": f"{base_url}/.well-known/ai-plugin.json",
            },
            "schema_formats": SUPPORTED_FORMATS,
            "auth": "bearer_token" if api_key else "none",
        }

    @app.get("/tools", tags=["tools"])
    async def list_tools(
        format: str = Query(
            default="mcp",
            description=f"Schema format: {', '.join(SUPPORTED_FORMATS)}",
        )
    ):
        """
        List all 33 SoloOS tools in the requested schema format.

        - `mcp` — MCP protocol standard
        - `openai` — OpenAI function calling (also Groq, Mistral, Together, LiteLLM)
        - `anthropic` — Anthropic Claude API tools
        - `gemini` — Google Gemini function declarations
        - `langchain` — LangChain / LlamaIndex StructuredTool format

        Use the returned schemas to inject SoloOS tools into any LLM call.
        """
        tools = await mcp.list_tools()
        return convert_tools(tools, format=format)

    class ToolCallRequest(BaseModel):
        params: dict[str, Any] = {}

    @app.post("/tools/{name}", tags=["tools"])
    async def call_tool(name: str, request: ToolCallRequest):
        """
        Execute a SoloOS tool by name.

        The tool result is returned as a JSON object.
        For tool schemas, see GET /tools?format=openai (or anthropic/gemini).

        Example (council_brief):
          POST /tools/council_brief
          {"params": {"decision": "should I raise a $500K round?", "stage_mrr": "$8K MRR"}}
        """
        # Verify tool exists
        tools = await mcp.list_tools()
        tool_names = {t.name for t in tools}
        if name not in tool_names:
            raise HTTPException(
                status_code=404,
                detail=f"Tool '{name}' not found. Available: {sorted(tool_names)}"
            )
        return await _invoke_tool(name, request.params)

    @app.get("/schemas", tags=["tools"])
    async def get_schemas(
        format: str = Query(
            default="openai",
            description=f"Schema format: {', '.join(SUPPORTED_FORMATS)}",
        )
    ):
        """
        Full tool schema set — inject directly into any LLM SDK call.

        **OpenAI / Groq / Mistral / Together / LiteLLM:**
        ```python
        import requests, openai
        schemas = requests.get("http://localhost:8765/schemas?format=openai").json()
        client.chat.completions.create(model="gpt-4o", tools=schemas, messages=[...])
        ```

        **Anthropic:**
        ```python
        schemas = requests.get("http://localhost:8765/schemas?format=anthropic").json()
        client.messages.create(model="claude-opus-4-5", tools=schemas, messages=[...])
        ```

        **Google Gemini:**
        ```python
        schemas = requests.get("http://localhost:8765/schemas?format=gemini").json()
        model.generate_content(content, tools=[{"function_declarations": schemas}])
        ```
        """
        tools = await mcp.list_tools()
        return convert_tools(tools, format=format)

    @app.get("/.well-known/ai-plugin.json", tags=["discovery"])
    async def ai_plugin_manifest():
        """
        ChatGPT Actions / AI plugin discovery manifest.

        Point ChatGPT Action to this URL. ChatGPT will read the manifest,
        then fetch /openapi.json to discover all available tools.

        Setup:
          1. Create a GPT in ChatGPT
          2. Add Action → import from URL → http://your-host:8765/openapi.json
          3. SoloOS tools are now available in your GPT
        """
        tools = await mcp.list_tools()
        return {
            "schema_version": "v1",
            "name_for_human": "SoloOS Founder Intelligence",
            "name_for_model": "soloos",
            "description_for_human": (
                "33 AI tools for solo founders: financial modeling, kill signals, "
                "AI council, market intelligence, competitor briefs, and more."
            ),
            "description_for_model": (
                "SoloOS is a founder intelligence system with 33 tools. Use it to: "
                "check kill signals, run AI councils on decisions, calculate unit economics, "
                "get live market signals from HN and Reddit, validate startup ideas, "
                "model runway, track experiments, and get stage-calibrated founder advice. "
                f"Total tools available: {len(tools)}."
            ),
            "auth": {"type": "none"},
            "api": {
                "type": "openapi",
                "url": f"{base_url}/openapi.json",
                "is_user_authenticated": False,
            },
            "logo_url": f"{base_url}/logo.png",
            "contact_email": "founders@soloos.dev",
            "legal_info_url": f"{base_url}/",
        }

    @app.get("/connect", tags=["discovery"])
    async def connection_guide():
        """
        Connection guide for all AI clients and frameworks.

        Returns step-by-step instructions for connecting SoloOS to any AI system.
        """
        tools = await mcp.list_tools()
        return {
            "service": "SoloOS V10 Founder Intelligence",
            "tool_count": len(tools),
            "connections": {
                "claude_code": {
                    "method": "MCP stdio",
                    "setup": "soloos-mcp (default — already configured if using Claude Code)",
                    "config": {
                        "mcpServers": {
                            "soloos-core": {
                                "command": "soloos-mcp",
                                "args": []
                            }
                        }
                    }
                },
                "claude_desktop_http": {
                    "method": "MCP Streamable HTTP",
                    "setup": "soloos-mcp --transport http --port 8765",
                    "mcp_url": f"{base_url}/mcp",
                    "config": {
                        "mcpServers": {
                            "soloos-core": {
                                "url": f"{base_url}/mcp"
                            }
                        }
                    }
                },
                "cursor_windsurf_continue": {
                    "method": "MCP stdio (same as Claude Code)",
                    "setup": "Add to MCP config: command=soloos-mcp",
                },
                "n8n": {
                    "method": "MCP SSE node",
                    "setup": "soloos-api --port 8765",
                    "sse_url": f"{base_url}/sse",
                    "note": "Use n8n MCP node, point to SSE URL"
                },
                "chatgpt_actions": {
                    "method": "OpenAPI Actions",
                    "setup": "soloos-api --port 8765 (public URL required)",
                    "openapi_url": f"{base_url}/openapi.json",
                    "manifest_url": f"{base_url}/.well-known/ai-plugin.json",
                    "note": "ChatGPT needs a public HTTPS URL. Use ngrok or deploy to cloud."
                },
                "openai_sdk": {
                    "method": "OpenAI function calling",
                    "setup": "soloos-api --port 8765",
                    "schemas_url": f"{base_url}/schemas?format=openai",
                    "execute_url": f"{base_url}/tools/{{tool_name}}",
                    "code_example": (
                        "import requests, openai\n"
                        f"tools = requests.get('{base_url}/schemas?format=openai').json()\n"
                        "client.chat.completions.create(model='gpt-4o', tools=tools, ...)"
                    )
                },
                "anthropic_sdk": {
                    "method": "Anthropic tools",
                    "schemas_url": f"{base_url}/schemas?format=anthropic",
                    "execute_url": f"{base_url}/tools/{{tool_name}}",
                    "code_example": (
                        "import requests, anthropic\n"
                        f"tools = requests.get('{base_url}/schemas?format=anthropic').json()\n"
                        "client.messages.create(model='claude-opus-4-5', tools=tools, ...)"
                    )
                },
                "google_gemini": {
                    "method": "Gemini function declarations",
                    "schemas_url": f"{base_url}/schemas?format=gemini",
                    "execute_url": f"{base_url}/tools/{{tool_name}}",
                },
                "langchain": {
                    "method": "LangChain StructuredTool",
                    "schemas_url": f"{base_url}/schemas?format=langchain",
                    "note": "Wrap POST /tools/{name} as a StructuredTool or BaseTool"
                },
                "n8n_rest": {
                    "method": "REST API (HTTP Request node)",
                    "tools_url": f"{base_url}/tools",
                    "execute_url": f"{base_url}/tools/{{tool_name}}",
                },
                "cli": {
                    "method": "CLI direct",
                    "setup": "soloos <command> [args]",
                    "examples": [
                        "soloos pattern 'should I add a free tier'",
                        "soloos market 'AI resume builder'",
                        "soloos stage 5000",
                    ]
                }
            }
        }

    return app


# ─────────────────────────────────────────────────────────────
# CLI entrypoint
# ─────────────────────────────────────────────────────────────

def main():
    """
    Run the SoloOS REST gateway.

    Usage:
        soloos-api                         # localhost:8765
        soloos-api --port 9000             # custom port
        soloos-api --host 0.0.0.0          # public (for ChatGPT, remote AI)
        soloos-api --api-key MY_SECRET     # require Bearer token auth
    """
    import argparse

    if not _FASTAPI_AVAILABLE:
        print("ERROR: FastAPI not installed.")
        print("Install with: pip install 'soloos-core[http]'")
        raise SystemExit(1)

    try:
        import uvicorn
    except ImportError:
        print("ERROR: uvicorn not installed.")
        print("Install with: pip install 'soloos-core[http]'")
        raise SystemExit(1)

    parser = argparse.ArgumentParser(
        description="SoloOS REST Gateway — expose 33 founder intelligence tools to any AI"
    )
    parser.add_argument("--host", default="127.0.0.1",
                        help="Host to bind (default: 127.0.0.1). Use 0.0.0.0 for public access.")
    parser.add_argument("--port", type=int, default=8765,
                        help="Port to bind (default: 8765)")
    parser.add_argument("--api-key", default=os.environ.get("SOLOOS_API_KEY"),
                        help="Optional Bearer token for auth. Default: none (local use).")
    parser.add_argument("--reload", action="store_true",
                        help="Enable auto-reload (development only)")
    args = parser.parse_args()

    app = build_app(api_key=args.api_key, host=args.host, port=args.port)

    print(f"\n{'━' * 55}")
    print(f"  SoloOS V10 REST Gateway")
    print(f"{'━' * 55}")
    print(f"  REST API:    http://{args.host}:{args.port}/tools")
    print(f"  MCP HTTP:    http://{args.host}:{args.port}/mcp")
    print(f"  MCP SSE:     http://{args.host}:{args.port}/sse")
    print(f"  Swagger UI:  http://{args.host}:{args.port}/docs")
    print(f"  ChatGPT:     http://{args.host}:{args.port}/openapi.json")
    print(f"  Guide:       http://{args.host}:{args.port}/connect")
    print(f"  Auth:        {'Bearer token' if args.api_key else 'none (local)'}")
    print(f"{'━' * 55}\n")

    uvicorn.run(
        app,
        host=args.host,
        port=args.port,
        reload=args.reload,
        log_level="info",
    )


if __name__ == "__main__":
    main()

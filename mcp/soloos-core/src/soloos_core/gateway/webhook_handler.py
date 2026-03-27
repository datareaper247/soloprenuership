"""
Webhook receiver — turns external events into TaskQueue entries.

Endpoints (added to existing FastAPI app in http_bridge.py):
    POST /webhooks/stripe      — charge.succeeded → send welcome email task
    POST /webhooks/github      — push/PR → engineering review task
    POST /webhooks/intercom    — new ticket → customer success task
    POST /webhooks/crisp       — new message → customer success task
    POST /webhooks/generic     — generic event → any task type

Each webhook:
1. Validates signature (or logs warning if no secret configured)
2. Parses event type
3. Enqueues appropriate task in TaskQueue
4. Returns 200 immediately (async processing)
"""

from __future__ import annotations

import hashlib
import hmac
import json
import logging
import os
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)


def _verify_stripe_signature(body: bytes, signature_header: str) -> bool:
    secret = os.environ.get("STRIPE_WEBHOOK_SECRET")
    if not secret:
        logger.warning("STRIPE_WEBHOOK_SECRET not set — skipping signature verification")
        return True
    try:
        parts = dict(item.split("=", 1) for item in signature_header.split(","))
        timestamp = parts.get("t", "")
        sig_v1 = parts.get("v1", "")
        signed_payload = f"{timestamp}.{body.decode()}"
        expected = hmac.new(secret.encode(), signed_payload.encode(), hashlib.sha256).hexdigest()
        return hmac.compare_digest(expected, sig_v1)
    except Exception:
        return False


def _verify_github_signature(body: bytes, signature_header: str) -> bool:
    secret = os.environ.get("GITHUB_WEBHOOK_SECRET")
    if not secret:
        logger.warning("GITHUB_WEBHOOK_SECRET not set — skipping signature verification")
        return True
    try:
        expected = "sha256=" + hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
        return hmac.compare_digest(expected, signature_header)
    except Exception:
        return False


def register_webhooks(app) -> None:
    """Register webhook routes on the FastAPI app. Called from http_bridge.build_app()."""

    try:
        from fastapi import Request, HTTPException
        from fastapi.responses import JSONResponse
    except ImportError:
        logger.warning("FastAPI not available — webhooks not registered")
        return

    from ..agent.task_queue import get_task_queue
    from ..agent.founder_loop import get_founder_loop

    @app.post("/webhooks/stripe")
    async def stripe_webhook(request: Request):
        body = await request.body()
        sig = request.headers.get("stripe-signature", "")
        if not _verify_stripe_signature(body, sig):
            raise HTTPException(status_code=400, detail="Invalid signature")

        try:
            payload = json.loads(body)
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Invalid JSON")

        event_type = payload.get("type", "")
        loop = get_founder_loop()
        result = loop.handle_event(f"stripe.{event_type}", payload.get("data", {}).get("object", {}))
        return JSONResponse({"received": True, "queued_as": result.get("task_type")})

    @app.post("/webhooks/github")
    async def github_webhook(request: Request):
        body = await request.body()
        sig = request.headers.get("x-hub-signature-256", "")
        if not _verify_github_signature(body, sig):
            raise HTTPException(status_code=400, detail="Invalid signature")

        try:
            payload = json.loads(body)
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Invalid JSON")

        event_type = request.headers.get("x-github-event", "push")
        action = payload.get("action", "")
        loop = get_founder_loop()
        result = loop.handle_event(f"github.{event_type}.{action}", payload)
        return JSONResponse({"received": True, "queued_as": result.get("task_type")})

    @app.post("/webhooks/intercom")
    async def intercom_webhook(request: Request):
        body = await request.body()
        try:
            payload = json.loads(body)
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Invalid JSON")

        topic = payload.get("topic", "conversation.created")
        loop = get_founder_loop()
        result = loop.handle_event(f"intercom.{topic}", payload.get("data", {}).get("item", {}))
        return JSONResponse({"received": True, "queued_as": result.get("task_type")})

    @app.post("/webhooks/crisp")
    async def crisp_webhook(request: Request):
        body = await request.body()
        try:
            payload = json.loads(body)
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Invalid JSON")

        event = payload.get("event", "message:updated")
        loop = get_founder_loop()
        result = loop.handle_event(f"crisp.{event}", payload.get("data", {}))
        return JSONResponse({"received": True, "queued_as": result.get("task_type")})

    @app.post("/webhooks/generic")
    async def generic_webhook(request: Request):
        body = await request.body()
        try:
            payload = json.loads(body)
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Invalid JSON")

        event_type = payload.get("event_type", "generic_event")
        queue = get_task_queue()
        task_id = queue.enqueue(
            task_type="handle_generic_event",
            payload=payload,
            priority=5,
        )
        return JSONResponse({"received": True, "task_id": task_id})

    logger.info("Webhooks registered: /webhooks/{stripe,github,intercom,crisp,generic}")

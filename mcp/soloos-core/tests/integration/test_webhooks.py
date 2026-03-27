"""Integration tests for webhook endpoints.

Tests the full path:
  HTTP POST → signature verification → TaskQueue entry → response

Uses FastAPI TestClient (httpx) — skip if fastapi/httpx not installed.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import os
import tempfile
import time
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

# ─── Skip guard ───────────────────────────────────────────────────────────────

try:
    from fastapi.testclient import TestClient
    _FASTAPI_OK = True
except ImportError:
    _FASTAPI_OK = False

pytestmark = pytest.mark.skipif(
    not _FASTAPI_OK,
    reason="fastapi + httpx required for webhook integration tests",
)


# ─── Helpers ──────────────────────────────────────────────────────────────────

def _sign_stripe(body: bytes, secret: str) -> str:
    ts = str(int(time.time()))
    sig = hmac.new(secret.encode(), f"{ts}.{body.decode()}".encode(), hashlib.sha256).hexdigest()
    return f"t={ts},v1={sig}"


def _sign_github(body: bytes, secret: str) -> str:
    return "sha256=" + hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()


def _sign_intercom(body: bytes, secret: str) -> str:
    return "sha1=" + hmac.new(secret.encode(), body, hashlib.sha1).hexdigest()


def _sign_crisp(body: bytes, secret: str) -> str:
    return hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()


def _sign_generic(body: bytes, secret: str) -> str:
    return "sha256=" + hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()


def _make_app(monkeypatch, tmp_db: Path):
    """Build a test FastAPI app with webhooks registered and a real TaskQueue."""
    from soloos_core.gateway.http_bridge import build_app
    from soloos_core.agent.task_queue import TaskQueue
    from soloos_core.agent.founder_loop import FounderLoop

    # Isolated queue
    queue = TaskQueue(db_path=tmp_db)

    # Stub FounderLoop.handle_event to avoid pulling in executor/world model
    mock_loop = MagicMock(spec=FounderLoop)
    mock_loop.handle_event.side_effect = lambda event_type, payload: {
        "status": "queued",
        "task_id": "test-task-id",
        "task_type": "test_task",
    }

    monkeypatch.setattr(
        "soloos_core.gateway.webhook_handler.get_task_queue",
        lambda: queue,
    )
    monkeypatch.setattr(
        "soloos_core.gateway.webhook_handler.get_founder_loop",
        lambda: mock_loop,
    )

    app = build_app(api_key=None, host="127.0.0.1", port=8765)
    return app, queue, mock_loop


# ─── Stripe ───────────────────────────────────────────────────────────────────

def test_stripe_webhook_valid_signature(monkeypatch, tmp_path):
    secret = "whsec_test_stripe"
    monkeypatch.setenv("STRIPE_WEBHOOK_SECRET", secret)
    app, queue, mock_loop = _make_app(monkeypatch, tmp_path / "q.db")
    client = TestClient(app, raise_server_exceptions=True)

    body = json.dumps({"type": "charge.succeeded", "data": {"object": {"id": "ch_123"}}}).encode()
    sig = _sign_stripe(body, secret)

    resp = client.post("/webhooks/stripe", content=body, headers={"stripe-signature": sig})
    assert resp.status_code == 200
    mock_loop.handle_event.assert_called_once()
    event_arg = mock_loop.handle_event.call_args[0][0]
    assert event_arg == "stripe.charge.succeeded"


def test_stripe_webhook_missing_signature(monkeypatch, tmp_path):
    monkeypatch.setenv("STRIPE_WEBHOOK_SECRET", "secret")
    app, *_ = _make_app(monkeypatch, tmp_path / "q.db")
    client = TestClient(app, raise_server_exceptions=False)

    body = json.dumps({"type": "charge.succeeded"}).encode()
    resp = client.post("/webhooks/stripe", content=body)
    assert resp.status_code == 403


def test_stripe_webhook_no_secret_configured(monkeypatch, tmp_path):
    monkeypatch.delenv("STRIPE_WEBHOOK_SECRET", raising=False)
    app, *_ = _make_app(monkeypatch, tmp_path / "q.db")
    client = TestClient(app, raise_server_exceptions=False)

    body = json.dumps({"type": "charge.succeeded"}).encode()
    resp = client.post("/webhooks/stripe", content=body, headers={"stripe-signature": "t=1,v1=bad"})
    assert resp.status_code == 403


def test_stripe_webhook_wrong_signature(monkeypatch, tmp_path):
    monkeypatch.setenv("STRIPE_WEBHOOK_SECRET", "correct_secret")
    app, *_ = _make_app(monkeypatch, tmp_path / "q.db")
    client = TestClient(app, raise_server_exceptions=False)

    body = json.dumps({"type": "charge.succeeded"}).encode()
    bad_sig = _sign_stripe(body, "wrong_secret")
    resp = client.post("/webhooks/stripe", content=body, headers={"stripe-signature": bad_sig})
    assert resp.status_code == 403


# ─── GitHub ───────────────────────────────────────────────────────────────────

def test_github_webhook_valid_signature(monkeypatch, tmp_path):
    secret = "gh_test_secret"
    monkeypatch.setenv("GITHUB_WEBHOOK_SECRET", secret)
    app, queue, mock_loop = _make_app(monkeypatch, tmp_path / "q.db")
    client = TestClient(app, raise_server_exceptions=True)

    body = json.dumps({"action": "opened", "number": 42}).encode()
    sig = _sign_github(body, secret)

    resp = client.post(
        "/webhooks/github",
        content=body,
        headers={"x-hub-signature-256": sig, "x-github-event": "pull_request"},
    )
    assert resp.status_code == 200
    mock_loop.handle_event.assert_called_once()


def test_github_webhook_no_secret_returns_403(monkeypatch, tmp_path):
    monkeypatch.delenv("GITHUB_WEBHOOK_SECRET", raising=False)
    app, *_ = _make_app(monkeypatch, tmp_path / "q.db")
    client = TestClient(app, raise_server_exceptions=False)

    body = b'{"action": "opened"}'
    resp = client.post("/webhooks/github", content=body, headers={"x-hub-signature-256": "sha256=bad"})
    assert resp.status_code == 403


# ─── Generic ──────────────────────────────────────────────────────────────────

def test_generic_webhook_valid_signature(monkeypatch, tmp_path):
    secret = "generic_secret"
    monkeypatch.setenv("GENERIC_WEBHOOK_SECRET", secret)
    app, queue, _ = _make_app(monkeypatch, tmp_path / "q.db")
    client = TestClient(app, raise_server_exceptions=True)

    body = json.dumps({"event_type": "custom_event", "data": {"foo": "bar"}}).encode()
    sig = _sign_generic(body, secret)

    resp = client.post("/webhooks/generic", content=body, headers={"x-webhook-signature": sig})
    assert resp.status_code == 200
    data = resp.json()
    assert data["received"] is True
    assert "task_id" in data


def test_generic_webhook_no_secret_returns_403(monkeypatch, tmp_path):
    monkeypatch.delenv("GENERIC_WEBHOOK_SECRET", raising=False)
    app, *_ = _make_app(monkeypatch, tmp_path / "q.db")
    client = TestClient(app, raise_server_exceptions=False)

    body = b'{"event_type": "test"}'
    resp = client.post("/webhooks/generic", content=body, headers={"x-webhook-signature": "sha256=bad"})
    assert resp.status_code == 403


def test_generic_webhook_invalid_json_returns_400(monkeypatch, tmp_path):
    secret = "generic_secret"
    monkeypatch.setenv("GENERIC_WEBHOOK_SECRET", secret)
    app, *_ = _make_app(monkeypatch, tmp_path / "q.db")
    client = TestClient(app, raise_server_exceptions=False)

    body = b"not json"
    sig = _sign_generic(body, secret)
    resp = client.post("/webhooks/generic", content=body, headers={"x-webhook-signature": sig})
    assert resp.status_code == 400


# ─── Crisp ────────────────────────────────────────────────────────────────────

def test_crisp_webhook_valid_signature(monkeypatch, tmp_path):
    secret = "crisp_secret"
    monkeypatch.setenv("CRISP_WEBHOOK_SECRET", secret)
    app, queue, mock_loop = _make_app(monkeypatch, tmp_path / "q.db")
    client = TestClient(app, raise_server_exceptions=True)

    body = json.dumps({"event": "message:updated", "data": {"session_id": "sess_1"}}).encode()
    sig = _sign_crisp(body, secret)

    resp = client.post("/webhooks/crisp", content=body, headers={"x-crisp-hmac-sha256": sig})
    assert resp.status_code == 200
    mock_loop.handle_event.assert_called_once()


def test_crisp_webhook_no_secret_returns_403(monkeypatch, tmp_path):
    monkeypatch.delenv("CRISP_WEBHOOK_SECRET", raising=False)
    app, *_ = _make_app(monkeypatch, tmp_path / "q.db")
    client = TestClient(app, raise_server_exceptions=False)

    body = b'{"event": "message:updated"}'
    resp = client.post("/webhooks/crisp", content=body, headers={"x-crisp-hmac-sha256": "bad"})
    assert resp.status_code == 403


# ─── Intercom ─────────────────────────────────────────────────────────────────

def test_intercom_webhook_valid_signature(monkeypatch, tmp_path):
    secret = "intercom_secret"
    monkeypatch.setenv("INTERCOM_WEBHOOK_SECRET", secret)
    app, queue, mock_loop = _make_app(monkeypatch, tmp_path / "q.db")
    client = TestClient(app, raise_server_exceptions=True)

    body = json.dumps({"topic": "conversation.created", "data": {"item": {"id": "conv_1"}}}).encode()
    sig = _sign_intercom(body, secret)

    resp = client.post("/webhooks/intercom", content=body, headers={"x-hub-signature": sig})
    assert resp.status_code == 200
    mock_loop.handle_event.assert_called_once()


def test_intercom_webhook_no_secret_returns_403(monkeypatch, tmp_path):
    monkeypatch.delenv("INTERCOM_WEBHOOK_SECRET", raising=False)
    app, *_ = _make_app(monkeypatch, tmp_path / "q.db")
    client = TestClient(app, raise_server_exceptions=False)

    body = b'{"topic": "conversation.created"}'
    resp = client.post("/webhooks/intercom", content=body, headers={"x-hub-signature": "sha1=bad"})
    assert resp.status_code == 403

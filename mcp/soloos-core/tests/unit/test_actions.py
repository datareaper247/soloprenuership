"""Tests for autonomous action implementations."""

import os
from unittest.mock import patch, MagicMock

from soloos_core.actions.base_action import ActionOutcome
from soloos_core.actions.email_action import EmailAction
from soloos_core.actions.deploy_action import DeployAction
from soloos_core.actions.social_action import SocialAction
from soloos_core.actions.support_action import SupportAction
from soloos_core.actions.dns_action import DnsAction


# ─── Fail-open when SDK missing ───────────────────────────────────────────────

def test_email_fails_open_when_resend_missing():
    with patch.dict(os.environ, {"RESEND_API_KEY": "test_key"}):
        action = EmailAction()
        with patch.dict("sys.modules", {"resend": None}):
            result = action.execute({"to": "a@b.com", "subject": "hi", "body": "hello"})
            # Should not raise, should return ActionOutcome with error
            assert isinstance(result, ActionOutcome)
            assert not result.success


def test_all_actions_fail_open_when_unconfigured():
    """All actions return ActionOutcome (not raise) when not configured."""
    clean_env = {k: v for k, v in os.environ.items()
                 if k not in ("RESEND_API_KEY", "VERCEL_TOKEN", "VERCEL_PROJECT_ID",
                              "RAILWAY_TOKEN", "RAILWAY_PROJECT_ID",
                              "TWITTER_API_KEY", "BUFFER_TOKEN",
                              "INTERCOM_TOKEN", "CRISP_WEBSITE_ID",
                              "CLOUDFLARE_TOKEN", "CLOUDFLARE_ZONE_ID")}

    with patch.dict(os.environ, clean_env, clear=True):
        for action, params in [
            (EmailAction(), {"to": "a@b.com", "subject": "hi", "body": "hello"}),
            (DeployAction(), {"target": "staging"}),
            (SocialAction(), {"content": "hello world"}),
            (SupportAction(), {"conversation_id": "123", "message": "hello"}),
            (DnsAction(), {"type": "A", "name": "api", "content": "1.2.3.4"}),
        ]:
            result = action.execute(params)
            assert isinstance(result, ActionOutcome), f"{action.action_name} did not return ActionOutcome"
            assert not result.success
            assert result.error


def test_all_actions_is_configured_returns_false_when_no_env():
    """is_configured() returns False when required env vars absent."""
    clean_env = {k: v for k, v in os.environ.items()
                 if k not in ("RESEND_API_KEY", "VERCEL_TOKEN", "VERCEL_PROJECT_ID",
                              "RAILWAY_TOKEN", "RAILWAY_PROJECT_ID",
                              "TWITTER_API_KEY", "BUFFER_TOKEN",
                              "INTERCOM_TOKEN", "CRISP_WEBSITE_ID",
                              "CLOUDFLARE_TOKEN", "CLOUDFLARE_ZONE_ID")}
    with patch.dict(os.environ, clean_env, clear=True):
        assert not EmailAction().is_configured()
        assert not DeployAction().is_configured()
        assert not SocialAction().is_configured()
        assert not SupportAction().is_configured()
        assert not DnsAction().is_configured()


# ─── EmailAction param validation ────────────────────────────────────────────

def test_email_validates_required_params():
    action = EmailAction()
    assert action.validate_params({}) is not None
    assert action.validate_params({"to": "a@b.com"}) is not None
    assert action.validate_params({"to": "a@b.com", "subject": "hi"}) is not None
    assert action.validate_params({"to": "a@b.com", "subject": "hi", "body": "test"}) is None


# ─── DeployAction tier logic ──────────────────────────────────────────────────

def test_deploy_validates_target():
    action = DeployAction()
    assert action.validate_params({}) is not None
    assert action.validate_params({"target": "invalid"}) is not None
    assert action.validate_params({"target": "staging"}) is None
    assert action.validate_params({"target": "production"}) is None


def test_deploy_staging_param_valid():
    action = DeployAction()
    err = action.validate_params({"target": "staging", "provider": "vercel"})
    assert err is None


def test_deploy_production_param_valid():
    action = DeployAction()
    err = action.validate_params({"target": "production", "provider": "vercel"})
    assert err is None


# ─── SocialAction validation ──────────────────────────────────────────────────

def test_social_validates_content():
    action = SocialAction()
    assert action.validate_params({}) is not None
    assert action.validate_params({"content": "hello"}) is None


def test_social_twitter_280_char_limit():
    action = SocialAction()
    long_content = "x" * 281
    err = action.validate_params({"content": long_content, "platform": "twitter"})
    assert err is not None


# ─── SupportAction validation ─────────────────────────────────────────────────

def test_support_validates_required_params():
    action = SupportAction()
    assert action.validate_params({}) is not None
    assert action.validate_params({"conversation_id": "123"}) is not None
    assert action.validate_params({"conversation_id": "123", "message": "hi"}) is None


# ─── DnsAction validation ─────────────────────────────────────────────────────

def test_dns_validates_type():
    action = DnsAction()
    assert action.validate_params({"name": "x", "content": "1.2.3.4"}) is not None
    assert action.validate_params({"type": "INVALID", "name": "x", "content": "y"}) is not None
    assert action.validate_params({"type": "A", "name": "x", "content": "1.2.3.4"}) is None
    assert action.validate_params({"type": "CNAME", "name": "x", "content": "example.com"}) is None
    assert action.validate_params({"type": "TXT", "name": "@", "content": "v=spf1"}) is None

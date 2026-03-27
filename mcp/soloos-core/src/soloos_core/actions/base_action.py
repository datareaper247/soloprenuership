"""Base class for all autonomous actions."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class ActionOutcome:
    success: bool
    data: dict
    error: str | None = None


class BaseAction(ABC):
    """All actions implement this interface."""
    action_name: str

    @abstractmethod
    def is_configured(self) -> bool:
        """True if required env vars/SDKs are present."""

    @abstractmethod
    def execute(self, params: dict) -> ActionOutcome:
        """Execute the action. MUST fail open — never raise."""

    def validate_params(self, params: dict) -> str | None:
        """Return error string or None if valid."""
        return None

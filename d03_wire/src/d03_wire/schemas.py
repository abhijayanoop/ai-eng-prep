from dataclasses import dataclass, field
from typing import Any, Literal


@dataclass
class ToolCall:
    id: str
    name: str
    arguments: dict[str, Any]


@dataclass
class Response:
    text: str = ""
    tool_calls: list[ToolCall] = field(default_factory=list)
    status: Literal[
        "completed",
        "max_tokens",
        "tool_call",
        "filtered",
        "unknown",
    ] = "unknown"
    provider_stop_reason: str | None = None
    input_tokens: int | None = None
    output_tokens: int | None = None
    raw_response: dict[str, Any] | None = None
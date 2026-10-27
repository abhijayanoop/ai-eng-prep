import json
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class WeatherArgs(BaseModel):
    model_config = ConfigDict(extra="forbid")

    city: str = Field(min_length=1, max_length=100)


def get_weather(city: str) -> dict[str, Any]:
    """Return deterministic fake weather; this does not call a weather API."""
    demo_data = {
        "kochi": {"temperature_c": 29, "condition": "humid"},
        "london": {"temperature_c": 14, "condition": "cloudy"},
        "tokyo": {"temperature_c": 21, "condition": "clear"},
    }
    weather = demo_data.get(
        city.strip().lower(),
        {"temperature_c": 25, "condition": "unknown"},
    )
    return {"city": city, **weather, "source": "simulated"}


def dispatch_tool(name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    """Execute only explicitly allowlisted tools with validated arguments."""
    if name != "get_weather":
        raise ValueError(f"Unknown tool: {name}")

    validated = WeatherArgs.model_validate(arguments)
    return get_weather(validated.city)


def tool_result_json(result: dict[str, Any]) -> str:
    return json.dumps(result, ensure_ascii=False)
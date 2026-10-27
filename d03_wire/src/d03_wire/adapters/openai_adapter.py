import httpx
import json
from typing import Any
from d03_wire.schemas import Response

def openai_parse_tools(tools: list[dict[str, Any]]) -> list[dict[str, Any]]:
    converted = []
    for tool in tools:
        converted.append({
            "type": "function",
            "function": {
                "name": tool["name"],
                "description": tool["description"],
                "parameters": tool["parameters"],
            },
        })

    return converted

def parse_openai_response(data: dict[str, Any]) -> Response:
    
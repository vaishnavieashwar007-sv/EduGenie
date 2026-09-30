import json
import re

from typing import Any


def clean_json_block(
    text: str
) -> str:

    cleaned = text.strip()

    # Remove Markdown JSON fences
    cleaned = re.sub(
        r"^```(?:json)?\s*",
        "",
        cleaned,
        flags=re.IGNORECASE
    )

    cleaned = re.sub(
        r"\s*```$",
        "",
        cleaned
    )

    # Find JSON object/array
    first_object = cleaned.find("{")
    first_array = cleaned.find("[")

    starts = [
        position
        for position in (
            first_object,
            first_array
        )
        if position >= 0
    ]

    if starts:

        start = min(starts)

        end_object = cleaned.rfind("}")
        end_array = cleaned.rfind("]")

        end = max(
            end_object,
            end_array
        )

        if end >= start:

            cleaned = cleaned[
                start:end + 1
            ]

    return cleaned.strip()


def parse_json_response(
    text: str
) -> Any:

    cleaned = clean_json_block(
        text
    )

    return json.loads(
        cleaned
    )
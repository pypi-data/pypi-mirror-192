import sys
from typing import Any, Dict

from PyInquirer import prompt


def prompt_for_values(vars: Dict[str, Dict]) -> Dict[str, Any]:
    questions = []

    assert vars is not None, "Must provide dict of environment variables to prompt"

    hidden_defaults = {}
    for k, v in vars.items():
        if v.get("hidden", False):
            hidden_defaults[k] = v.get("default")
            continue

        def validate(value):
            if bool(value):
                return True

            return "Missing required value"

        question = {
            "name": k,
            "type": v.get("type", "input"),
            "message": v.get("prompt", k),
            "default": v.get("default", ""),
            "validate": validate if v.get("required") else None,
        }
        if (
            v.get("type", "input") == "list"
            or v.get("type", "input") == "rawlist"
            or v.get("type", "input") == "checkbox"
        ):
            question.update(
                {
                    "choices": v.get("choices"),
                }
            )
        questions.append(question)
    values = prompt(questions)

    if not values:
        sys.exit()

    return {**values, **hidden_defaults}

from typing import Any
from collections.abc import Generator


__all__ = [
    "SUPPORTED_TRUE_SYMBOLS",
    "SUPPORTED_FALSE_SYMBOLS",
    "to_boolean",
    "TSupportedTypes",
]

# I'm perhaps pushing at little bit here, but just for the sake of completness,
# I included a whole plethora of symbols that could be parsed as True of False.
SUPPORTED_TRUE_SYMBOLS = [
    True,
    "true",
    "verdadeiro",
    "wahr",
    "1",
    "1.0",
    "y",
    "yes",
    "ja",
]

SUPPORTED_FALSE_SYMBOLS = [
    False,
    "false",
    "falso",
    "falsch",
    "0",
    "0.0",
    "n",
    "no",
    "nein",
]


type TSupportedTypes = bool | str | float | int | None


def to_boolean(value: TSupportedTypes) -> bool | None:
    """Check if the incoming value is parseable as a boolean. If so, returns its parsed form."""

    value_type = type(value).__name__

    def check_inclusion(v: TSupportedTypes) -> bool | None:
        if v in SUPPORTED_TRUE_SYMBOLS:
            return True

        if v in SUPPORTED_FALSE_SYMBOLS:
            return False

        return None

    match value_type:
        case "bool":
            return bool(value)
        case "str":
            return check_inclusion(str(value).strip().lower())
        case "int", "float", "bigint":
            return check_inclusion(value)
        case _, "NoneType":
            return None

    return None


def is_generator_empty(generator: Generator) -> tuple[Generator, bool]:
    """Check if generator is empty without consuming any elements from it."""

    try:
        item = next(generator)

        def my_generator():
            yield item
            yield from generator

        return my_generator(), False
    except StopIteration:
        return (_ for _ in []), True


def filter_dict_by_key(json_object: dict[str, Any], target_key: str):
    """Filter recursively a JSON by a given key."""

    if isinstance(json_object, dict):
        for key, value in json_object.items():
            if key == target_key:
                yield value

            yield from filter_dict_by_key(value, target_key)
    elif isinstance(json_object, list):
        for item in json_object:
            yield from filter_dict_by_key(item, target_key)

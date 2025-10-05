from typing import cast

import pytest
from loguru import logger

from src.common.utils.parsing import (
    to_boolean,
    SUPPORTED_FALSE_SYMBOLS,
    SUPPORTED_TRUE_SYMBOLS,
    TSupportedTypes,
)


def build_test_cases(generate_truthy_tc: bool) -> list[tuple[TSupportedTypes, bool]]:
    """Create the space of test cases for each category of symbols."""

    if generate_truthy_tc:
        return [(cast(TSupportedTypes, item), True) for item in SUPPORTED_TRUE_SYMBOLS]

    return [(cast(TSupportedTypes, item), False) for item in SUPPORTED_FALSE_SYMBOLS]


def perform_assertion(
    value: TSupportedTypes, expected: bool | None, debug: bool = False
) -> None:
    """Help make basic assertion."""
    result = to_boolean(value)

    if debug:
        logger.warning(
            f"\tValue: {value}\tType: {type(value).__name__}\tResult: {result}\tExpected: {expected}"
        )
    else:
        assert result == expected, f"Parsing of '{value}' was not possible."


@pytest.mark.parametrize(
    "value, expected",
    build_test_cases(True),
)
def test_to_boolean_success_truthy_symbols(
    value: TSupportedTypes, expected: bool | None
) -> None:
    """Check if the predefined truthy symbols are being parsed successfully."""
    perform_assertion(value, expected)


@pytest.mark.parametrize(
    "value, expected",
    build_test_cases(False),
)
def test_to_boolean_success_falsy_symbols(
    value: TSupportedTypes, expected: bool | None
) -> None:
    """Check if the predefined falsy symbols are being parsed successfully."""
    perform_assertion(value, expected)


@pytest.mark.parametrize(
    "value, expected",
    [
        ({}, None),
        ([], None),
        (lambda x: x, None),
        (logger, None),
        ("this is not parseable", None),
        (Exception("an error object"), None),
    ],
)
def test_to_boolean_failure_unparseable_symbols(
    value: TSupportedTypes, expected: bool | None
) -> None:
    """Check if the predefined unparseable symbols will be mapped to None."""
    perform_assertion(value, expected)

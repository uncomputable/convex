# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=no-value-for-parameter

import os
from typing import List
from hypothesis import given, settings, strategies as st, HealthCheck

import convex

settings.register_profile(
    "ci",
    max_examples=1000,
    deadline=1000,
    suppress_health_check=[HealthCheck.too_slow],
    derandomize=True
)
settings.register_profile(
    "dev",
    max_examples=2000,
    deadline=None
)
PROFILE = os.getenv("HYPOTHESIS_PROFILE", "dev")
settings.load_profile(PROFILE)


@given(st.text())
def fuzz_parse_any_string(input_string: str):
    convex.parse_string(input_string)


@given(st.text())
def fuzz_parse_any_c(input_string: str):
    convex.parse_c(input_string)


@given(st.text())
def fuzz_parse_any_coq(input_string: str):
    convex.parse_coq(input_string)


@given(st.text())
def fuzz_parse_any_rust(input_string: str):
    convex.parse_rust(input_string)


@given(st.text())
def fuzz_parse_any_json(input_string: str):
    convex.parse_json(input_string)


@given(st.from_regex(convex.STRING_HEX, fullmatch=True))
def fuzz_parse_valid_string(input_string: str):
    assert convex.parse_string(input_string) is not None


@given(st.from_regex(convex.C_HEX, fullmatch=True))
def fuzz_parse_valid_c(input_string: str):
    assert convex.parse_c(input_string) is not None


@given(st.from_regex(convex.COQ_HEX, fullmatch=True))
def fuzz_parse_valid_coq(input_string: str):
    assert convex.parse_coq(input_string) is not None


@given(st.from_regex(convex.RUST_HEX, fullmatch=True))
def fuzz_parse_valid_rust(input_string: str):
    assert convex.parse_rust(input_string) is not None


@given(st.from_regex(convex.JSON_HEX, fullmatch=True))
def fuzz_parse_valid_json(input_string: str):
    assert convex.parse_json(input_string) is not None


@given(st.lists(st.integers(min_value=0, max_value=255)))
def fuzz_format_string_is_valid(lst: List[int]):
    assert convex.is_string(convex.clean(convex.format_string(lst)))


FOUR_INTS = st.lists(st.integers(min_value=0, max_value=255), min_size=4, max_size=4)
LISTS_OF_FOUR_INTS = st.lists(FOUR_INTS) \
    .flatmap(lambda x: st.just([item for sublist in x for item in sublist]))

@given(LISTS_OF_FOUR_INTS)
def fuzz_format_c_is_valid(lst: List[int]):
    assert convex.is_c(convex.clean(convex.format_c(lst)))


@given(st.lists(st.integers(min_value=0, max_value=255)))
def fuzz_format_coq_is_valid(lst: List[int]):
    assert convex.is_coq(convex.clean(convex.format_coq(lst)))


@given(st.lists(st.integers(min_value=0, max_value=255)))
def fuzz_format_rust_is_valid(lst: List[int]):
    assert convex.is_rust(convex.clean(convex.format_rust(lst)))


@given(st.lists(st.integers(min_value=0, max_value=255)))
def fuzz_format_json_is_valid(lst: List[int]):
    assert convex.is_json(convex.clean(convex.format_json(lst)))


if __name__ == "__main__":
    print(settings())

    fuzz_parse_any_string()
    fuzz_parse_any_c()
    fuzz_parse_any_coq()
    fuzz_parse_any_rust()
    fuzz_parse_any_json()

    fuzz_parse_valid_string()
    fuzz_parse_valid_c()
    fuzz_parse_valid_coq()
    fuzz_parse_valid_rust()
    fuzz_parse_valid_json()

    fuzz_format_string_is_valid()
    fuzz_format_c_is_valid()
    fuzz_format_coq_is_valid()
    fuzz_format_rust_is_valid()
    fuzz_format_json_is_valid()

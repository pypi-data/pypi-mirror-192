from __future__ import annotations

from arrow import Arrow
from delta_calculation import Age, calculate_delta
from input_conversion import convert_inputs_to_dates


def calculate_age(birthday_input: Arrow | str, date_to_compare_to_input: Arrow | str | None = None) -> Age:
    birthday, comparison_date = convert_inputs_to_dates(birthday_input, date_to_compare_to_input)

    return calculate_delta(birthday, comparison_date)

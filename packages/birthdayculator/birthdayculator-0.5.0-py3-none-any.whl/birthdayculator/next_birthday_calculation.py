from __future__ import annotations

from datetime import date
from functools import lru_cache

from arrow import Arrow
from input_conversion import convert_inputs_to_dates


def __calculate_birthday_on_comparison_date_year(birthday: Arrow, comparison_date: Arrow) -> Arrow:
    try:
        return birthday.replace(year=comparison_date.year)
    except ValueError:
        return birthday.replace(year=comparison_date.year, day=birthday.day - 1)


@lru_cache(maxsize=100)
def calculate_next_birthday(birthday_input: Arrow | str, date_to_compare_to_input: Arrow | str | None = None) -> date:
    birthday, comparison_date = convert_inputs_to_dates(birthday_input, date_to_compare_to_input)

    birthday_on_comparison_date_year = __calculate_birthday_on_comparison_date_year(birthday, comparison_date)

    return (
        birthday_on_comparison_date_year.replace(year=birthday_on_comparison_date_year.year + 1)
        if birthday_on_comparison_date_year <= comparison_date
        else birthday_on_comparison_date_year
    ).date()

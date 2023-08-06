from __future__ import annotations

from datetime import tzinfo
from functools import lru_cache
from typing import Tuple

from arrow import Arrow, get


def __calculate_comparison_date(date_to_compare_to_input: Arrow | str | None, tzinfo: tzinfo) -> Arrow:
    return get(tzinfo=tzinfo) if date_to_compare_to_input is None else get(date_to_compare_to_input)


@lru_cache(maxsize=100)
def convert_inputs_to_dates(
    birthday_input: Arrow | str,
    date_to_compare_to_input: Arrow | str | None = None,
) -> Tuple[Arrow, Arrow]:
    birthday = get(birthday_input)
    comparison_date = __calculate_comparison_date(date_to_compare_to_input, birthday.tzinfo)

    return birthday, comparison_date

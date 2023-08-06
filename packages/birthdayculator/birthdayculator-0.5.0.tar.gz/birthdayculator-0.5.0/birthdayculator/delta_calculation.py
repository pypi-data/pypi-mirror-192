from dataclasses import dataclass
from typing import Tuple

from arrow import Arrow
from dateutil.relativedelta import relativedelta
from typing_extensions import Self

DAYS_IN_WEEK = 7


@dataclass(frozen=True)
class Age:
    years: int
    months: int
    weeks: int
    days: int

    def __neg__(self) -> Self:
        return Age(years=self.years * -1, months=self.months * -1, weeks=self.weeks * -1, days=self.days * -1)


def __calculate_unit(first: Arrow, second: Arrow, unit: str) -> Tuple[int, Arrow]:
    total_of_unit_naive: int = getattr(relativedelta(second.date(), first.date()), unit)

    first_adjusted_naive = first + relativedelta(**{unit: total_of_unit_naive})

    total_of_unit = total_of_unit_naive if first_adjusted_naive <= second else total_of_unit_naive - 1

    return total_of_unit, first + relativedelta(**{unit: total_of_unit})


def __calculate_weeks_and_days(days: int) -> Tuple[int, int]:
    return days // DAYS_IN_WEEK, days % DAYS_IN_WEEK


def __calculate_delta(first: Arrow, second: Arrow) -> Age:
    years, first_adjusted_with_years = __calculate_unit(first, second, "years")
    months, first_adjusted_with_months = __calculate_unit(first_adjusted_with_years, second, "months")
    total_days, _ = __calculate_unit(first_adjusted_with_months, second, "days")
    weeks, days = __calculate_weeks_and_days(total_days)

    return Age(years=years, months=months, weeks=weeks, days=days)


def calculate_delta(first: Arrow, second: Arrow) -> Age:
    if first <= second:
        return __calculate_delta(first, second)

    return -__calculate_delta(second, first)

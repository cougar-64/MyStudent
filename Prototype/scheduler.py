from datetime import date, timedelta
from models import Assignment, Block, DaySchedule, Semester

MIN_SESSION = 0.5    # minimum hours worth scheduling in a single block
MAX_SINGLE_DAY = 3.0 # max hours of one assignment in a single day


def generate_daily_hours(semester: Semester) -> dict[date, float]:
    """
    Auto-generate a daily_hours dict for every weekday in the semester,
    based on each course's weekly_hours divided across 5 weekdays.
    """
    total_weekly_hours = sum(c.weekly_hours for c in semester.courses)
    hours_per_weekday = total_weekly_hours / 5

    daily = {}
    current = semester.start_date
    while current <= semester.end_date:
        if current.weekday() < 5:  # 0-4 = Monday-Friday, 5-6 = weekend
            daily[current] = round(hours_per_weekday, 2)
        current += timedelta(days=1)

    return daily


def build_schedule(
    assignments: list[Assignment],
    daily_hours: dict[date, float],
) -> list[DaySchedule]:
    """
    Distribute assignment work across available days using back-loaded
    weighting — lighter sessions early, heavier sessions closer to due date.

    Args:
        assignments:  All assignments to schedule.
        daily_hours:  A dict mapping each date to how many free hours you have.

    Returns:
        A list of DaySchedule objects, one per date in daily_hours, in order.
    """
    today = min(daily_hours.keys())

    # --- 1. Filter and sort assignments ---------------------------------
    # Drop anything already overdue — can't schedule the past.
    active = [a for a in assignments if not a.is_overdue(today)]

    # Sort by urgency: days remaining is the dominant factor,
    # priority nudges the score slightly (0.5 weight so it doesn't overpower)
    def urgency(a: Assignment) -> float:
        days_left = a.days_until_due(today)
        return days_left - (a.priority * 0.5)

    active.sort(key=urgency)

    # --- 2. Build empty day slots ---------------------------------------
    sorted_dates = sorted(daily_hours.keys())
    days: dict[date, DaySchedule] = {
        d: DaySchedule(date=d, available_hours=daily_hours[d])
        for d in sorted_dates
    }

    # --- 3. Spread each assignment's hours across available days --------
    for assignment in active:
        hours_left = assignment.est_hours

        # Only schedule on days on or before the due date
        eligible_days = [
            d for d in sorted_dates
            if d <= assignment.due_date and days[d].hours_remaining > 0
        ]

        if not eligible_days:
            continue  # no room — future: surface a warning to the user

        # Back-loaded weights: earlier days get less, later days get more.
        # e.g. 3 eligible days → weights [1, 2, 3], total = 6
        # Day 1 gets 1/6, Day 2 gets 2/6, Day 3 gets 3/6 of total hours.
        weights = list(range(1, len(eligible_days) + 1))
        total_weight = sum(weights)

        # First pass: distribute proportionally with back-loaded weights
        for i, d in enumerate(eligible_days):
            if hours_left <= 0:
                break
            slot = days[d]
            proportional = (weights[i] / total_weight) * assignment.est_hours

            # Cap allocation on the due date to MIN_SESSION (review only)
            is_due_date = (d == assignment.due_date)
            daily_cap = MIN_SESSION if is_due_date else MAX_SINGLE_DAY

            allocated = min(proportional, slot.hours_remaining, hours_left, daily_cap)
            if allocated >= MIN_SESSION:
                slot.blocks.append(Block(assignment=assignment, hours=round(allocated, 2)))
                hours_left -= allocated

        # Second pass: fill any hours that didn't fit the weighted spread
        if hours_left > 0.01:
            for d in eligible_days:
                if hours_left <= 0:
                    break
                slot = days[d]
                extra = min(slot.hours_remaining, hours_left)
                if extra >= MIN_SESSION:
                    existing = next(
                        (b for b in slot.blocks if b.assignment is assignment), None
                    )
                    if existing:
                        existing.hours = round(existing.hours + extra, 2)
                    else:
                        slot.blocks.append(Block(assignment=assignment, hours=round(extra, 2)))
                    hours_left -= extra

    return [days[d] for d in sorted_dates]


def print_schedule(schedule: list[DaySchedule]) -> None:
    """Pretty-print the schedule to the terminal."""
    for day in schedule:
        header = day.date.strftime("%A, %b %d")
        print(f"\n{header}  ({day.hours_scheduled:.1f}/{day.available_hours:.1f} hrs used)")
        print("-" * 40)
        if not day.blocks:
            print("  Nothing scheduled")
        for block in day.blocks:
            a = block.assignment
            days_left = a.days_until_due(day.date)
            due_str = f"due in {days_left}d" if days_left > 0 else "due TODAY"
            print(f"  {block.hours:.1f}h  [{a.course.code}] {a.title}  ({due_str})")
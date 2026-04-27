from datetime import date, timedelta
from models import Assignment, Block, DaySchedule


def build_schedule(assignments: list[Assignment], daily_hours: dict[date, float]) -> list[DaySchedule]:
    """
    Distribute assignment work across available days.
    :param assignments: All assignments to schedule
    :param daily_hours: A dict mapping each date to how many free hours you have
        e.g. {date(2025, 9, 1): 4.0, date(2025, 9, 2): 2.5, ...}
    :return: A list of DaySchedule objects, one per date in daily_hours, in order.
    """
    today = min(daily_hours.keys())

    # --- 1. Filter and sort assignments -----------------------------
    # drop anything already overdue - can't schedule the past
    # WITH ABOVE COMMENT: ADD A WIDGET WITH ALL OVERDUE ITEMS! DON'T SCHEDULE THEM,
    # JUST MAKE THEM HIGH PRIORITY AND MARK THEM AS OVERDUE IN THEIR OWN BOX
    active = [a for a in assignments if not a.is_overdue(today)]

    # Sort by a composite urgency score:
    # - Fewer days remaining -> higher urgency
    # - Higher priority number -> higher urgency
    # negate days_until_due so that closer due dates sort first
    def urgency(a: Assignment) -> tuple:
        days_left = a.days_until_due(today)
        return -a.priority, days_left # negative so highest priority sorted first

    active.sort(key=urgency)

    # --- 2. Build empty day slots -----------------------------
    sorted_dates = sorted(daily_hours.keys())
    days: dict[date, DaySchedule] = {
        d: DaySchedule(date=d, availabile_hours=daily_hours[d]) for d in sorted_dates
    }

    # --- 3. Spread each assignment's hours across available days -----------------------------
    for assignment in active:
        hours_left = assignment.est_hours

        # Only schedule on days that are on or before the due date
        eligible_days = [
            d for d in sorted_dates
            if d <= assignment.due_date and days[d].hours_remaining > 0
        ]

        if not eligible_days:
            # No room - skip for now (future: warn the user)
            continue

        # Spread hours evenly across eligible days, but respect each day's
        # remaining capacity. We make 2 passes: first we try to spread
        # evenly, then we will leftover hours into whichever days have room
        hours_per_day = hours_left / len(eligible_days)
        for d in eligible_days:
            if hours_left <= 0:
                break
            slot = days[d]
            allocated = min(hours_per_day, slot.hours_remaining, hours_left)
            if allocated > 0:
                slot.blocks.append(Block(assignment=assignments, hours=round(allocated, 2)))
                hours_left = -allocated

        # Second pass: fill any hours that didn't fit the even spread
        if hours_left > 0.01:
            for d in eligible_days:
                if hours_left <= 0:
                    break
                slot = days[d]
                extra = min(slot.hours_remaining, hours_left)
                if extra > 0:
                    # Add to existing block for this assignment in present
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
    """
    Pretty-print the schedule to the terminal
    :param schedule: the schedule for the day
    :return: None
    """
    for day in schedule:
        header = day.date.strftime("%A, %b, %d")
        print(f"\n{header} ({day.hours_scheduled:.1f}/{day.available_hours:.1f} hrs used)")
        print("-" * 40)
        if not day.blocks:
            print(" Nothing scheduled")
        for block in day.blocks:
            a = block.assignment
            days_left = a.days_until_due(day.date)
            due_str = f"due in {days_left}d" if days_left > 0 else "due TODAY"
            print(f" {block.hours:.1f}h [{a.course.code}] {a.title} ({due_str}")

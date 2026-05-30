from datetime import date, timedelta

from models import Assignment, Course, TaskType, Semester
from scheduler import build_schedule, print_schedule, generate_daily_hours

# --- Courses ------------------------------
cs401 = Course("Algorithms", "CS 401", 3, "#6366f1")
bio201 = Course("Cell Biology", "BIO 201", 3, "#10b981")
eng310 = Course("Technical Writing", "ENG 310", 4, "#f59e0b")

# --- Assignments ------------------------------
semester_start = date(2026, 8, 24)

assignments = [
    Assignment(
        title="Dijkstra's algorithm implementation",
        course=cs401,
        task_type=TaskType.CODING,
        due_date=semester_start + timedelta(days=3),
        priority=4,
        est_hours=6.0
    ),
    Assignment(
        title="Chapter 7 reading - cell membranes",
        course=bio201,
        task_type=TaskType.READING,
        due_date=semester_start + timedelta(days=1),
        priority=3
        # est_hours omitted; defaults to 1.0 (READING default)
    ),
    Assignment(
        title="Lab report draft",
        course=bio201,
        task_type=TaskType.ESSAY,
        due_date=semester_start + timedelta(days=5),
        priority=3
    ),
    Assignment(
        title="Essay outline - technical communication",
        course=cs401,
        task_type=TaskType.EXAM_PREP,
        due_date=semester_start + timedelta(days=6),
        priority=5
    )
]

# --- Semester ------------------------------
semester = Semester(
    name="Fall 2026",
    start_date=date(2026, 8, 24),
    end_date=date(2026, 12, 12),
    courses=[cs401, bio201, eng310]
)

# --- Run and display ------------------------------
daily_hours = generate_daily_hours(semester)
schedule = build_schedule(assignments, daily_hours)
print_schedule(schedule)
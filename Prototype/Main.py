from datetime import date, timedelta
from models import Assignment, Course, TaskType
from scheduler import build_schedule, print_schedule

# --- Courses ------------------------------
cs401 = Course("Algorithms", "CS 401", "#6366f1")
bio201 = Course("Cell Biology", "BIO 201", "#10b981")
eng310 = Course("Technical Writing", "ENG 310", "#f59e0b")

# --- Assignments ------------------------------
today = date.today()

assignments = [
    Assignment(
        title="Dijkstra's algorithm implementation",
        course=cs401,
        task_type=TaskType.CODING,
        due_date=today + timedelta(days=3),
        priority=4,
        est_hours=6.0
    ),
    Assignment(
        title="Chapter 7 reading - cell membranes",
        course=bio201,
        task_type=TaskType.READING,
        due_date=today + timedelta(days=1),
        priority=3
        # est_hours omitted; defaults to 0.1 (READING default)
    ),
    Assignment(
        title="Lab report draft",
        course=bio201,
        task_type=TaskType.ESSAY,
        due_date=today + timedelta(days=5),
        priority=3
    ),
    Assignment(
        title="Essay outline - technical communication",
        course=cs401,
        task_type=TaskType.EXAM_PREP,
        due_date=today + timedelta(days=6),
        priority=5
    )
]

# --- Available hours per day ------------------------------
# adjust these to reflect your actual time for the week
daily_hours = {
    today + timedelta(days=i): hours
    for i, hours in enumerate([3.0, 4.0, 2.5, 4.0, 3.5, 5.0, 3.0])
}

# --- Run and display ------------------------------
schedule = build_schedule(assignments, daily_hours)
print_schedule(schedule)
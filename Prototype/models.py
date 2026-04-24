from dataclasses import dataclass, field
from datetime import date, time
from enum import Enum
from typing import Optional


class TaskType(Enum):
    HOMEWORK = "homework"
    READING = "reading"
    CODING = "coding"
    EXAM_PREP = "exam_prep"
    ESSAY = "essay"
    OTHER = "other"


DEFAULT_HOURS: dict[TaskType, float] = {
    TaskType.HOMEWORK: 1.5,
    TaskType.READING: 1.0,
    TaskType.CODING: 5.0,
    TaskType.EXAM_PREP: 0.5,
    TaskType.ESSAY: 2.0,
    TaskType.OTHER: 1.0
    }


@dataclass
class Course:
    name: str # i.e Software Design
    code: str # i.e. CS 340
    color: str = '888' # used for UI color later


@dataclass
class Assignment:
    title: str
    course: Course
    task_type: TaskType
    due_date: date
    priority: int = 3 # 1 to 5, low to high. mid is default
    due_time: Optional[time] = None # None assumes 11:59pm end of day
    est_hours: Optional[float] = None

    def __post_init__(self):
        # if no estimate is provided, falls back to the type default estimate
        if self.est_hours is None:
            self.est_hours = DEFAULT_HOURS[self.task_type]

    def days_until_due(self, from_date: date):
        return (self.due_date - from_date).days

    def is_overdue(self, from_date: date):
        return self.due_date < from_date



@dataclass
class Block:
    """ A single chunk of work scheduled on a given day"""
    assignment: Assignment
    hours: float



@dataclass
class DaySchedule:
    """ The scheduler's output for one day"""
    date: date
    available_hours: float
    blocks: list[Block] = field(default_factory=list)

    @property
    def hours_scheduled(self):
        return sum(b.hours for b in self.blocks)

    @property
    def hours_remaining(self):
        return max(0.0, self.available_hours - self.hours_scheduled)
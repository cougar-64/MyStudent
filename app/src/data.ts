import {type Assignment, type Course, type Semester, TaskType} from "./types.ts";

let cs401: Course =
    {
        name: "Algorithms",
        code: "CS 401",
        weeklyHours: 3,
        color: "#6366f1"
    };
let cs340: Course =
    {
        name: "Software Engineering",
        code: "CS 340",
        weeklyHours: 3,
        color: "#6355f1"
    };
let cs404: Course =
    {
        name: "ethics",
        code: "CS 404",
        weeklyHours: 3,
        color: "#6344f1"
    };

export const courses: Course[] = [cs401, cs340, cs404];

export const semesters: Semester[] = [
    {
        name: "Fall 2026",
        startDate: "2026-09-05",
        endDate: "2026-12-15",
        courses: courses
    }
]

export const assignments: Assignment[] = [
    {
        title: "Introductions",
        course: cs401,
        taskType: TaskType.HOMEWORK,
        dueDate: "2026-09-20",
        priority: 2,
        dueTime: null,
        estHours: 0.5,
        completed: false,
        completedDate: null
    },

    {
        title: "Phase 1",
        course: cs340,
        taskType: TaskType.CODING,
        dueDate: "2026-10-10",
        priority: 5,
        dueTime: null,
        estHours: 10,
        completed: false,
        completedDate: null
    },
    {
        title: "AI Ethics",
        course: cs404,
        taskType: TaskType.READING,
        dueDate: "2026-09-10",
        priority: 3,
        dueTime: null,
        estHours: 1,
        completed: false,
        completedDate: null
    }
]


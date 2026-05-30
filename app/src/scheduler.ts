import {type DaySchedule, TaskType} from "./types.ts";
import type {Semester, Assignment} from "./types.ts";

const MIN_SESSION = 0.5;
const MAX_SINGLE_DAY = 3;

const DEFAULT_HOURS: Record<TaskType, number> = {
    [TaskType.HOMEWORK]: 1.5,
    [TaskType.READING]: 1.0,
    [TaskType.CODING]: 5.0,
    [TaskType.EXAM_PREP]: 2.0,
    [TaskType.ESSAY]: 2.5,
    [TaskType.OTHER]: 1.0
}


export function generateDailyHours(semester: Semester): Record<string, number> {
    let totalWeeklyHours = 0;
    for (let i = 0; i < semester.courses.length; i++) {
        totalWeeklyHours += semester.courses[i].weeklyHours;
    }
    let hoursPerWeekday = totalWeeklyHours / 5;
    let daily: Record<string, number> = {};
    const current = new Date(semester.startDate);
    const end = new Date(semester.endDate);
    while (current < end) {
        const day = current.getDay();
        if (day != 0 && day != 6) {
            const key = current.toISOString().split('T')[0];
            daily[key] = Math.round(hoursPerWeekday * 100) / 100;
        }
        current.setDate(current.getDate() + 1);
    }
    return daily
}


export function buildSchedule(assignments: Assignment[], dailyHours: Record<string, number>): DaySchedule[] {
    let today = Math.min(...Object.keys(dailyHours).map(Number));
    const x = 5
}
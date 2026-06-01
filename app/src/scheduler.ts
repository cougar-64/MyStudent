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
    let today = Object.keys(dailyHours).sort()[0];
    let active: Assignment[] = [];
    for (let i = 0; i <assignments.length; i++) {
        if (assignments[i].dueDate > today) {
            active.push(assignments[i]);
        }
    }
    function urgency(a: Assignment): number {
        const daysLeft = (new Date(a.dueDate).getTime() - new Date(today).getTime()) / (1000 * 60 * 60 * 24)
        return daysLeft - (a.priority * 0.5)
    }
    active.sort((a, b) => urgency(a) - urgency(b))
    const sortedDates = Object.keys(dailyHours).sort();
    const days: Record<string, DaySchedule> = {};
    for (const d of sortedDates) {
        days[d] = {
            date: d,
            availableHours: dailyHours[d],
            blocks: []
        }
    }
    for (const assignment of active) {
        let hoursLeft = assignment.estHours ?? DEFAULT_HOURS[assignment.taskType];
        let eligibleDays = [];
        for (const d of sortedDates) {
            const hoursRemaining = days[d].availableHours - days[d].blocks.reduce((sum, b) => sum + b.hours, 0);
            if (d <= assignment.dueDate && hoursRemaining > 0) {
                eligibleDays.push(d);
            }
        }
        if (eligibleDays.length === 0) {
            continue;
        }
        const weights = eligibleDays.map((_, i) => i + 1);
        const totalWeight = weights.reduce((sum, w) => sum + w, 0);
        for (let i = 0; i < eligibleDays.length; i++) {
            const d = eligibleDays[i];
            if (hoursLeft <= 0) {
                break;
            }
            let slot = days[d];
            let proportional = (weights[i] / totalWeight) * (assignment.estHours ?? DEFAULT_HOURS[assignment.taskType]);
            let isDueDate = (d === assignment.dueDate)
            let dailyCap = null;
            if (isDueDate) {
                dailyCap = MIN_SESSION
            }
            else {
                dailyCap = MAX_SINGLE_DAY;
            }
            let allocated = Math.min(proportional, slot.availableHours - slot.blocks.reduce((sum, b) => sum + b.hours, 0), hoursLeft, dailyCap);
            if (allocated >= MIN_SESSION) {
                slot.blocks.push({
                    assignment: assignment,
                    hours: Math.round(allocated * 100) / 100
                });
                hoursLeft -= allocated;
            }
        }
    }
}
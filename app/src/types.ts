export enum TaskType {
    HOMEWORK  = "homework",
    READING   = "reading",
    CODING    = "coding",
    EXAM_PREP = "exam_prep",
    ESSAY     = "essay",
    OTHER     = "other",
}


export interface Course {
    name: string;
    code: string;
    weeklyHours: number;
    color: string; // used for UI color-coding later
}


export interface Assignment {
    title: string;
    course: Course;
    taskType: TaskType;
    dueDate: string;
    priority: number; // low (1) to high (5) (haha high-5, get it?)
    dueTime: string | null; // assumes due at 11:59pm end of day
    estHours: number | null;
    completed: boolean;
    completedDate: string | null;
}


export interface Block { // a single chunk of work in a given day
    assignment: Assignment;
    hours: number;
}


export interface DaySchedule { // the scheduler's output for the day
    date: string;
    availableHours: number;
    blocks: Block[];
}


export interface Semester {
    name: string;
    startDate: string;
    endDate: string;
    courses: Course[];
}
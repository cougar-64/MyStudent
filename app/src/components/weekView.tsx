import type { DaySchedule } from "../types.ts";

interface WeekViewProps {
    schedule: DaySchedule;
}

export function WeekView({ schedule }: WeekViewProps) {
    return (
        <div>
            <p>Week view goes here</p>
        </div>
    );
}
import type { DaySchedule } from "../types.ts";
import { useState } from "react";

interface WeekViewProps {
    schedule: DaySchedule[];
}

export function WeekView({ schedule }: WeekViewProps) {
    const [weekOffset, setWeekOffset] = useState(0);
    const today = new Date();
    today.setHours(0, 0, 0, 0);

    // find Monday of the current week
    const monday = new Date(today);
    const dayOfWeek = today.getDay(); // 0 = Sunday, 1 = Monday, etc.
    const daysFromMonday = dayOfWeek === 0 ? -6 : 1 - dayOfWeek;
    monday.setDate(today.getDate() + daysFromMonday + (weekOffset * 7));

    // build an array of monday-friday date strings for this week
    const weekDates: string[] = [];
    for (let i = 0; i < 7; i++) {
        const d = new Date(monday);
        d.setDate(monday.getDate() + i);
        weekDates.push(d.toISOString().split('T')[0]);
    }

    const weekSchedule = weekDates.map(dateStr =>
            schedule.find(day => day.date === dateStr) ?? {
                date: dateStr,
                availableHours: 0,
                blocks: []
            }
    );

    const dayNames = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];

    return (
        <div style={{ display: "flex", flexDirection: "column", gap: "1rem", padding: "1rem" }}>
            <div style={{ display: "flex", alignItems: "center", gap: "1rem" }}>
                <button onClick={() => setWeekOffset(weekOffset - 1)}>← Prev</button>
                <button onClick={() => setWeekOffset(0)}>Today</button>
                <button onClick={() => setWeekOffset(weekOffset + 1)}>Next →</button>
            </div>
            <div style={{ display: "flex", gap: "1rem" }}>
                {weekSchedule.map((day, i) => {
                    const isToday = day.date === today.toISOString().split('T')[0];
                    return (
                        <div
                            key={day.date}
                            style={{
                                flex: 1,
                                border: isToday ? "2px solid #6366f1" : "1px solid #ddd",
                                borderRadius: "8px",
                                padding: "0.75rem",
                                backgroundColor: isToday ? "#f5f3ff" : "#fff",
                            }}
                        >
                            <p style={{ fontWeight: isToday ? "bold" : "normal", marginBottom: "0.5rem" }}>
                                {dayNames[i]} {day.date.slice(5)}
                            </p>
                            {day.blocks.length === 0 ? (
                                <p style={{ color: "#aaa", fontSize: "0.8rem" }}>Nothing scheduled</p>
                            ) : (
                                day.blocks.map((block, j) => (
                                    <div
                                        key={j}
                                        style={{
                                            backgroundColor: block.assignment.course.color,
                                            borderRadius: "4px",
                                            padding: "0.4rem 0.5rem",
                                            marginBottom: "0.4rem",
                                            color: "#fff",
                                            fontSize: "0.8rem",
                                        }}
                                    >
                                        <strong>{block.hours}h</strong> {block.assignment.title}
                                    </div>
                                ))
                            )}
                        </div>
                    );
                })}
            </div>
        </div>
    );
}
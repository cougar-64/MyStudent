# MyStudent — Product Roadmap & Future Ideas

This document captures product ideas and the thinking behind them.
Some are already built. Some are next. Some are further out.
The goal is to record not just *what* to build, but *why*.

---

## Already Built

### Python prototype (proof of concept)
The scheduling algorithm — urgency sorting, back-loaded weighting,
minimum session length, due-date capping — was proven out in Python
first before any UI was written. This let the hard logic get debugged
fast without fighting a build tool or component re-renders at the same
time.

### Credit hour rule
The app uses a real academic standard — the Carnegie Unit — as its
scheduling foundation. 1 credit hour = 1 hour of outside work per week.
A student taking 15 credit hours gets roughly 15 hours of homework
budgeted per week automatically. Setup takes minutes instead of manually
entering availability every day. Lives on `Course.weeklyHours`, feeds
`generateDailyHours()`.

### Full semester auto-scheduling
`generateDailyHours()` builds a full day-by-day hour budget from semester
start to end, derived from total course credit hours. The user never
manually enters availability — they add assignments and the scheduler
figures out the rest. This is the core insight that separates MyStudent
from a basic to-do list.

### Spaced distribution (back-loaded weighting)
The scheduler spreads hours across eligible days with *less* time early
and *more* time as the due date approaches — not an even split. This
exists because of a direct personal frustration: "I never start early
enough." Starting light and ramping up matches how students actually
work, and the structure nudges starting early without making day one
feel heavy.

### Minimum session length + due-date capping
`MIN_SESSION` (0.5 hrs) prevents the scheduler from creating useless
tiny blocks, and ensures short tasks get scheduled in one sitting rather
than split thin across days. Separately, the day an assignment is
actually due is capped to a light review session rather than a full
work block — the due date is for turning something in, not finishing it.

### TypeScript port (full pipeline)
`models.py` → `types.ts`, `scheduler.py` → `scheduler.ts`, ported field
by field and function by function. The Python prototype worked as a
spec, not just a reference — the translation was close to 1:1.

### Week view UI
Horizontal calendar-style week view, all 7 days, with previous/today/next
navigation. Today is visually emphasized (border + background) without
overwhelming the rest of the week — directly based on user preference
during build ("today a little big and emphasized so it pops").

### Mark complete + live rescheduling
Checking an assignment complete removes it from the active list fed into
`buildSchedule`, which re-runs on every state change. Completed work's
remaining hours are freed up automatically for everything else — this
was the single most-wanted feature going into the TypeScript build
("I need... the schedule to automatically refactor itself if I finish
an assignment early or get it done late"), and it fell out almost for
free because state changes trigger a full scheduler re-run rather than
patching an old plan.

---

## Known Gaps (found during building, not yet fixed)

### Completed/overdue work disappears with no record
Right now, marking something complete makes it vanish from the schedule
entirely — there's no way to look back and see what you finished, or
when an overdue item slipped past its due date. This was flagged as a
real moment of confusion while testing ("it deleted the assignment
entirely"). The data isn't actually deleted — it's just that no view
exists yet for completed or overdue work. Needs:
- A "recently completed" view, visible for ~7 days after completion
- A "recently overdue" view for assignments that passed due date without
  being marked done, instead of silently disappearing

### No way to add assignments through the UI
Everything currently lives in a hardcoded `data.ts`. Needs a real form,
and the `Assignment` model should grow a `description` field at the same
time so assignments can carry real instructions/notes, not just a title.

### No persistence
Refreshing the page loses all state. This is the most urgent gap —
everything above (completed history, overdue tracking, user-added
assignments) is pointless if it doesn't survive a page reload.

---

## Next — Persistence & Data Layer

### localStorage first
Before reaching for a backend, get persistence working locally:
save state to localStorage on every change, load from localStorage on
startup (falling back to sample data if nothing's saved). Since the data
model already uses plain objects and ISO date strings rather than real
`Date` objects or class instances, this should serialize cleanly with
`JSON.stringify` / `JSON.parse` — no special handling needed.

### Then: real backend (Supabase)
Several separately-listed feature ideas are actually the same underlying
piece of work:

- **"SQL database so data persists across logins"** — Supabase *is* a
  hosted Postgres (SQL) database with the backend already built.
- **"Login/logout, multiple users"** — Supabase auth comes bundled in,
  rather than building auth from scratch.

So rather than three separate projects, this is one migration: swap the
localStorage layer for Supabase once the local version is working and
the storage interface is clean. Build against an abstraction now so the
swap later doesn't require rewriting the UI.

### Thinking about scale, even on a small project
Prompted by the question "what if this scaled to 2 million users?" — the
honest answer is this project will likely never need that scale, and
that's fine. The value isn't solving for 2 million users now, it's
building the habit of thinking about it: keeping the scheduler as a pure
function (so it could run server-side later if needed), letting Supabase
handle auth/security instead of rolling it by hand, not assuming
single-user/single-device. These are the kinds of decisions worth being
able to explain in an internship interview, even on a project with ten
real users.

---

## New Feature Ideas (raised during planning, not yet built)

### Course colors — pure polish
`Course.color` already exists in the data model and is already used in
the week view. What's missing is a UI to *pick* the color instead of
hardcoding hex values in `data.ts`. Small and self-contained once a
course-editing form exists. Purpose: visually distinguishing classes at
a glance to stay organized, not just aesthetic.

### Feedback mechanism — new interaction
Important once this reaches beta/user testing. Doesn't need real
infrastructure to start — a `mailto:` link or simple form that opens the
user's email client covers most of the value with very little build
effort. A real feedback dashboard/database is a later-stage concern.

### Grade list — new view
Distinct from the scheduler entirely — grades are records to track, not
work to schedule. Deserves its own data model (a `Grade` interface) and
its own view, separate from the week view. Open question: manually
entered, or eventually pulled from somewhere automatically? Not urgent;
a good Phase 6 feature once the core scheduler/UI is solid.

---

## Phase 3–4 — Schedule Awareness (not started)

### Work shifts and blocked time
Real life has fixed commitments — jobs, club meetings, gym time — that
the scheduler currently has no concept of. The plan is to let users mark
specific time blocks as unavailable and have the scheduler route around
them. Meaningful feature, real complexity increase — belongs after the
core scheduling + persistence work is solid, not before.

---

## Further Out — The Hard Stuff

### Calendar-style editing with live rescheduling
The bigger vision: drag a block to a different day, and the scheduler
automatically readjusts everything downstream — what Motion and
Reclaim.ai do. Genuinely hard (the rescheduling cascade, what happens
when you move a block other things were depending on) but the right
long-term direction for MyStudent.

### iOS app
Web first was the right call — it reduced complexity while learning
TypeScript and let existing JS skills transfer. iOS comes after the web
app is solid and can likely reuse the same scheduling logic.

---

## Notes on Scope

The temptation with a project like this is to build everything at once
— and the ideas keep coming faster than they can be built, which is a
good sign the product direction is real. The discipline that matters
most right now is the one already being practiced: write every idea
down the moment it shows up, then keep building the current phase
anyway. Persistence is the next real milestone — almost everything else
on this list (completed history, overdue tracking, multi-user, even the
feedback form) is waiting on data actually surviving a page refresh.
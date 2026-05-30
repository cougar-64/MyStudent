# MyStudent — Product Roadmap & Future Ideas

This document captures product ideas and the thinking behind them.
Some are already built. Some are next. Some are further out.
The goal is to record not just *what* to build, but *why*.

---

## Already Built (Python Prototype)

### Credit hour rule
The app uses a real academic standard — the Carnegie Unit — as its
scheduling foundation. 1 credit hour = 1 hour of outside work per week.
This means a student taking 15 credit hours has roughly 15 hours of
homework per week, or 3 hours per weekday. Building this in means setup
takes 2 minutes at the start of a semester instead of manually budgeting
hours every single day. It fits naturally on the `Course` model via
`weekly_hours` and feeds directly into `generate_daily_hours()`.

### Full semester auto-scheduling
Rather than asking the user "how many hours do you have today?", the app
generates a `daily_hours` dict for every weekday from semester start to
semester end, derived automatically from each course's credit hours. The
user never thinks about availability — they just add assignments and the
scheduler figures it out. This is the core product insight that separates
MyStudent from a basic to-do list.

---

## Near Term — Algorithm Improvements

### Spaced distribution (the scheduling philosophy)
Right now the scheduler spreads hours evenly across eligible days. The
better approach — and the whole reason this app exists — is to schedule
work as far out as possible and ramp up toward the due date. A 6-hour
assignment due in 10 days should look like:

```
Day 1:  0.5hrs   ← just get started, build familiarity
Day 2:  0.5hrs
Day 3:  1.0hr
Day 4:  1.0hr
Day 5:  1.0hr
Day 6:  1.5hrs
Day 7:  1.5hrs   ← heavier sessions closer to due date
```

This is back-loaded weighting — earlier days get less, later days get
more. The weights count up instead of down. This reflects how students
actually work best: small early sessions to get familiar with the
material, heavier sessions when the deadline creates natural urgency.

### Minimum session length
Already implemented via `MIN_SESSION = 0.5`. Any block smaller than 30
minutes doesn't get scheduled — it's not worth the context switching.
This also means short tasks (a 1-hour reading) get scheduled in one
sitting rather than split across multiple days.

### Overdue item surfacing
Overdue assignments don't get scheduled — you can't change the past. But
they shouldn't just disappear. The app should surface them in their own
visible "overdue" section, marked clearly, so the student knows they
exist and can deal with them manually. This is noted in the code already
as a comment.

---

## Phase 3–4 — Schedule Awareness

### Work shifts and blocked time
The current model assumes all weekday hours are available for homework.
In reality, students have jobs, club meetings, gym time, and other fixed
commitments. The right solution is to let users mark time blocks as
unavailable, and have the scheduler route around them automatically.
This is a meaningful feature but would significantly increase complexity
if added now — it belongs in Phase 3 or 4 once the core scheduling logic
is solid.

### Weekend toggle
Right now weekends are excluded from scheduling entirely (`weekday() < 5`).
Some students do homework on weekends. This should be a user preference,
not a hardcoded assumption.

---

## Further Out — The Hard Stuff

### Calendar-style editing with live rescheduling
The bigger vision: a calendar UI where you can drag a block to a
different day and the scheduler automatically readjusts everything
downstream. Move one thing, and the ripple effects propagate correctly
across the rest of the week.

This is essentially what Motion and Reclaim.ai do. It's a genuinely hard
engineering problem — the rescheduling cascade alone (what happens when
you move a block that was load-bearing for three other assignments) is
tricky to get right without creating conflicts or dropping hours. This is
the right long-term vision for MyStudent. It's a Phase 4–5 problem.

### iOS app
The web app comes first. Once the scheduling logic is proven and the UI
feels right, an iOS app is a natural next step. Building web first was
the right call — it reduces complexity during the learning phase and
leverages existing JavaScript/TypeScript skills. iOS can reuse the same
scheduling logic.

---

## Notes on Scope

The temptation with a project like this is to build everything at once.
The right move is the opposite: get the scheduler producing a plan you'd
actually follow, then build the UI around it, then add the smart features
on top. Each phase should be usable on its own before the next one starts.

The credit hour rule + full semester scheduling + spaced distribution is
already a more useful product than most student planners on the market.
That's the MVP. Everything else is a feature.

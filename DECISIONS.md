# Decision log

This file records design decisions made while carrying out the work, in the order they were made. It exists so that a choice made under time pressure in week three does not get forgotten, or worse, get rewritten in memory to sound cleverer than it was.

## Format

One entry per decision. Each entry has three parts: the date, a one line statement of the decision, and one sentence on why it was made. Keep entries short. This is a log, not an essay.

```
### YYYY-MM-DD
**Decision:** what was decided.
**Why:** the one sentence reason.
```

Log a decision whenever you:

- choose one modeling assumption over another (a grid resolution, a parameter value, which of several models to prioritize if time runs short)
- change something the protocol left open
- hit a dead end and change approach
- discover the data does not support the original plan, and adjust scope

Do **not** use this file to change a research question, a hypothesis, or a pre-registered threshold after seeing results. Those are fixed by `PROTOCOL.md`. If a threshold turns out to have been chosen badly, that observation belongs in the report's Limitations section, not in a retroactive edit here.

## Example entry (for format reference only, delete before the first real entry)

### 2026-08-19
**Decision:** Dropped the 100 meter demand grid in favor of a 400 meter grid.
**Why:** the 80,000 point version of the problem does not solve in reasonable time, and the difference in mean travel time between the two resolutions is under 6 seconds.

---

## Log

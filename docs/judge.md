# student-judge competency report

**Judged at:** 2026-10-05T12:37:17-04:00
**Evidence pass:** re-read current docs/report.md, docs/diagrams/, docs/wireframes/, and local project validation output; prior judge markdown was ignored as stale.

## Phase-by-phase rubric

| Phase | Status | Notes |
|---|---|---|
| 1 — Project + workflows | Met | The report clearly names the assigned project as MyAdvisor and defines three core workflows: Track Degree Progress, Plan Semester Course Selections, and Review and Approve Course Plan. |
| 2 — Use-case diagram | Met | Use-case diagram is present and linked in the report; the report calls out shared and extended flows in the narrative. |
| 3 — Model diagram | Met | The ERD is named and represented as a Mermaid `erDiagram` with program, requirement, course, student course, semester plan, and plan course entities. |
| 4 — Wireframes | Met | Wireframe coverage is embedded in the report and the single dashboard mockup is mapped to the relevant workflows. |
| 5 — Theme + build + polish | Mostly met | The app has theming, workflow implementation, usability polish, and stronger status/feedback treatment; the project reports a validated local build. |
| 6 — Deploy | Not met | No live Render URL or deployed app evidence is recorded in the report yet. |

## Strengths

- The project matches the assignment brief with a clear MyAdvisor scope and three named workflows.
- The report includes the required use-case PNG and accepts a Mermaid model diagram for the ERD.
- The app appears to implement the advisor/student workflow in a polished dashboard pattern with role-aware views, plan status handling, and validation feedback.
- Project validation is clean: the CLI skill integrity check passes and the automated tests pass.

## Gaps

- Phase 6 is incomplete because the report still lacks a live Render URL and deployment evidence.
- The model diagram issue is not a scoring problem in itself, but the source Mermaid content was not rendered in the export until the Node tooling was installed and the report was regenerated.

## Awarded total / scoreable max

- Awarded: 24 / 30
- Overall: 3.2 / 4

## Summary

This is a strong assignment submission overall: the project is well-scoped, the workflow design is credible, the ERD and use-case artefacts are in place, and the local implementation is clearly validated. The main missing item is the live deployment evidence for Phase 6, which prevents a higher final mark.

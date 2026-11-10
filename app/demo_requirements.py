"""Owner-approved fictional coursework data; not an official UWI curriculum."""

DEMO_PROGRAM = "Computer Science"
DEMO_TOTAL_CREDITS = 93
DEMO_REQUIREMENTS = (
    ("Core Courses", 36),
    ("General Education", 18),
    ("Electives", 12),
    ("Major Requirements", 18),
    ("Additional Requirements", 9),
)

# Only these known demonstration values may be migrated automatically.
LEGACY_DEMO_REQUIREMENTS = {
    "Core Courses": 36,
    "General Education": 18,
    "Electives": 18,
    "Major Requirements": 24,
    "Additional Requirements": 24,
}

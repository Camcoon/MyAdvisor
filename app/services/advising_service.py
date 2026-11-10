from datetime import datetime, timezone

from sqlmodel import Session

from app.demo_requirements import (
    DEMO_PROGRAM,
    DEMO_REQUIREMENTS,
    DEMO_TOTAL_CREDITS,
    LEGACY_DEMO_REQUIREMENTS,
)
from app.models.advising import (
    Course,
    DegreeProgram,
    DegreeRequirement,
    SemesterPlan,
    StudentCourse,
)
from app.repositories.advising import AdvisingRepository
from app.repositories.user import UserRepository
from app.schemas.advising import (
    AdvisorPlanResponse,
    CourseSelectionResponse,
    DegreeProgressResponse,
    SemesterPlanResponse,
)
from app.services.advising_errors import (
    PlanConflictError,
    PlanNotFoundError,
    PlanValidationError,
)

DEFAULT_PROGRAM = DEMO_PROGRAM
DEFAULT_TOTAL_CREDITS = DEMO_TOTAL_CREDITS
SEMESTER_OPTIONS = tuple(
    f"Year {year} semester {semester}"
    for year in range(1, 4)
    for semester in range(1, 4)
)
RESUBMITTABLE_PLAN_STATUSES = {"Rejected", "Changes Requested"}


class AdvisingService:
    def __init__(self, db: Session):
        self.repo = AdvisingRepository(db)
        self.user_repo = UserRepository(db)

    def sync_demo_requirements(self, *, apply: bool = False) -> list[dict]:
        """Review/apply the approved demo allocation, preserving existing row IDs.

        Reject unfamiliar/custom data before changing any row. This deliberately
        does not seed users, courses, academic records, or semester plans.
        """
        program = self.repo.get_degree_program_by_name(DEFAULT_PROGRAM)
        if program is None:
            raise ValueError("The fictional Computer Science demo program does not exist.")
        if program.total_credits != DEFAULT_TOTAL_CREDITS:
            raise ValueError("Demo degree total differs from the approved 93 credits; review required.")
        existing = self.repo.list_degree_requirements(program.id)
        requirements = {row.category: row for row in existing}
        approved = dict(DEMO_REQUIREMENTS)
        if len(requirements) != len(existing) or set(requirements) - approved.keys():
            raise ValueError("Unexpected or duplicate demo requirement categories; review required.")
        for category, row in requirements.items():
            if row.required_credits not in {approved[category], LEGACY_DEMO_REQUIREMENTS[category]}:
                raise ValueError(f"Custom requirement for {category}; review required before migration.")

        review = [
            {
                "category": category,
                "previous": requirements[category].required_credits if category in requirements else None,
                "required": credits,
                "changed": category not in requirements or requirements[category].required_credits != credits,
            }
            for category, credits in DEMO_REQUIREMENTS
        ]
        if apply:
            changes = []
            for item in review:
                if not item["changed"]:
                    continue
                row = requirements.get(item["category"])
                if row is None:
                    row = DegreeRequirement(program_id=program.id, category=item["category"],
                                            required_credits=item["required"])
                else:
                    row.required_credits = item["required"]
                changes.append(row)
            if changes:
                self.repo.save_degree_requirements(changes)
        return review

    def ensure_demo_data(self) -> None:
        program = self.repo.get_degree_program_by_name(DEFAULT_PROGRAM)
        if program is None:
            program = DegreeProgram(name=DEFAULT_PROGRAM, total_credits=DEFAULT_TOTAL_CREDITS)
            self.repo.db.add(program)
            self.repo.db.commit()
            self.repo.db.refresh(program)

        self.sync_demo_requirements(apply=True)

        catalog = (
            ("COMP 1101", "Introduction to Programming", 3, "", "Core Courses", "Computer Science"),
            ("MATH 1200", "Discrete Mathematics", 3, "", "General Education", "Mathematics"),
            ("COMP 1600", "Data Structures", 3, "COMP 1101", "Core Courses", "Computer Science"),
            ("COMP 2100", "Database Design", 3, "COMP 1600", "Core Courses", "Computer Science"),
            ("COMP 2400", "Software Engineering", 3, "COMP 1600", "Major Requirements", "Computer Science"),
            ("COMP 2510", "Operating Systems", 3, "COMP 1600", "Major Requirements", "Computer Science"),
            ("COMP 2604", "Operating Systems II", 3, "COMP 1600", "Core Courses", "Computer Science"),
            ("COMP 2605", "Database Systems", 3, "COMP 2100", "Core Courses", "Computer Science"),
            ("COMP 2606", "Software Engineering", 3, "COMP 2400", "Major Requirements", "Computer Science"),
            ("COMP 2611", "Data Structures II", 3, "COMP 1600", "Electives", "Computer Science"),
            ("MATH 2250", "Industrial Statistics", 3, "", "Electives", "Mathematics"),
            ("COMP 1201", "Object-Oriented Programming", 3, "COMP 1101", "Core Courses", "Computer Science"),
            ("COMP 1601", "Algorithms and Complexity", 3, "COMP 1600", "Core Courses", "Computer Science"),
            ("COMP 2201", "Web Application Development", 3, "COMP 1101", "Major Requirements", "Computer Science"),
            ("COMP 2301", "Computer Networks", 3, "COMP 1600", "Major Requirements", "Computer Science"),
            ("COMP 2501", "Software Testing and Quality Assurance", 3, "COMP 2400", "Major Requirements", "Computer Science"),
            ("COMP 2700", "Introduction to Artificial Intelligence", 3, "COMP 1600, MATH 2250", "Electives", "Computer Science"),
            ("COMP 2800", "Cybersecurity Fundamentals", 3, "COMP 1600", "Electives", "Computer Science"),
            ("COMP 3001", "Mobile Application Development", 3, "COMP 2400", "Major Requirements", "Computer Science"),
            ("COMP 3100", "Cloud Computing", 3, "COMP 2100", "Electives", "Computer Science"),
            ("COMP 3200", "Data Analytics", 3, "COMP 2100, MATH 2250", "Electives", "Computer Science"),
            ("MATH 1300", "Calculus I", 3, "", "General Education", "Mathematics"),
            ("MATH 2200", "Linear Algebra", 3, "", "General Education", "Mathematics"),
            ("STAT 2000", "Probability and Statistics", 3, "MATH 1200", "General Education", "Statistics"),
            ("ENGL 1000", "Academic Writing", 3, "", "General Education", "English"),
            ("PHYS 1100", "Introduction to Physics", 3, "", "General Education", "Physics"),
        )
        courses_by_code = {course.code: course for course in self.repo.list_courses()}
        for code, title, credits, prerequisites, category, department in catalog:
            if code not in courses_by_code:
                course = Course(
                    code=code,
                    title=title,
                    credits=credits,
                    prerequisite_text=prerequisites,
                    category=category,
                    department=department,
                )
                self.repo.db.add(course)
                courses_by_code[code] = course
            elif courses_by_code[code].category == "Core" or code in {
                "MATH 1200",
                "COMP 2400",
                "COMP 2510",
                "COMP 2606",
                "COMP 2611",
                "MATH 2250",
            }:
                courses_by_code[code].category = category
                courses_by_code[code].department = department
                self.repo.db.add(courses_by_code[code])
        self.repo.db.commit()

        bob = self.user_repo.get_by_username("bob")
        if bob:
            bob.name = bob.name or "Cameron Ramesar"
            bob.student_number = bob.student_number or "12345678"
            bob.degree_program = bob.degree_program or program.id
            self.repo.db.add(bob)
        advisor = self.user_repo.get_by_username("admin")
        if advisor and not advisor.name:
            advisor.name = "Dr. Williams"
            self.repo.db.add(advisor)
        self.repo.db.commit()

        if bob is None or bob.id is None:
            return
        for code, status, grade in (
            ("COMP 1101", "Completed", "A"),
            ("MATH 1200", "Completed", "A"),
            ("COMP 1600", "In Progress", ""),
        ):
            course = courses_by_code[code]
            existing = next(
                (
                    record
                    for record in self.repo.get_completed_courses(bob.id)
                    if record.course_id == course.id
                ),
                None,
            )
            if existing is None:
                self.repo.db.add(
                    StudentCourse(
                        student_id=bob.id,
                        course_id=course.id,
                        completion_status=status,
                        grade=grade,
                        completed_at=(
                            datetime.now(timezone.utc)
                            if status == "Completed"
                            else None
                        ),
                    )
                )
        self.repo.db.commit()

    def get_student_dashboard(
        self,
        student_id: int,
        semester_name: str | None = None,
    ) -> dict:
        student = self.user_repo.get_by_id(student_id)
        courses = self.repo.list_courses()
        records = self.repo.get_completed_courses(student_id)
        courses_by_id = {course.id: course for course in courses}
        completed_records = [
            record for record in records
            if record.completion_status.lower() == "completed"
        ]
        in_progress_records = [
            record for record in records
            if record.completion_status.lower() == "in progress"
        ]
        completed_ids = {record.course_id for record in completed_records}
        in_progress_ids = {record.course_id for record in in_progress_records}
        completed_courses = [
            courses_by_id[course_id] for course_id in completed_ids
            if course_id in courses_by_id
        ]
        in_progress_courses = [
            courses_by_id[course_id] for course_id in in_progress_ids
            if course_id in courses_by_id
        ]
        program = self.repo.get_degree_program(student.degree_program if student else None)
        total_credits = program.total_credits if program else DEFAULT_TOTAL_CREDITS
        completed_credits = sum(course.credits for course in completed_courses)
        in_progress_credits = sum(course.credits for course in in_progress_courses)
        remaining_credits = max(total_credits - completed_credits - in_progress_credits, 0)
        student_plans = self.repo.list_student_plans(student_id)
        selected_semester = (
            semester_name if semester_name in SEMESTER_OPTIONS else None
        )
        if selected_semester is None:
            latest_matching_plan = next(
                (
                    plan for plan in student_plans
                    if plan.semester_name in SEMESTER_OPTIONS
                ),
                None,
            )
            selected_semester = (
                latest_matching_plan.semester_name
                if latest_matching_plan
                else SEMESTER_OPTIONS[0]
            )
        current_plan = self.repo.get_plan_for_student(student_id, selected_semester)
        plan_course_ids = (
            {
                item.course_id for item in self.repo.get_plan_courses(current_plan.id)
            }
            if current_plan and current_plan.status != "Cancelled"
            else set()
        )
        planned_courses = [
            course for course in courses if course.id in plan_course_ids
        ]

        earned_by_category: dict[str, int] = {}
        for course in completed_courses:
            earned_by_category[course.category] = (
                earned_by_category.get(course.category, 0) + course.credits
            )
        category_progress = []
        if program:
            for requirement in self.repo.list_degree_requirements(program.id):
                earned = earned_by_category.get(requirement.category, 0)
                category_progress.append(
                    {
                        "category": requirement.category,
                        "earned": earned,
                        "required": requirement.required_credits,
                        "remaining": max(requirement.required_credits - earned, 0),
                        "percent": min(
                            round(earned / requirement.required_credits * 100),
                            100,
                        ) if requirement.required_credits else 0,
                    }
                )

        activity = []
        for record in records:
            course = courses_by_id.get(record.course_id)
            if course:
                activity.append(
                    {
                        "course": course,
                        "status": record.completion_status,
                        "grade": record.grade,
                        "completed_at": record.completed_at,
                    }
                )

        plan_messages = []
        for plan in self.repo.list_student_plans(student_id):
            advisor = (
                self.user_repo.get_by_id(plan.advisor_id)
                if plan.advisor_id is not None
                else None
            )
            plan_messages.append(
                {
                    "plan": plan,
                    "advisor_name": advisor.name or advisor.username
                    if advisor
                    else "MyAdvisor",
                    "message": plan.advisor_feedback
                    or f"Your {plan.semester_name} plan is {plan.status.lower()}.",
                }
            )

        semester_options = list(SEMESTER_OPTIONS)
        return {
            "student": student,
            "program": program,
            "courses": courses,
            "completed": completed_courses,
            "in_progress": in_progress_courses,
            "current_plan": current_plan,
            "planned_courses": planned_courses,
            "selected_course_ids": plan_course_ids,
            "completed_credits": completed_credits,
            "in_progress_credits": in_progress_credits,
            "remaining_credits": remaining_credits,
            "total_credits": total_credits,
            "progress_percent": min(round(completed_credits / total_credits * 100), 100)
            if total_credits else 0,
            "category_progress": category_progress,
            "activity": activity[:5],
            "plan_messages": plan_messages,
            "selected_semester": selected_semester,
            "semester_options": semester_options,
            "can_edit_plan": bool(
                current_plan
                and (
                    current_plan.status in RESUBMITTABLE_PLAN_STATUSES
                    or current_plan.status == "Cancelled"
                )
            ),
        }

    def get_degree_progress(self, student_id: int) -> DegreeProgressResponse:
        """Project the existing dashboard calculation onto a public allowlist."""
        return DegreeProgressResponse.model_validate(
            self.get_student_dashboard(student_id)
        )

    def get_course_catalogue(self, student_id: int) -> list[CourseSelectionResponse]:
        """Use the same catalogue and eligibility rules as HTML course selection."""
        availability = self.get_course_availability(student_id)
        return [
            CourseSelectionResponse(
                **course.model_dump(),
                eligible=availability[course.id][0],
                eligibility_reason=availability[course.id][1],
            )
            for course in self.repo.list_courses()
        ]

    def get_course_availability(self, student_id: int) -> dict[int, tuple[bool, str]]:
        completed_ids = self.repo.get_completed_course_ids(student_id)
        in_progress_ids = {
            record.course_id
            for record in self.repo.get_completed_courses(student_id)
            if record.completion_status.lower() == "in progress"
        }
        completed_codes = {
            course.code: course.id for course in self.repo.list_courses()
        }
        availability = {}
        for course in self.repo.list_courses():
            if course.id in completed_ids:
                availability[course.id] = (False, "Already completed")
                continue
            if course.id in in_progress_ids:
                availability[course.id] = (False, "Already in progress")
                continue
            unmet = [
                code.strip()
                for code in course.prerequisite_text.split(",")
                if code.strip()
                and completed_codes.get(code.strip()) not in completed_ids
            ]
            if unmet:
                availability[course.id] = (
                    False,
                    f"Missing prerequisite(s): {', '.join(unmet)}",
                )
            else:
                availability[course.id] = (True, "Eligible")
        return availability

    def submit_plan(
        self,
        student_id: int,
        selected_course_ids: list[int],
        semester_name: str,
    ) -> SemesterPlan:
        semester_name = semester_name.strip()
        if semester_name not in SEMESTER_OPTIONS:
            raise PlanValidationError(
                "Choose a valid year and semester before submitting a plan."
            )
        if not selected_course_ids:
            raise PlanValidationError("Select at least one course for the semester plan.")
        if len(set(selected_course_ids)) != len(selected_course_ids):
            raise PlanValidationError("A course may only appear once in a semester plan.")
        availability = self.get_course_availability(student_id)
        for course_id in selected_course_ids:
            course = self.repo.get_course_by_id(course_id)
            if course is None:
                raise PlanValidationError(f"Course ID {course_id} is no longer available.")
            eligible, reason = availability[course_id]
            if not eligible:
                raise PlanValidationError(f"{course.code}: {reason}.")

        existing_plan = self.repo.get_plan_for_student(student_id, semester_name)
        if existing_plan:
            if existing_plan.status in RESUBMITTABLE_PLAN_STATUSES:
                return self.repo.resubmit_plan(existing_plan, selected_course_ids)
            if existing_plan.status != "Cancelled":
                raise PlanConflictError(
                    "A plan for this semester is already under review or approved."
                )
        return self.repo.create_plan(
            student_id,
            selected_course_ids,
            semester_name=semester_name,
        )

    def get_student_plan(self, student_id: int, plan_id: int) -> SemesterPlan:
        plan = self.repo.get_plan_by_id(plan_id)
        if plan is None or plan.student_id != student_id:
            raise PlanNotFoundError("Plan not found.")
        return plan

    def plan_response(self, plan: SemesterPlan) -> SemesterPlanResponse:
        return SemesterPlanResponse(
            # Attribute access reloads a plan expired by a repository commit.
            id=plan.id,
            semester_name=plan.semester_name,
            status=plan.status,
            submitted_at=plan.submitted_at,
            advisor_feedback=plan.advisor_feedback,
            courses=[
                self.repo.get_course_by_id(item.course_id)
                for item in self.repo.get_plan_courses(plan.id)
            ],
        )

    def list_semester_plans(self, student_id: int) -> list[SemesterPlanResponse]:
        return [
            self.plan_response(plan)
            for plan in self.repo.list_student_plans(student_id)
        ]

    def get_semester_plan(self, student_id: int, plan_id: int) -> SemesterPlanResponse:
        return self.plan_response(self.get_student_plan(student_id, plan_id))

    def submit_semester_plan(
        self, student_id: int, course_ids: list[int], semester_name: str,
    ) -> tuple[SemesterPlanResponse, bool]:
        """Use the form submission rules, reporting whether a resource was created."""
        previous = self.repo.get_plan_for_student(student_id, semester_name.strip())
        plan = self.submit_plan(student_id, course_ids, semester_name)
        created = previous is None or previous.id != plan.id
        return self.plan_response(plan), created

    def revise_plan(
        self, student_id: int, plan_id: int, course_ids: list[int],
    ) -> SemesterPlan:
        plan = self.get_student_plan(student_id, plan_id)
        if plan.status not in RESUBMITTABLE_PLAN_STATUSES:
            raise PlanConflictError(
                "Only rejected plans or plans with changes requested can be revised."
            )
        latest = self.repo.get_plan_for_student(student_id, plan.semester_name)
        if latest.id != plan.id:
            raise PlanConflictError("Only the latest plan for a semester can be revised.")
        return self.submit_plan(student_id, course_ids, plan.semester_name)

    def remove_submitted_course(
        self,
        student_id: int,
        plan_id: int,
        course_id: int,
    ) -> SemesterPlan:
        plan = self.get_student_plan(student_id, plan_id)
        if plan.status != "Pending":
            raise PlanConflictError("Only courses in pending plans can be removed.")

        plan_courses = self.repo.get_plan_courses(plan.id)
        plan_course = next(
            (item for item in plan_courses if item.course_id == course_id),
            None,
        )
        if plan_course is None:
            raise PlanNotFoundError("That course is not part of this plan.")
        if len(plan_courses) == 1:
            raise PlanConflictError("Cancel the semester plan to remove its last course.")
        self.repo.remove_plan_course(plan_course)
        return plan

    def cancel_plan(self, student_id: int, plan_id: int) -> SemesterPlan:
        plan = self.get_student_plan(student_id, plan_id)
        if plan.status not in {"Pending", "Rejected", "Approved"}:
            raise PlanConflictError(
                "Only pending, rejected, or approved plans can be cancelled."
            )
        return self.repo.cancel_plan(plan)

    def get_advisor_dashboard(self, advisor_id: int) -> list[dict]:
        del advisor_id
        pending_plans = self.repo.list_pending_plans()
        plans = []
        for plan in pending_plans:
            student = self.user_repo.get_by_id(plan.student_id)
            program = self.repo.get_degree_program(
                student.degree_program if student else None
            )
            courses = [
                course
                for item in self.repo.get_plan_courses(plan.id)
                if (course := self.repo.get_course_by_id(item.course_id)) is not None
            ]
            plans.append(
                {
                    "plan": plan,
                    "student": student,
                    "program": program,
                    "courses": courses,
                }
            )
        return plans

    def advisor_plan_response(self, plan: SemesterPlan) -> AdvisorPlanResponse:
        student = self.user_repo.get_by_id(plan.student_id)
        return AdvisorPlanResponse(
            **self.plan_response(plan).model_dump(),
            advisor_id=plan.advisor_id,
            student=student,
            program=self.repo.get_degree_program(
                student.degree_program if student else None
            ),
        )

    def list_advisor_plans(self, advisor_id: int) -> list[AdvisorPlanResponse]:
        """Expose the same shared pending queue as the advisor dashboard."""
        return [
            self.advisor_plan_response(item["plan"])
            for item in self.get_advisor_dashboard(advisor_id)
        ]

    def get_advisor_plan(self, plan_id: int) -> AdvisorPlanResponse:
        plan = self.repo.get_plan_by_id(plan_id)
        if plan is None:
            raise PlanNotFoundError("Plan not found.")
        return self.advisor_plan_response(plan)

    def get_advisor_overview(self, advisor_id: int) -> dict:
        students = [
            user for user in self.user_repo.get_all_users()
            if user.role == "regular_user"
        ]
        all_plans = self.repo.list_all_plans()
        pending_plans = [
            plan for plan in all_plans if plan.status == "Pending"
        ]
        reviewed_plans = [
            plan
            for plan in all_plans
            if plan.advisor_id == advisor_id and plan.status != "Pending"
        ]
        plan_status_counts = {
            status: sum(plan.status == status for plan in all_plans)
            for status in ("Approved", "Rejected", "Changes Requested")
        }
        reviewed_activity = []
        for plan in reviewed_plans[:10]:
            student = self.user_repo.get_by_id(plan.student_id)
            reviewed_activity.append(
                {
                    "plan": plan,
                    "student": student,
                    "student_name": (
                        student.name or student.username
                        if student
                        else "Student account unavailable"
                    ),
                    "message": plan.advisor_feedback
                    or f"Plan {plan.status.lower()} for {plan.semester_name}.",
                }
            )

        return {
            "student_count": len(students),
            "pending_count": len(pending_plans),
            "reviewed_count": len(reviewed_plans),
            "approved_count": plan_status_counts["Approved"],
            "rejected_count": plan_status_counts["Rejected"],
            "changes_requested_count": plan_status_counts["Changes Requested"],
            "pending_plans": self.get_advisor_dashboard(advisor_id)[:5],
            "reviewed_activity": reviewed_activity,
        }

    def review_plan(
        self,
        plan_id: int,
        decision: str,
        feedback: str,
        advisor_id: int,
    ) -> SemesterPlan:
        decisions = {
            "approve": "Approved",
            "reject": "Rejected",
            "request_changes": "Changes Requested",
        }
        if decision not in decisions:
            raise PlanValidationError("Choose approve, reject, or request changes.")
        if len(feedback) > 500:
            raise PlanValidationError("Advisor feedback must be 500 characters or fewer.")
        plan = self.repo.get_plan_by_id(plan_id)
        if not plan:
            raise PlanNotFoundError("Plan not found.")
        if plan.status != "Pending":
            raise PlanConflictError("Only pending plans can be reviewed.")
        reviewed = self.repo.update_plan(
            plan,
            status=decisions[decision],
            feedback=feedback.strip(),
            advisor_id=advisor_id,
            expected_status="Pending",
        )
        if reviewed is None:
            raise PlanConflictError("Only pending plans can be reviewed.")
        return reviewed

    def prerequisite_ok(self, student_id: int, course_id: int) -> bool:
        course = self.repo.get_course_by_id(course_id)
        if not course:
            return False
        tracked_ids = {
            record.course_id
            for record in self.repo.get_completed_courses(student_id)
            if record.completion_status.lower() in {"completed", "in progress"}
        }
        if course_id in tracked_ids:
            return False
        if not course.prerequisite_text:
            return True
        completed_ids = self.repo.get_completed_course_ids(student_id)
        catalog = {item.code: item.id for item in self.repo.list_courses()}
        requirement_codes = [
            code.strip()
            for code in course.prerequisite_text.split(",")
            if code.strip()
        ]
        return all(
            catalog.get(code) in completed_ids for code in requirement_codes
        )

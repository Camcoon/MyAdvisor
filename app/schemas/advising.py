"""Public request and response allowlists for advising APIs."""

from datetime import datetime
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field


class CourseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    code: str
    title: str
    credits: int = Field(ge=0)
    category: str
    department: str
    prerequisite_text: str


class CourseSelectionResponse(CourseResponse):
    eligible: bool
    eligibility_reason: str


class DegreeProgramResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    total_credits: int = Field(ge=0)


class CategoryProgressResponse(BaseModel):
    category: str
    earned: int = Field(ge=0)
    required: int = Field(ge=0)
    remaining: int = Field(ge=0)
    percent: int = Field(ge=0, le=100)


class DegreeProgressResponse(BaseModel):
    program: DegreeProgramResponse | None
    total_credits: int = Field(ge=0)
    completed_credits: int = Field(ge=0)
    in_progress_credits: int = Field(ge=0)
    remaining_credits: int = Field(ge=0)
    progress_percent: int = Field(ge=0, le=100)
    category_progress: list[CategoryProgressResponse]
    completed: list[CourseResponse]
    in_progress: list[CourseResponse]


class PlanCoursesRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    course_ids: list[Annotated[int, Field(strict=True, gt=0, le=2**63 - 1)]] = Field(
        min_length=1
    )


class SemesterPlanRequest(PlanCoursesRequest):
    semester_name: str


class SemesterPlanResponse(BaseModel):
    id: int
    semester_name: str
    status: Literal["Pending", "Approved", "Rejected", "Changes Requested", "Cancelled"]
    submitted_at: datetime
    advisor_feedback: str
    courses: list[CourseResponse]


class PlanFeedbackRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    feedback: str = Field(default="", strict=True, max_length=500)


class PlanReviewRequest(PlanFeedbackRequest):
    decision: str = Field(
        strict=True, description="approve, reject, or request_changes"
    )


class AdvisorStudentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    username: str
    student_number: str | None


class AdvisorPlanResponse(SemesterPlanResponse):
    advisor_id: int | None
    student: AdvisorStudentResponse | None
    program: DegreeProgramResponse | None

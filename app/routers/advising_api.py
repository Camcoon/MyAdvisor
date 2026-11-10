from typing import Annotated

from fastapi import Depends, HTTPException, Path, Request, Response
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app.dependencies.auth import AdminDep, StudentDep
from app.dependencies.session import SessionDep
from app.schemas.advising import (
    AdvisorPlanResponse,
    CourseSelectionResponse,
    DegreeProgressResponse,
    PlanCoursesRequest,
    PlanFeedbackRequest,
    PlanReviewRequest,
    SemesterPlanRequest,
    SemesterPlanResponse,
)
from app.services.advising_errors import (
    PlanConflictError,
    PlanNotFoundError,
    PlanValidationError,
)
from app.services.advising_service import AdvisingService

from . import api_router


@api_router.get("/degree-progress", response_model=DegreeProgressResponse)
def degree_progress(user: StudentDep, db: SessionDep, response: Response):
    """Return degree progress for the authenticated student."""
    response.headers["Cache-Control"] = "no-store"
    return AdvisingService(db).get_degree_progress(user.id)


@api_router.get("/courses", response_model=list[CourseSelectionResponse])
def courses(user: StudentDep, db: SessionDep, response: Response):
    """Return the shared catalogue with this student's selection eligibility."""
    response.headers["Cache-Control"] = "no-store"
    return AdvisingService(db).get_course_catalogue(user.id)


def plan_service(db: SessionDep, response: Response):
    """Translate domain errors and roll back failed API operations.

    Repository writes own their commits; create/resubmit commit the plan and all
    course rows together. Do not begin a nested transaction after auth's reads.
    """
    response.headers["Cache-Control"] = "no-store"
    try:
        yield AdvisingService(db)
    except (PlanValidationError, PlanNotFoundError, PlanConflictError) as exc:
        db.rollback()
        status_code, code = {
            PlanValidationError: (422, "invalid_plan"),
            PlanNotFoundError: (404, "not_found"),
            PlanConflictError: (409, "plan_conflict"),
        }[type(exc)]
        raise HTTPException(
            status_code=status_code,
            detail={"code": code, "message": str(exc)},
            headers={"Cache-Control": "no-store"},
        ) from exc
    except SQLAlchemyError as exc:
        db.rollback()
        conflict = isinstance(exc, IntegrityError)
        raise HTTPException(
            status_code=409 if conflict else 503,
            detail={
                "code": "plan_conflict" if conflict else "database_unavailable",
                "message": (
                    "The plan could not be saved because of a data conflict."
                    if conflict
                    else "The plan operation could not be completed. Try again later."
                ),
            },
            headers={"Cache-Control": "no-store"},
        ) from exc


PlanServiceDep = Annotated[AdvisingService, Depends(plan_service)]
ResourceId = Annotated[int, Path(gt=0, le=2**63 - 1)]


@api_router.get("/semester-plans", response_model=list[SemesterPlanResponse])
def semester_plans(user: StudentDep, service: PlanServiceDep):
    """List only the authenticated student's plans, newest first."""
    return service.list_semester_plans(user.id)


@api_router.get("/semester-plans/{plan_id}", response_model=SemesterPlanResponse)
def semester_plan(plan_id: ResourceId, user: StudentDep, service: PlanServiceDep):
    """Return an owned plan; missing and foreign plans both return 404."""
    return service.get_semester_plan(user.id, plan_id)


@api_router.post(
    "/semester-plans",
    response_model=SemesterPlanResponse,
    status_code=201,
    responses={
        200: {"model": SemesterPlanResponse, "description": "Existing plan resubmitted"}
    },
)
def submit_semester_plan(
    payload: SemesterPlanRequest,
    user: StudentDep,
    service: PlanServiceDep,
    request: Request,
    response: Response,
):
    """Submit eligible selections, reusing a resubmittable plan if present."""
    plan, created = service.submit_semester_plan(
        user.id,
        payload.course_ids,
        payload.semester_name,
    )
    response.status_code = 201 if created else 200
    response.headers["Location"] = str(
        request.url_for("semester_plan", plan_id=plan.id)
    )
    return plan


@api_router.put(
    "/semester-plans/{plan_id}/courses", response_model=SemesterPlanResponse
)
def revise_semester_plan(
    plan_id: ResourceId,
    payload: PlanCoursesRequest,
    user: StudentDep,
    service: PlanServiceDep,
):
    """Replace selections and resubmit a rejected or changes-requested plan."""
    return service.plan_response(
        service.revise_plan(user.id, plan_id, payload.course_ids)
    )


@api_router.delete(
    "/semester-plans/{plan_id}/courses/{course_id}",
    response_model=SemesterPlanResponse,
)
def remove_semester_plan_course(
    plan_id: ResourceId,
    course_id: ResourceId,
    user: StudentDep,
    service: PlanServiceDep,
):
    """Remove a course from a pending plan, retaining at least one course."""
    return service.plan_response(
        service.remove_submitted_course(user.id, plan_id, course_id)
    )


@api_router.delete("/semester-plans/{plan_id}", response_model=SemesterPlanResponse)
def cancel_semester_plan(
    plan_id: ResourceId, user: StudentDep, service: PlanServiceDep
):
    """Cancel a permitted plan while retaining its history and course rows."""
    return service.plan_response(service.cancel_plan(user.id, plan_id))


@api_router.get("/advisor/plans", response_model=list[AdvisorPlanResponse])
def advisor_plans(user: AdminDep, service: PlanServiceDep):
    """List the shared pending queue available in the advisor dashboard."""
    return service.list_advisor_plans(user.id)


@api_router.get("/advisor/plans/{plan_id}", response_model=AdvisorPlanResponse)
def advisor_plan(plan_id: ResourceId, user: AdminDep, service: PlanServiceDep):
    """View a submitted plan and its current review status."""
    return service.get_advisor_plan(plan_id)


@api_router.post("/advisor/plans/{plan_id}/review", response_model=AdvisorPlanResponse)
def review_advisor_plan(
    plan_id: ResourceId,
    payload: PlanReviewRequest,
    user: AdminDep,
    service: PlanServiceDep,
):
    """Apply an existing review decision to a pending plan."""
    return service.advisor_plan_response(
        service.review_plan(plan_id, payload.decision, payload.feedback, user.id)
    )


@api_router.post("/advisor/plans/{plan_id}/approve", response_model=AdvisorPlanResponse)
def approve_advisor_plan(
    plan_id: ResourceId,
    payload: PlanFeedbackRequest,
    user: AdminDep,
    service: PlanServiceDep,
):
    return service.advisor_plan_response(
        service.review_plan(plan_id, "approve", payload.feedback, user.id)
    )


@api_router.post("/advisor/plans/{plan_id}/reject", response_model=AdvisorPlanResponse)
def reject_advisor_plan(
    plan_id: ResourceId,
    payload: PlanFeedbackRequest,
    user: AdminDep,
    service: PlanServiceDep,
):
    return service.advisor_plan_response(
        service.review_plan(plan_id, "reject", payload.feedback, user.id)
    )


@api_router.post(
    "/advisor/plans/{plan_id}/request-changes", response_model=AdvisorPlanResponse
)
def request_advisor_plan_changes(
    plan_id: ResourceId,
    payload: PlanFeedbackRequest,
    user: AdminDep,
    service: PlanServiceDep,
):
    return service.advisor_plan_response(
        service.review_plan(plan_id, "request_changes", payload.feedback, user.id)
    )

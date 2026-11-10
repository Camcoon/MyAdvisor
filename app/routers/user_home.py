from typing import Annotated

from fastapi import Form, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse

from app.dependencies.auth import AuthDep, StudentDep
from app.dependencies.session import SessionDep
from app.services.advising_service import AdvisingService
from app.utilities.flash import flash

from . import router, templates


@router.get("/app", response_class=HTMLResponse, name="user_home_view")
async def user_home_view(
    request: Request,
    user: AuthDep,
    db: SessionDep,
    semester: str | None = None,
    tab: str = "home",
):
    valid_tabs = (
        {"home", "messages", "profile"}
        if user.role == "admin"
        else {"home", "degree-progress", "plan-courses", "messages", "profile"}
    )
    active_tab = tab if tab in valid_tabs else "home"
    service = AdvisingService(db)
    if user.role == "admin":
        advisor_dashboard = service.get_advisor_overview(user.id)
        dashboard = None
        catalog_items = []
        departments = []
    else:
        advisor_dashboard = None
        dashboard = service.get_student_dashboard(user.id, semester)
        availability = service.get_course_availability(user.id)
        catalog_items = [
            {
                "course": course,
                "eligible": availability[course.id][0],
                "eligibility_message": availability[course.id][1],
            }
            for course in dashboard["courses"]
        ]
        departments = sorted({item["course"].department for item in catalog_items})
    return templates.TemplateResponse(
        request=request,
        name="myadvisor_dashboard.html",
        context={
            "user": user,
            "dashboard": dashboard,
            "catalog_items": catalog_items,
            "departments": departments,
            "active_tab": active_tab,
            "advisor_dashboard": advisor_dashboard,
        },
    )


@router.post("/app/plan", response_class=HTMLResponse, name="submit_plan")
async def submit_plan(
    request: Request,
    user: StudentDep,
    db: SessionDep,
    course_ids: Annotated[list[int] | None, Form()] = None,
    semester_name: Annotated[str, Form()] = "",
):
    service = AdvisingService(db)
    try:
        service.submit_plan(user.id, course_ids or [], semester_name)
    except ValueError as exc:
        flash(request, str(exc), "warning")
        return RedirectResponse(
            url=request.url_for("user_home_view").include_query_params(
                semester=semester_name,
                tab="plan-courses",
            ),
            status_code=status.HTTP_303_SEE_OTHER,
        )

    flash(request, "Semester plan submitted for advisor review.", "success")
    return RedirectResponse(
        url=request.url_for("user_home_view").include_query_params(
            semester=semester_name,
            tab="plan-courses",
        ),
        status_code=status.HTTP_303_SEE_OTHER,
    )


@router.post(
    "/app/plan/{plan_id}/courses/{course_id}/remove",
    name="remove_submitted_course",
)
async def remove_submitted_course(
    request: Request,
    user: StudentDep,
    db: SessionDep,
    plan_id: int,
    course_id: int,
):
    service = AdvisingService(db)
    try:
        plan = service.remove_submitted_course(user.id, plan_id, course_id)
    except ValueError as exc:
        flash(request, str(exc), "warning")
        return RedirectResponse(
            url=request.url_for("user_home_view").include_query_params(
                tab="plan-courses",
            ),
            status_code=status.HTTP_303_SEE_OTHER,
        )

    flash(request, "Course removed from the submitted plan.", "success")
    return RedirectResponse(
        url=request.url_for("user_home_view").include_query_params(
            semester=plan.semester_name,
            tab="plan-courses",
        ),
        status_code=status.HTTP_303_SEE_OTHER,
    )


@router.post("/app/plan/{plan_id}/cancel", name="cancel_plan")
async def cancel_plan(
    request: Request,
    user: StudentDep,
    db: SessionDep,
    plan_id: int,
):
    service = AdvisingService(db)
    try:
        plan = service.cancel_plan(user.id, plan_id)
    except ValueError as exc:
        flash(request, str(exc), "warning")
        return RedirectResponse(
            url=request.url_for("user_home_view").include_query_params(
                tab="plan-courses",
            ),
            status_code=status.HTTP_303_SEE_OTHER,
        )

    flash(request, "Semester plan cancelled. You can edit it and resubmit.", "success")
    return RedirectResponse(
        url=request.url_for("user_home_view").include_query_params(
            semester=plan.semester_name,
            tab="plan-courses",
        ),
        status_code=status.HTTP_303_SEE_OTHER,
    )

import json

from fastapi import HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse

from app.dependencies.auth import AdminDep
from app.dependencies.session import SessionDep
from app.services.advising_service import AdvisingService
from app.utilities.flash import flash

from . import router, templates


@router.get("/admin", response_class=HTMLResponse, name="admin_home_view")
async def admin_home_view(request: Request, user: AdminDep, db: SessionDep):
    service = AdvisingService(db)
    return templates.TemplateResponse(
        request=request,
        name="advisor_dashboard.html",
        context={
            "user": user,
            "plans": service.get_advisor_dashboard(user.id),
            "active_tab": "advisor-review",
        },
    )


@router.post(
    "/admin/review/{plan_id}",
    response_class=HTMLResponse,
    name="review_plan",
)
async def review_plan(
    request: Request,
    user: AdminDep,
    db: SessionDep,
    plan_id: int,
):
    content_type = request.headers.get("content-type", "").split(";", 1)[0].strip().lower()
    if content_type == "application/json":
        try:
            payload = await request.json()
        except json.JSONDecodeError as exc:
            raise HTTPException(status_code=400, detail="Invalid JSON request body.") from exc
        if not isinstance(payload, dict):
            raise HTTPException(status_code=422, detail="The review payload must be a JSON object.")
    else:
        payload = await request.form()

    decision = payload.get("decision")
    feedback = payload.get("feedback", "")
    if not isinstance(decision, str) or not decision:
        raise HTTPException(
            status_code=422,
            detail=[{
                "type": "missing",
                "loc": ["body", "decision"],
                "msg": "Field required",
                "input": None,
            }],
        )
    if not isinstance(feedback, str):
        raise HTTPException(
            status_code=422,
            detail="Feedback must be a string.",
        )

    service = AdvisingService(db)
    try:
        service.review_plan(plan_id, decision, feedback, user.id)
    except ValueError as exc:
        flash(request, str(exc), "warning")
        return RedirectResponse(
            url=request.url_for("admin_home_view"),
            status_code=status.HTTP_303_SEE_OTHER,
        )

    messages = {
        "approve": "Plan approved.",
        "reject": "Plan rejected.",
        "request_changes": "Changes requested. The student can revise and resubmit this plan.",
    }
    flash(request, messages[decision], "success")
    return RedirectResponse(
        url=request.url_for("admin_home_view"),
        status_code=status.HTTP_303_SEE_OTHER,
    )

"""Plan errors remain ValueErrors for the existing HTML form handlers."""


class PlanValidationError(ValueError):
    pass


class PlanNotFoundError(ValueError):
    pass


class PlanConflictError(ValueError):
    pass

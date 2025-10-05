from fastapi import APIRouter, FastAPI


def add_routers(
    app: FastAPI,
    routes: list[APIRouter],
    api_version: str = "v1",
    redirect_slashes: bool = False,
) -> None:
    """Include the declared API routers into the global versioned application router."""
    app.router.redirect_slashes = redirect_slashes
    prefix = f"/{api_version}"

    for route in routes:
        app.include_router(route, prefix=prefix)

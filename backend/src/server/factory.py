from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.core.fastapi.exceptions.handlers import init_error_handlers
from src.core.fastapi.routing import add_routers
from src.core.fastapi.openapi import apply_openapi_schema
from src.modules.cbtracking.infrastructure.api import (
    cbtracking_api_router,
    endpoints as cbtracking_endpoints,
)

from .containers import Container


def create_app() -> tuple[FastAPI, Container]:
    """Build the FastAPi application instance."""

    container = Container()
    container.wire(modules=[cbtracking_endpoints])

    wsconfig = container.config
    debug: bool = wsconfig.server_debug()
    root_path: str = wsconfig.server_api_root_path()

    fastapi_app = FastAPI(
        debug=debug,
        title=wsconfig.sui_page_title(),
        description=wsconfig.sui_description(),
        root_path=f"/{root_path}",
    )

    fastapi_app.mount("/static", StaticFiles(directory="static"), name="static")
    fastapi_app.__setattr__("container", container)
    fastapi_app.__setattr__("openapi", apply_openapi_schema(fastapi_app, wsconfig))

    add_routers(
        fastapi_app,
        [cbtracking_api_router],
        api_version=wsconfig.server_api_root_version(),
    )

    init_error_handlers(fastapi_app, wsconfig.server_sysadmin_contact())

    return fastapi_app, container


app, container = create_app()

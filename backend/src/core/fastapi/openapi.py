from typing import Any
from collections.abc import Callable

from dependency_injector.providers import Configuration
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi


def apply_openapi_schema(
    app: FastAPI, config: Configuration
) -> Callable[..., dict[str, Any]]:
    """Generate the callable that applies the custom parameters for the OpenAPI UI."""

    def custom_openapi():
        """Override the default schema building for both /docs and /redoc."""
        if app.openapi_schema:
            return app.openapi_schema

        title: str = config.sui_page_title()
        version: str = config.sui_api_version()
        summary: str = config.sui_summary()
        description: str = config.sui_description()
        hostname: str = config.server_hostname()
        port: int = config.server_port()

        base_url = f"http://{'localhost' if hostname == '0.0.0.0' else hostname}:{port}/{config.server_api_root_path()}"

        openapi_schema = get_openapi(
            title=title,
            version=version,
            summary=summary,
            description=description,
            routes=app.routes,
            servers=[
                {
                    "description": "Development",
                    "url": base_url,
                }
            ],
        )

        openapi_schema["info"]["x-logo"] = {
            "url": f"{base_url}/{config.sui_redoc_logo_path()}",
            "altText": config.sui_redoc_logo_alt_text(),
            "backgroundColor": config.sui_redoc_logo_background_color(),
            "href": config.sui_redoc_redoc_logo.href(),
            "width": config.sui_redoc_logo_width(),
            "height": config.sui_redoc_logo_height(),
        }

        return openapi_schema

    return custom_openapi

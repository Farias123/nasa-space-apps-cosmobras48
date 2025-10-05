from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Configuration


def _build_db_config(config: Configuration) -> None:
    config.db_engine.from_env("DB_ENGINE", as_=str, default="mongodb")
    config.db_name.from_env("DB_NAME", as_=str, default="cosmobras48_db")
    config.db_host.from_env("DB_HOSTNAME", as_=str, default="0.0.0.0")
    config.db_username.from_env("DB_USERNAME", as_=str, required=True)
    config.db_password.from_env("DB_PASSWORD", as_=str, required=True)
    config.db_port.from_env("DB_PORT", as_=int, default=21017)


def _build_server_config(config: Configuration) -> None:
    config.server_hostname.from_env("SERVER_HOSTNAME", as_=str, default="0.0.0.0")
    config.server_debug.from_env("SERVER_DEBUG", as_=bool, default=True)
    config.server_port.from_env("SERVER_PORT", as_=int, default=8001)
    config.server_log_level.from_env("SERVER_LOG_LEVEL", as_=str, default="info")
    config.server_api_root_path.from_env("SERVER_API_ROOT_PATH", as_=str, default="api")
    config.server_api_root_version.from_env(
        "SERVER_API_ROOT_VERSION", as_=str, default="v1"
    )
    config.server_sysadmin_contact.from_env("SERVER_SYSADMIN_CONTACT", as_=str)


def _build_swagger_ui_config(config: Configuration) -> None:
    config.sui_api_version.from_env("SWAGGER_UI_API_VERSION", as_=str, default="1.0.0")
    config.sui_tab_title.from_env("SWAGGER_UI_TAB_TITLE", as_=str, required=True)
    config.sui_page_title.from_env("SWAGGER_UI_PAGE_TITLE", as_=str, required=True)
    config.sui_summary.from_env("SWAGGER_UI_SUMMARY", as_=str, required=True)
    config.sui_description.from_env("SWAGGER_UI_DESCRIPTION", as_=str, required=True)
    config.sui_redoc_logo_path.from_env(
        "SWAGGER_UI_REDOC_LOGO_PATH", as_=str, required=True
    )
    config.sui_redoc_logo_alt_text.from_env(
        "SWAGGER_UI_REDOC_LOGO_ALT_TEXT", as_=str, required=True
    )
    config.sui_redoc_logo_background_color.from_env(
        "SWAGGER_UI_REDOC_LOGO_BACKGROUND_COLOR", as_=str, required=True
    )
    config.sui_redoc_logo_href.from_env(
        "SWAGGER_UI_REDOC_LOGO_HREF", as_=str, required=True
    )
    config.sui_redoc_logo_width.from_env(
        "SWAGGER_UI_REDOC_LOGO_WIDTH", as_=str, required=True
    )
    config.sui_redoc_logo_height.from_env(
        "SWAGGER_UI_REDOC_LOGO_HEIGHT", as_=str, required=True
    )


class Container(DeclarativeContainer):
    config = Configuration()

    _build_db_config(config)
    _build_server_config(config)
    _build_swagger_ui_config(config)

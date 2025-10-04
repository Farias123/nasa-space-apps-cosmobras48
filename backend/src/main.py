import uvicorn

from src.server import container


if __name__ == "__main__":
    wsconfig = container.config

    uvicorn.run(
        "src.server:app",
        host=wsconfig.server_hostname(),
        port=wsconfig.server_port(),
        log_level=wsconfig.server_log_level(),
        reload=wsconfig.server_debug(),
    )

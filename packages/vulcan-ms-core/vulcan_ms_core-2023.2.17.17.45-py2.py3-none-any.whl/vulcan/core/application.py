import os
import shutil
from typing import Awaitable, Callable, List

from fastapi import FastAPI, Request
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

# from opentelemetry.instrumentation.aio_pika import AioPikaInstrumentor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from opentelemetry.sdk.resources import (
    DEPLOYMENT_ENVIRONMENT,
    SERVICE_NAME,
    TELEMETRY_SDK_LANGUAGE,
    Resource,
)

# from opentelemetry.sdk.trace import TracerProvider
# from opentelemetry.sdk.trace.export import BatchSpanProcessor
# from opentelemetry.trace import set_tracer_provider
from prometheus_fastapi_instrumentator.instrumentation import (
    PrometheusFastApiInstrumentator,
)

from vulcan.core.config import config
from vulcan.core.db import db_core
from vulcan.core.exceptions import CustomException
from vulcan.core.fastapi.middlewares import ResponseLogMiddleware
from vulcan.core.helpers.cache import Cache, RedisBackend, CustomKeyMaker

# def setup_opentelemetry(app: FastAPI) -> None:  # pragma: no cover
#     """
#     Enables opentelemetry instrumentation.

#     :param app: current application.
#     """
#     if not settings.opentelemetry_endpoint:
#         return

#     tracer_provider = TracerProvider(
#         resource=Resource(
#             attributes={
#                 SERVICE_NAME: "ms_portfolio",
#                 TELEMETRY_SDK_LANGUAGE: "python",
#                 DEPLOYMENT_ENVIRONMENT: config.ENV,
#             },
#         ),
#     )

#     tracer_provider.add_span_processor(
#         BatchSpanProcessor(
#             OTLPSpanExporter(
#                 endpoint=settings.opentelemetry_endpoint,
#                 insecure=True,
#             ),
#         ),
#     )

#     excluded_endpoints = [
#         app.url_path_for("health_check"),
#         app.url_path_for("openapi"),
#         app.url_path_for("swagger_ui_html"),
#         app.url_path_for("swagger_ui_redirect"),
#         app.url_path_for("redoc_html"),
#         "/metrics",
#     ]

#     FastAPIInstrumentor().instrument_app(
#         app,
#         tracer_provider=tracer_provider,
#         excluded_urls=",".join(excluded_endpoints),
#     )
#     SQLAlchemyInstrumentor().instrument(
#         tracer_provider=tracer_provider,
#         engine=app.state.db_engine.sync_engine,
#     )
#     # AioPikaInstrumentor().instrument(
#     #     tracer_provider=tracer_provider,
#     # )

#     set_tracer_provider(tracer_provider=tracer_provider)


# def stop_opentelemetry(app: FastAPI) -> None:  # pragma: no cover
#     """
#     Disables opentelemetry instrumentation.

#     :param app: current application.
#     """
#     if not settings.opentelemetry_endpoint:
#         return

#     FastAPIInstrumentor().uninstrument_app(app)
#     SQLAlchemyInstrumentor().uninstrument()
#     # AioPikaInstrumentor().uninstrument()


def init_listeners(app_: FastAPI) -> None:
    # Exception handler
    @app_.exception_handler(CustomException)
    async def custom_exception_handler(request: Request, exc: CustomException):
        return JSONResponse(
            status_code=exc.code,
            content={"error_code": exc.error_code, "message": exc.message},
        )


def on_auth_error(request: Request, exc: Exception):
    status_code, error_code, message = 401, None, str(exc)
    if isinstance(exc, CustomException):
        status_code = int(exc.code)
        error_code = exc.error_code
        message = exc.message

    return JSONResponse(
        status_code=status_code,
        content={"error_code": error_code, "message": message},
    )


def make_middleware() -> List[Middleware]:
    middleware = [
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        ),
        # Middleware(
        #     AuthenticationMiddleware,
        #     backend=AuthBackend(),
        #     on_error=on_auth_error,
        # ),
        Middleware(ResponseLogMiddleware),
    ]
    return middleware


def set_multiproc_dir() -> None:
    """
    Sets mutiproc_dir env variable.

    This function cleans up the multiprocess directory
    and recreates it. This actions are required by prometheus-client
    to share metrics between processes.

    After cleanup, it sets two variables.
    Uppercase and lowercase because different
    versions of the prometheus-client library
    depend on different environment variables,
    so I've decided to export all needed variables,
    to avoid undefined behaviour.
    """
    shutil.rmtree(config.PROMETHEUS_DIR, ignore_errors=True)
    os.makedirs(config.PROMETHEUS_DIR, exist_ok=True)
    os.environ["prometheus_multiproc_dir"] = str(
        config.PROMETHEUS_DIR.expanduser().absolute(),
    )
    os.environ["PROMETHEUS_MULTIPROC_DIR"] = str(
        config.PROMETHEUS_DIR.expanduser().absolute(),
    )


def setup_prometheus(app: FastAPI) -> None:  # pragma: no cover
    """
    Enables prometheus integration.

    :param app: current application.
    """
    PrometheusFastApiInstrumentator(should_group_status_codes=False).instrument(
        app,
    ).expose(app, should_gzip=True, name="prometheus_metrics")


def init_cache() -> None:
    Cache.init(backend=RedisBackend(), key_maker=CustomKeyMaker())


def register_startup_event(
    app: FastAPI,
) -> Callable[[], Awaitable[None]]:  # pragma: no cover
    """
    Actions to run on application startup.

    This function uses fastAPI app to store data
    inthe state, such as db_engine.

    :param app: the fastAPI application.
    :return: function that actually performs actions.
    """

    @app.on_event("startup")
    async def _startup() -> None:  # noqa: WPS430
        db_core._setup_db(app)
        # setup_opentelemetry(app)
        setup_prometheus(app)
        pass  # noqa: WPS420

    return _startup


def register_shutdown_event(
    app: FastAPI,
) -> Callable[[], Awaitable[None]]:  # pragma: no cover
    """
    Actions to run on application's shutdown.

    :param app: fastAPI application.
    :return: function that actually performs actions.
    """

    @app.on_event("shutdown")
    async def _shutdown() -> None:  # noqa: WPS430
        await app.state.db_engine.dispose()

        # await shutdown_rabbit(app)
        # stop_opentelemetry(app)
        pass  # noqa: WPS420

    return _shutdown

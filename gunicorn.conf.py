"""Gunicorn WSGI server configuration."""
from multiprocessing import cpu_count
from typing import Final

bind: Final[str] = "0.0.0.0:8000"
max_requests: Final[int] = 1000
workers = cpu_count() * 2
threads = 1
timeout: Final[int] = 60
keepalive: Final[int] = 60
preload_app: Final[bool] = True
accesslog: Final[str] = "-"
reload: Final[bool] = True
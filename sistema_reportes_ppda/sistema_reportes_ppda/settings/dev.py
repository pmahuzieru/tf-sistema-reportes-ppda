from .base import * # noqa: F403


DEBUG = True

SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"] = timedelta(minutes=60*24)  # noqa: F405
from .base import * # noqa: F403


DEBUG = False

SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"] = timedelta(minutes=5) # noqa: F405
from .base import *


DEBUG = False

SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"] = timedelta(minutes=5)
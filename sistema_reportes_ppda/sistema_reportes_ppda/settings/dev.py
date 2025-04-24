from .base import *


DEBUG = True

SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"] = timedelta(minutes=60*24)  # 1 día
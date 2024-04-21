import datetime

"""Global app settings."""
FLASK_DEBUG = True
FLASK_ENV = "development"
FLASK_JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(seconds=10)
JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(seconds=10)

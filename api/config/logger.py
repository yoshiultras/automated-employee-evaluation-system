import logging.config

ERROR_LOG_FILENAME = "logs/error.log"
LOG_FILENAME = "logs/logs.log"
JSON_LOG_FILENAME = "logs/json.log"

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s::%(name)-70s::%(process)d::%(lineno)-4d:: "
            "%(levelname)-7s :: %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "json": {  # The formatter name
            "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "format": """
                    asctime: %(asctime)s
                    created: %(created)f
                    filename: %(filename)s
                    funcName: %(funcName)s
                    levelname: %(levelname)s
                    levelno: %(levelno)s
                    lineno: %(lineno)d
                    message: %(message)s
                    module: %(module)s
                    msec: %(msecs)d
                    name: %(name)s
                    pathname: %(pathname)s
                    process: %(process)d
                    processName: %(processName)s
                    relativeCreated: %(relativeCreated)d
                    thread: %(thread)d
                    threadName: %(threadName)s
                    exc_info: %(exc_info)s
                """,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "logfile": {
            "formatter": "default",
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOG_FILENAME,
            "backupCount": 2,
        },
        "errlogfile": {
            "formatter": "default",
            "level": "ERROR",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOG_FILENAME,
            "backupCount": 2,
        },
        "verbose_output": {
            "formatter": "default",
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
        "jsonfile": {
            "formatter": "json",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": JSON_LOG_FILENAME,
            "backupCount": 2,
        },
    },
    "loggers": {
        "erp": {
            "level": "ERROR",
            "handlers": ["verbose_output"],
        },
    },
    "root": {
        "level": "DEBUG",
        "handlers": [
            "logfile",
            "errlogfile",
            "jsonfile",
        ],
    },
}

logging.config.dictConfig(LOGGING_CONFIG)

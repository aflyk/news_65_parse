logging_config = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'default': {
            'format': '#%(levelname)-8s|%(lineno)s %(name)s:%(funcName)s - %(message)s'
        },
    },
    'handlers': {
        'default': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        },
    },
    'loggers': {
        'queries.orm': {
            'level': 'DEBUG',
            'handlers': ['default'],
            'propagate': False,
        },
        'api_get.api_mun': {
            'level': 'DEBUG',
            'handlers': ['default'],
            'propagate': False,
        },
        'parse.parse_astv': {
            'level': 'DEBUG',
            'handlers': ['default'],
            'propagate': False,
        }
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['default']
    }
}

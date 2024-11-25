from dotenv import load_dotenv
import os

load_dotenv()

from logging.config import dictConfig
from app import create_app

# Logging configuration
dictConfig({
    "version": 1,
    "formatters": {
        "default": {
            "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
            "formatter": "default",
        }
    },
    "root": {
        "level": "DEBUG",
        "handlers": ["console"],
    },
})

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8082, debug=True)

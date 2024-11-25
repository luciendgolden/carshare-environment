#!/bin/bash

export FLASK_APP=main.py
export FLASK_DEBUG=1
export FLASK_RUN_HOST=0.0.0.0
export FLASK_RUN_PORT=8087

flask run
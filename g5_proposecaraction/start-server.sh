#!/bin/bash

export FLASK_APP=rest.py
export FLASK_DEBUG=1
export FLASK_RUN_HOST=0.0.0.0
export FLASK_RUN_PORT=8085

flask run

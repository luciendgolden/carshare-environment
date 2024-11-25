#!/bin/bash

export FLASK_APP=run.py
export FLASK_DEBUG=1
export FLASK_RUN_HOST=0.0.0.0
export FLASK_RUN_PORT=8082

flask run

#!/usr/bin/env bash
python=`which python || which python3`
eval "$python -m pytest -v --cov=noclist ./tests/"
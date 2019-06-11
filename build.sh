#!/bin/bash

python setup.py build_ext --inplace
time python -c "import pathfinder"

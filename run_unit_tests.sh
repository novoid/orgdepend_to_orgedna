#!/bin/sh
set -o errexit

# pytest is invoking the unit tests:
PYTHONPATH=. pytest-3 orgdepend_to_orgedna_test.py

# mypy is checking the type annotations:
PYTHONPATH=. mypy orgdepend_to_orgedna.py

#end

#!/bin/sh
set -o errexit

# pytest is invoking the unit tests:
PYTHONPATH=. pytest-3 org-depend_to_org-edna_test.py

# mypy is checking the type annotations:
#PYTHONPATH=. mypy orgformat/orgformat.py

#end

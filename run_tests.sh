#!/bin/sh
FILENAME=$(basename $0)
set -o errexit

report()
{
    echo "\n–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––→"
    echo "$FILENAME:  $@"
    echo "←–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––\n"
}

report "pytest is invoking the unit tests:"
pytest

report "mypy is checking the type annotations:"
PYTHONPATH=. mypy orgdepend_to_orgedna.py

report "all tests finished without an issue :-)"
#end

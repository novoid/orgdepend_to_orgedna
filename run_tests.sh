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

report "converting \"testfile_input.org\" to \"testfile_input_converted.org\""
./orgdepend_to_orgedna.py --overwrite testfile_input.org

report "comparing \"testfile_input_converted.org\" to \"testfile_expected_output.org\""
diff testfile_input_converted.org testfile_expected_output.org

report "all tests finished without an issue :-)"
#end

#!/usr/bin/env python3
# -*- coding: utf-8; mode: python; -*-
PROG_VERSION = u"Time-stamp: <2020-09-20 22:15:04 vk>"
PROG_VERSION_DATE = PROG_VERSION[13:23]
import sys
import os
PROG_NAME = os.path.basename(sys.argv[0])
import logging
import re
import argparse   # for handling command line arguments
from typing import List, Union, Tuple, Optional  # mypy: type checks
import codecs


DESCRIPTION = """This script converts Emacs Org mode files from org-depend to org-edna.
Please make sure you do have backup files in case something gets wrong."""

EPILOG = """
:copyright: (c) by Karl Voit <tools@Karl-Voit.at>
:license: GPL v3 or any later version
:URL: https://github.com/novoid/FIXXME
:bugreports: via github or <tools@Karl-Voit.at>
:version: """ + PROG_VERSION_DATE + "\n·\n"

# ASSUMPTION: IDs consists of [a-zA-Z0-9-]+ only
# Note: though org-depend concatenates IDs with spaces, I may have used commas as well somewhere.
BLOCKER_DEPEND_REGEX = re.compile(r'\s*:BLOCKER:\s+(?P<ids>([a-zA-Z0-9-]+[ ,]*)+)\s*')

# TRIGGER_DEPEND_REGEX = re.compile(r'((([a-zA-Z0-9-]+)\(([A-Z]+)\)))')  # working version without elisp parts
TRIGGER_DEPEND_REGEX = re.compile(r'((([a-zA-Z0-9-\'`\(\)\\ ]+?)\(([A-Z]+?)\)))')

parser = argparse.ArgumentParser(prog=sys.argv[0],
                                 # keep line breaks in EPILOG and such
                                 formatter_class=argparse.RawDescriptionHelpFormatter,
                                 epilog=EPILOG,
                                 description=DESCRIPTION)

parser.add_argument(dest="files", metavar='FILE', nargs='*', help='One or more files to convert')

parser.add_argument("--overwrite",
                    dest="overwrite", action="store_true",
                    help="Existing output files may be overwritten without warning")

parser.add_argument("-v", "--verbose",
                    dest="verbose", action="store_true",
                    help="Enable verbose mode")

parser.add_argument("-q", "--quiet",
                    dest="quiet", action="store_true",
                    help="Enable quiet mode")

parser.add_argument("--version",
                    dest="version", action="store_true",
                    help="Display version and exit")

options = parser.parse_args()


def handle_logging() -> None:
    """Log handling and configuration"""

    if options.verbose:
        FORMAT = "%(levelname)-8s %(asctime)-15s %(message)s"
        logging.basicConfig(level=logging.DEBUG, format=FORMAT)
    elif options.quiet:
        FORMAT = "%(levelname)-8s %(message)s"
        logging.basicConfig(level=logging.ERROR, format=FORMAT)
    else:
        FORMAT = "%(levelname)-8s %(message)s"
        logging.basicConfig(level=logging.INFO, format=FORMAT)


def error_exit(errorcode: int, text: str) -> None:
    """exits with return value of errorcode and prints to stderr"""

    sys.stdout.flush()
    logging.error(text)
    # input('Press <Enter> to finish with return value %i ...' % errorcode).strip()
    sys.exit(errorcode)


class OrgmodeParseException(Exception):
    """
    General exception when parsing fails.
    """

    def __init__(self, value) -> None:
        self.value = value

    def __str__(self) -> str:
        return repr(self.value)

    # example:
    # raise OrgmodeParseException('Error while parsing line. Could not extract ids: "%s"' % line)


def get_trigger_matches(line: str) -> Union[None, list]:
    """
    Returns a set of matching elements or False when the line does not match.
    """

    # ASSUMPTION: existing org-edna trigger lines are only detected via occurrences of 'todo!(' or 'scheduled!('.
    if 'todo!(' in line:
        # already org-edna syntax
        return None
    elif 'scheduled!(' in line:
        # already org-edna syntax
        return None
    elif line.strip().upper().startswith(':TRIGGER:'):
        # most probably a clean trigger line (comments, ...)
        components = TRIGGER_DEPEND_REGEX.findall(line.strip())
        # example: ('2016-11-04-some-title(DONE)', '2016-11-04-some-title(DONE)', '2016-11-04-some-title', 'DONE')
        if components:
            # generate a list of sets from the result:
            #    x[-2] = id
            #    x[-1] = keyword
            return [(x[-2].strip(), x[-1]) for x in components]
        else:
            logging.info('Could not parse trigger line: ' + line)
            return None
    else:
        # not a clean trigger line: comments, ...
        return None


def convert_trigger_line(matches: list) -> str:
    """
    Converts matching trigger elements from org-depend syntax to org-edna syntax.

    example "matches": ('2016-11-04-some-title(DONE)', '2016-11-04-some-title(DONE)', '2016-11-04-some-title', 'DONE')

    example return value: ':TRIGGER: ids(2016-11-04-some-title) todo!(DONE) ids(2020-09-19-foo) todo!(STARTED)'
    """

    assert(len(matches) > 0)
    edna_result = ':TRIGGER:'

    # a list of sets from the regex result
    for match in matches:
        (dependid, keyword) = match
        edna_result += ' ids(' + dependid + ') todo!(' + keyword + ')'
    return edna_result


def get_blocker_matches(line: str) -> Union[None, list]:
    """
    Returns a set of id strings or None when the line does not match.
    """

    if 'ids(' in line:
        return None
    else:
        components = BLOCKER_DEPEND_REGEX.match(line.strip())
        if components:
            rawids = components.group('ids')
            if ',' in rawids:
                ids = rawids.split(',')  # multiple ids, concatenated with commas and optional spaces
                return [x.strip() for x in ids]  # strip each element
            elif ' ' in rawids:
                return rawids.split()  # multiple ids, concatenated with spaces
            else:
                return [rawids]  # only one id
        else:
            return None


def generate_blocker_line_from_ids(ids: list) -> str:
    """
    Converts an matching blocker line from org-depend syntax to org-edna syntax.
    """
    return ':BLOCKER: ids(' + ' '.join(ids) + ')'


def handle_file(filename: str) -> None:
    """
    Handles one single Org mode file for conversion

    @param filename: name of the file to process
    """

    # converted_filename = absolute path + basename of old filename + '_converted.' + old file extension
    filename_split = os.path.splitext(filename)
    output_filename = filename_split[0] + '_converted' + filename_split[1]

    # check that new file name does not exist
    if os.path.isfile(output_filename) and not options.overwrite:
        error_exit(10, 'Output file name already exists and option "--overwrite" is not given. File name: "output_filename"')

    logging.info('converting:  "' + filename + '"  →  "' + output_filename + '"')

    with open(output_filename, 'w') as outputhandle:
        with codecs.open(filename, 'r', encoding='utf-8') as input:
            in_properties = False
            for line in input:
                # To maintain at least a minimum of sanity, matches for
                # trigger and blocker properties are only tried within
                # property drawers and not outside. However, detection of
                # property drawers is very basic.
                #
                # ASSUMPTION: property drawers are always starts with
                # ':PROPERTIES:' (no extra leading spaces) and ends with
                # ':END:' (no extra leading spaces).
                #
                # ASSUMPTION: no check for non-conform property drawer.
                # Each line starting with ':PROPERTIES:' is a valid
                # property drawer start indicator.
                if line.startswith(':PROPERTIES:'):
                    in_properties = True
                    outputhandle.write(line)
                    continue
                if line.startswith(':END:'):
                    in_properties = False
                    outputhandle.write(line)
                    continue
                if in_properties:
                    ids = get_blocker_matches(line)
                    if ids:
                        newline = generate_blocker_line_from_ids(ids)
                        outputhandle.write(newline + '\n')
                        continue
                    matches = get_trigger_matches(line)
                    if matches:
                        newline = convert_trigger_line(matches)
                        outputhandle.write(newline + '\n')
                        continue
                    else:
                        outputhandle.write(line)
                else:
                    outputhandle.write(line)
    print()  # add an empty line after each file so that stdout is more legible


def main():
    """Main function"""

    if options.version:
        print(os.path.basename(sys.argv[0]) + " version " + PROG_VERSION_DATE)
        sys.exit(0)

    if not options.files:
        parser.print_help()
        sys.exit(0)

    handle_logging()

    if options.verbose and options.quiet:
        error_exit(1, "Options \"--verbose\" and \"--quiet\" found. " +
                   "This does not make any sense, you silly fool :-)")

    # check existance of all files before start with handling any of them:
    all_files_exist = True
    for filename in options.files:
        if not os.path.isfile(filename):
            all_files_exist = False
            print('File "%s" does not exist.' % filename)
    if not all_files_exist:
        error_exit(2, "One or more files from the argument list do not exist. Please check parameters and try again.")

    print()  # add an empty line before each file so that stdout is more legible
    for filename in options.files:
        handle_file(filename)

    logging.info("successfully converted all given files.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:

        logging.info("Received KeyboardInterrupt")

# Local Variables:
# End:

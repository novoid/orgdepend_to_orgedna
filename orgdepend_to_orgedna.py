#!/usr/bin/env python3
# -*- coding: utf-8; mode: python; -*-
PROG_VERSION = u"Time-stamp: <2020-09-19 23:39:59 vk>"
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
:URL: https://github.com/novoid/filetags
:bugreports: via github or <tools@Karl-Voit.at>
:version: """ + PROG_VERSION_DATE + "\n·\n"

BLOCKER_DEPEND_REGEX = re.compile(r'\s*:BLOCKER:\s+(?P<ids>([a-zA-Z0-9-]+[ ,]*)+)\s*')

parser = argparse.ArgumentParser(prog=sys.argv[0],
                                 # keep line breaks in EPILOG and such
                                 formatter_class=argparse.RawDescriptionHelpFormatter,
                                 epilog=EPILOG,
                                 description=DESCRIPTION)

parser.add_argument(dest="files", metavar='FILE', nargs='*', help='FIXXME: One or more files to convert')

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


def handle_logging():
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


def error_exit(errorcode, text):
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


TRIGGER_DEPEND_REGEX = re.compile(r'\w*:TRIGGER:\w*(ids\((?P<ids>.+?\))|(/(?P<action>.+)!\(?P<value>.+\)))')


def get_trigger_matches(line: str) -> Union[bool, list]:
    """
    Returns a set of matching elements or False when the line does not match.

    @param line: FIXXME
    @param m: FIXXME
    @return:  FIXXME
    """

    if '!' in line:
        return False
    else:
        components = line.match(TRIGGER_DEPEND_REGEX)

        return components


def convert_trigger_line(line: str) -> Union[bool, str]:
    """
    Converts an matching trigger line from org-depend syntax to org-edna syntax.

    @param line: FIXXME
    @param m: FIXXME
    @return:  FIXXME
    """

    return False  # FIXXME


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


def handle_file(filename: str) -> bool:
    """
    Handles one single Org mode file for conversion

    @param filename: name of the file to process
    @return:  FIXXME
    """

    with codecs.open(filename, 'r', encoding='utf-8') as input:
        for line in input:
            # trigger_components = get_trigger_matches(line)
            # if trigger_components:
            #     print(line)
            ids = get_blocker_matches(line)
            if ids:
                line = generate_blocker_line_from_ids(line)
                
    return True  # FIXXME


def main():
    """Main function"""

    if options.version:
        print(os.path.basename(sys.argv[0]) + " version " + PROG_VERSION_DATE)
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

    for filename in options.files:
        handle_file(filename)

    logging.debug("successfully finished.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:

        logging.info("Received KeyboardInterrupt")

# Local Variables:
# End:

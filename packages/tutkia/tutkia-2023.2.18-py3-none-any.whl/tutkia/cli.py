"""Explore (Finnish: tutkia) ticket system trees. - command line interface."""
import argparse
import sys
from typing import no_type_check

import tutkia.api as api
from tutkia import (
    APP_NAME,
    APP_VERSION,
    ENCODING,
    LOG_SEPARATOR,
    QUIET,
    TS_FORMAT_PAYLOADS,
    log,
)


@no_type_check
def parser():
    """Implementation of command line API returning parser."""
    impl = argparse.ArgumentParser(description='Explore.')
    impl.add_argument(
        '-v',
        '--verbose',
        dest='verbose',
        action='store_true',
        help='Be more verbose, maybe',
    )
    impl.add_argument(
        '-d',
        '--debug',
        dest='debug',
        action='store_true',
        help='Support debugging, maybe',
    )
    impl.add_argument(
        '-q',
        '--query',
        dest='query',
        type=str,
        help='A valid JQL query',
    )
    return impl


@no_type_check
def app(argv=None):
    """Drive the exploration."""
    argv = sys.argv[1:] if argv is None else argv
    options = parser().parse_args(argv)
    return api.process(options)


if __name__ == '__main__':
    sys.exit(app(sys.argv[1:]))

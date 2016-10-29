# This file is part of the APOD feed fixer.
# 
# APOD feed fixer is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# APOD feed fixer is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with APOD feed fixer.  If not, see <http://www.gnu.org/licenses/>.


import getopt, io, sys
from apod import fetch_feed, generate_feed


FEED_URL = 'https://apod.fragdev.com'
FEED_TITLE = 'Astronomy Picture of the Day (FragDev Cache)'
FEED_DESCRIPTION = """
This feed is a restructured, slightly modified and repaired version of the
Astronomy Picture of the Day feed generously provided by NASA, Goddard
Space Flight Center, NASA's Astrophysics Science Division, and Michigan
Tech U. The original feed can be found at http://apod.nasa.gov/apod.rss.
"""


def usage():
    return """
USAGE:
    xxx [[-i|--input] http://example.com/rss] [[-o|--output] out.file] [-d|--debug]

    All arguments are optional; if unspecified, program reads from stdin and
    sends output to stdout.

OPTIONS:
    -i | --input
        Specifies a URL to fetch and process. 
    -o | --output
        Filename and/or path to write to.
    -d | --debug
        Print debugging information

EXAMPLES:

    TODO
    """


# If this module was called directly, run it
if __name__ == "__main__":

    debug = False
    source = False
    output = sys.stdout

    try:
        opt, args = getopt.getopt(sys.argv, 'di:o:', [
                '--debug',
                '--input=',
                '--output='])

        for switch, value in opt:

            if switch in ('-d', '--debug'):
                debug = True

            elif switch in ('-i', '--input'):
                source = fetch_feed(value)

            elif switch in ('-o', '--output'):
                output = io.open(value, 'w')

    except Exception as err:
        print(err) >> sys.stderr
        print(usage()) >> sys.stderr
        exit(1)

    # Get all of stdin if we haven't been given an URL to fetch
    if not source:
        source = sys.stdin.read()

    output.write(generate_feed(FEED_TITLE,
        FEED_URL,
        FEED_DESCRIPTION,
        source,
        debug))


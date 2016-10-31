
Astronomy Picture of the Day (APOD) Feed Fixer
===

Unfortunately, NASA and the University of Michigan are far too busy teaching
students and exploring the universe to fix their RSS feed, which leaves fans
of the Astronomy Picture of the Day (APOD for short) with a sub-par RSS
experience.

As a fix for this, I've created this small python module to gently re-shape
their RSS data into something more stable and well escaped.

Usage
---

To generate a fixed APOD feed, the following command can be scripted:

    curl -s http://apod.nasa.gov/apod.rss | \
        python __init__.py > fixed_feed.rss

This program is not designed to host the file itself, for simplicity's sake. The
output should be served up by a full-fledged webserver, like nginx or Apache.

To see an example, you can use https://apod.fragdev.com/rss.

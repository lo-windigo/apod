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


def fetch_feed(url, debug):
    """ Fetch data from a URL
    """

    # from datetime import datetime
    import urllib3

    http = urllib3.PoolManager()
    headers = {}

    # Fetch the feed data
    #if self.last_updated:
    #    if self.debug:
    #        print('[D] Setting "If-Modified-Since" header to "{}".' %
    #        self.last_updated)
    #    headers = {'If-Modified-Since': self.last_updated}

    r = http.request('GET', url, headers=headers)

    # Feed has not been updated since last fetch
    #if r.status is 304:
    #    if self.debug:
    #        print('[D] Feed is unmodified; skipping update.')
    #    return

    # Request didn't return HTTP 200 (OK)
    if not r.status == 200:

        if debug:
            error = '[D] Feed returned non-200 HTTP code of {}.'.format(
                r.status)
            print(error)

        raise Exception('HTTP ERROR: {}'.format(r.status))

    return r.data


def generate_feed(title, url, description, data, debug):
    """ Parse RSS feed data and restructure it using known good elements of the
    feed, like title and link.
    """

    from datetime import datetime
    import pytz
    from xml.etree import ElementTree

    # Parse the feed into an XML tree
    latest_feed = ElementTree.fromstring(data)

    # Get all of the items that we need
    pictures = latest_feed.findall('./channel/item')

    # Begin to create the new, fixed document
    fixed_feed = ElementTree.Element('rss')
    fixed_feed.set('version', '2.0')
    channel = ElementTree.SubElement(fixed_feed, 'channel')

    # Set general feed details
    feed_title = ElementTree.SubElement(channel, 'title')
    feed_title.text = title
    feed_link = ElementTree.SubElement(channel, 'link')
    feed_link.text = url
    feed_desc = ElementTree.SubElement(channel, 'desc')
    feed_desc.text = description
    feed_lang = ElementTree.SubElement(channel, 'lang')
    feed_lang.text = 'en-us'

    # Generate the date with UTC, so we can get the right format for RSS
    utc = pytz.utc
    now = datetime.now(utc)
    feed_update = ElementTree.SubElement(channel, 'lastBuildDate')
    feed_update.text = now.strftime('%a, %d %b %Y %H:%M:%S %z')

    # Convert each picture, or item node, into a better version of itself
    for picture in pictures:
        item = ElementTree.SubElement(channel, 'item')

        old_title = picture.find('title')
        item.append(old_title)
        old_link = picture.find('link')
        item.append(old_link)
        
        # Create a new, less ugly description
        description = ElementTree.SubElement(item, 'description')
        description.text = '<a href="{}">{}</a>'.format(
            old_link.text, old_title.text)

    return ElementTree.tostring(fixed_feed, encoding='unicode')

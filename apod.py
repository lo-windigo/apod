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

from datetime import datetime
import pytz
from xml.etree import ElementTree


def generate_feed(title, url, description, data):
    """
    Parse RSS feed data and restructure it using known good elements of the
    feed, like title and link.
    """

    # Parse the feed into an XML tree
    latest_feed = ElementTree.fromstring(data)

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
    for picture in latest_feed.findall('./channel/item'):
        channel.append(reformat_item(picture))

    return ElementTree.tostring(fixed_feed, encoding='unicode')


def reformat_item(feed_element):
    """
    Create a new XML element for a single item
    """
    item = ElementTree.Element('item')

    # Carry over the old title and link
    original_title = feed_element.find('title')
    original_link = feed_element.find('link')
    item.append(original_title)
    item.append(original_link)
    
    # Create a new, less ugly description
    description = ElementTree.SubElement(item, 'description')
    description.text = '<a href="{}">{}</a>'.format(
        original_link.text, original_title.text)

    return item


#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of PyBOSSA.
#
# PyBOSSA is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PyBOSSA is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with PyBOSSA.  If not, see <http://www.gnu.org/licenses/>.


import re
import json
import urllib
import urllib2
import flickr

def get_flickr_photos(size="big", tags='endangered species, butterfly'):
    """
    Gets public photos from Flickr feeds
    :arg string size: Size of the image from Flickr feed.
    :returns: A list of photos.
    :rtype: list
    """
    # Get the ID of the photos and load it in the output var
    print('Contacting Flickr for photos')
    url = "https://api.flickr.com/services/rest/"
    parameters = {
        'method': 'flickr.photos.search',
        'api_key': flickr.API_KEY,
        'license': '1',
        'format':  'json',
        'tags': tags,
        'nojsoncallback': 1}

    query = url + "?" + urllib.urlencode(parameters)
    print query
    urlobj = urllib2.urlopen(query)
    data = urlobj.read()
    print data
    urlobj.close()
    # The returned JSON object by Flickr is not correctly escaped,
    # so we have to fix it see
    # http://goo.gl/A9VNo
    regex = re.compile(r'\\(?![/u"])')
    fixed = regex.sub(r"\\\\", data)
    output = json.loads(fixed)
    print('Data retrieved from Flickr')

    # For each photo ID create its direct URL according to its size:
    # big, medium, small (or thumbnail) + Flickr page hosting the photo
    photos = []
    url = 'https://api.flickr.com/services/rest'
    for photo in output['photos']['photo']:
        # Get photo info
        parameters = {
            'method': 'flickr.photos.getInfo',
            'api_key': flickr.API_KEY,
            'photo_id': photo['id'],
            'secret': photo['secret'],
            'format':  'json',
            'nojsoncallback': 1
        }
        query = url + "?" + urllib.urlencode(parameters)
        print query
        urlobj = urllib2.urlopen(query)
        data = urlobj.read()
        #print data
        urlobj.close()
        photo_data = json.loads(data)

        imgUrl_m = "https://farm%s.staticflickr.com/%s/%s_%s_m.jpg" % (photo['farm'], photo['server'], photo['id'], photo['secret'])
        imgUrl_b = "https://farm%s.staticflickr.com/%s/%s_%s_b.jpg" % (photo['farm'], photo['server'], photo['id'], photo['secret'])
        photos.append({'url_m':  imgUrl_m,
                       'url_b': imgUrl_b,
                       'photo_info': photo_data})
    return photos

photos = get_flickr_photos()

with open('images.json', 'w') as f:
    f.write(json.dumps(photos))

print "DONE!"

#!/usr/bin/env python3

import re
import sys
import json

REZOMAN_FIELDS = ['pseudo', 'name', 'promo', 'last_update']

def error(msg, rezoman = None):
    error_msg = f"Error: {msg}"
    if rezoman:
        error_msg += f" for rezoman {rezoman['properties']['pseudo']}"
    sys.stderr.write(error_msg + '\n')
    sys.exit(1)


_promo = re.compile(r'^(19|20)[0-9][0-9]$')
_date = re.compile(r'^20[0-9][0-9]-[0-9][0-9]-[0-9][0-9]$')
_coord = re.compile(r'^-?[0-9]{1,3}\.[0-9]{1,10}$')


if __name__ == '__main__':
    with open(sys.argv[1]) as json_map:
        rezomap = json.load(json_map)

    for rezoman in rezomap['features']:
        # Fields check
        if not list(rezoman['properties'].keys()) == REZOMAN_FIELDS:
            error('Invalid properties fields')

        # Type checks
        for field in REZOMAN_FIELDS:
            if type(rezoman['properties'][field]) != str:
                error(f"Field {field} must be a string", rezoman)

        # Value checks
        if not _promo.match(rezoman["properties"]["promo"]):
            error('Invalid Promo', rezoman)
        if not _date.match(rezoman["properties"]["last_update"]):
            error('Invalid update date', rezoman)
        if not _coord.match(str(rezoman["geometry"]["coordinates"][0])):
            error('Invalid latitude', rezoman)
        if not _coord.match(str(rezoman["geometry"]["coordinates"][1])):
            error('Invalid longitude', rezoman)

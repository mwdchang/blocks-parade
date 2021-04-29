"""
Clean blocks-min.jsoon
- Convert to JSON-L and only preserves the ones with thumbnails
"""

import json
from dateutil.parser import parse


def sort_key(block):
  return parse(block["created_at"])

with open("blocks-min.json", "r") as reader:
    content = reader.readline()
    json_content = json.loads(content)
    r = []

    for block in json_content:
        if "thumbnail" in block:
            r.append(block)
    r.sort(key = sort_key)
    print(json.dumps(r))


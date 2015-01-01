__author__ = 'martin'
"""
Convert a csv matrix file to json file
"""

import pandas as pd
import json
import io

# read csv
link_csv_path = "../../dataset/original/xhamster/link_xhamster.csv"
link_json_path = "../../dataset/generated/xhamster/link_xhamster.json"
data = pd.read_csv(link_csv_path, sep=",",encoding="utf-8", index_col=0)

# clean data
data = pd.DataFrame(data.fillna(0))

# get the tags name
tags = list(data[:0])


# get the maximum matrix value
max_value = 0
for tag_source in tags:
    for tag_target in tags:
        if data[tag_source][tag_target] >= max_value:
            max_value = data[tag_source][tag_target]

# get matrix values
strenghs = []
for tag_source in tags:
    for tag_target in tags:
        strengh = []
        strengh.append(tags.index(tag_source))
        strengh.append(tags.index(tag_target))
        value = data[tag_source][tag_target]
        # transform - 1 value to 0
        value = (value + 1) / max_value * 200

        # gephi edges file
        #if ((tags.index(tag_source) != tags.index(tag_target)) and value!=0.0):
        #    print str(tags.index(tag_source)) + ';' + str(tags.index(tag_target)) + ';Undirected;' + str(value)

        strengh.append(value)
        strenghs.append(strengh)

# create the JSON file
with io.open(link_json_path, 'w', encoding='utf-8') as f:
  f.write(unicode(json.dumps({"nodes": [{'tags':tag, 'group':1} for tag in tags],"links": [{'source':strengh[0], 'target':strengh[1], 'value':strengh[2]} for strengh in strenghs]}, ensure_ascii=False)))



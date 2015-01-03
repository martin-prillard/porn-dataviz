__author__ = 'martin'
"""
Convert a csv matrix file to json file
"""

import json
import io
import pandas as pd

# read csv
link_xhamster_csv_path = "../../dataset/original/xhamster/link_xhamster.csv"
# generated file
link_json_path = "../../dataset/generated/xhamster/link_xhamster.json"

data_xhamster = pd.read_csv(link_xhamster_csv_path, sep=",",encoding="utf-8", index_col=0)
# clean data
data_xhamster = pd.DataFrame(data_xhamster.fillna(0))
# get the tags name
tags_xhamster = list(data_xhamster[:0])

# gephi clustering
tags_cluster = [1,1,0,1,1,2,3,3,1,2,4,1,1,1,3,5,1,1,2,3,2,2,2,1,3,2,1,4,1,1,1,1,1,4,7,3,2,2,7,3,7,3,1,6,5,3,5,3,2,3,3,1,1,7,2,1,1,6,1,1,1,2,2,2,1,0,2,3,1,5,3,1,3,3,3,1,2,3,2,3,2,4,1,1,1,1,3,1,7,7,2,1]

# get the maximum matrix value
max_value = 0
for tag_source in tags_xhamster:
    for tag_target in tags_xhamster:
        if data_xhamster[tag_source][tag_target] >= max_value:
            max_value = data_xhamster[tag_source][tag_target]

# get matrix values
strenghs = []
for tag_source in tags_xhamster:
    for tag_target in tags_xhamster:
        strengh = []
        strengh.append(tags_xhamster.index(tag_source))
        strengh.append(tags_xhamster.index(tag_target))
        value = data_xhamster[tag_source][tag_target]

        # transform - 1 value to 0
        value = (value + 1) / max_value * 200

        strengh.append(value)
        strenghs.append(strengh)

# create the JSON file
with io.open(link_json_path, 'w', encoding='utf-8') as f:
  f.write(unicode(json.dumps({"nodes": [{'tags':tag, 'group':tags_cluster[tags_xhamster.index(tag)]} for tag in tags_xhamster],
                              "links": [{'source':strengh[0], 'target':strengh[1], 'value':strengh[2]} for strengh in strenghs]},
                             ensure_ascii=False)))
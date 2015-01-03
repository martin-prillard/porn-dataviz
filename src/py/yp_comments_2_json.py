__author__ = 'martin'
"""
Convert wordcount on user's comments to JSON file
"""

import pandas as pd
import json
import io

# file to convert
comments_wordcount_txt_path = "../../dataset/generated/youporn/video-comments_wordcount.txt"
# generated file
comments_wordcount_json_path = "../../dataset/generated/youporn/video-comments_wordcount.json"

# read comments_wordcount_txt_path
data = pd.read_csv(comments_wordcount_txt_path, sep="\s", engine='python', encoding="utf-8", header=None)
data = pd.DataFrame(data.fillna(0))

# get the maximum tag frequency
max_tag_frequency = float(data.icol(2)[0])
# maximum tag size
max_tag_size = float(150)
# max tag in json file
max_tag_json = 35


# set the right size according the tag frequency
def get_tag_size(frequency):
    return int((float(frequency) / max_tag_frequency) * max_tag_size)

# create the JSON file
with io.open(comments_wordcount_json_path, 'w', encoding='utf-8') as f:
  f.write(unicode(json.dumps([{'tag':data.icol(1)[tag_id], 'size':get_tag_size(str(data.icol(2)[tag_id]))} for tag_id in range(0, max_tag_json)], ensure_ascii=False)))

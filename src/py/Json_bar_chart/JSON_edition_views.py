# -*- coding: utf8 -*-

#--------------------------------------------------------------------------------#
# Generate JSON file containing the number of videos per slice for a given field
# function generate_json_from_tags:
# feature: nb_views / nb_comments / runtime
# Tags : list of Tags
# number_of_bins : number of elements
#--------------------------------------------------------------------------------#

import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import math

#--------------------------------------------------------------------------------#

# create a 2D-list containing the tags for each cluster
clusters =pd.read_csv("20_clusters.csv", sep=';', header = 0)
Tags = []
for i in range (0, 20):
    cluster_tag = clusters.loc[clusters['cluster'].isin([i])].tag.values
    Tags.append(cluster_tag)


#--------------------------------------------------------------------------------#

# load data:
xhamster =pd.read_csv("xhamster.csv")
xhamster = xhamster.drop_duplicates().dropna()
# /!\ on passe de 786000 éléments à 338500

# parse upload_date to date:
#xhamster.upload_date  = pd.to_datetime(xhamster.upload_date)

# remove ponctuation & symbols from channels
import string
exclude = set(string.punctuation)
def remove_ponctuation(s):
    return ''.join(ch for ch in s if ch not in exclude)
xhamster.channels = xhamster.channels.apply(lambda x: remove_ponctuation(x))
#--------------------------------------------------------------------------------#

def generate_json_from_tags(tags, feature, number_of_bins, cluster_number):

    print feature
    print tags

    # select the rows containing the tags
    xhamster_tags = xhamster.loc[xhamster['channels'].isin(tags)]

    # generate df for histogram visualization

    if xhamster_tags.shape[0] >= number_of_bins:
        nb_of_groups = number_of_bins
        maxSup4 = int(math.ceil((xhamster_tags[feature].max().astype(int))))
        min = 0
        somme = 1e3
        while min < 5 and somme > 100:
            maxSup4 = int(0.9*maxSup4)
            print maxSup4
            if maxSup4 > number_of_bins:
                df_groups = pd.cut(xhamster_tags[feature], range(0, maxSup4, int(math.ceil(maxSup4/nb_of_groups))))

                # number of videos per range
                df_cut = xhamster_tags[feature].groupby(df_groups).count()
                somme = df_cut.sum()

                # reindex with the max value of each group
                ddf = pd.DataFrame(df_cut.index.values)
                ddf2 = ddf[0].apply(lambda x: remove_ponctuation(x).split(" ")[1])
                df_cut.index = ddf2.values
                # min
                min = df_cut.min()
                print min

            else:
                df_groups = pd.cut(xhamster_tags[feature], range(0, int(math.ceil(0.5*(xhamster_tags[feature].max().astype(int)))), int(math.ceil(0.5*(xhamster_tags[feature].max().astype(int))/nb_of_groups))))
                # number of videos per range
                df_cut = xhamster_tags[feature].groupby(df_groups).count()

                # reindex with the max value of each group
                ddf = pd.DataFrame(df_cut.index.values)
                ddf2 = ddf[0].apply(lambda x: remove_ponctuation(x).split(" ")[1])
                df_cut.index = ddf2.values

                # min y value
                min = df_cut.min()

    else:
        df_cut = pd.DataFrame(np.zeros(number_of_bins))


    # rename columns
    df_cut = pd.DataFrame(df_cut)
    df_cut['x'] = df_cut.index
    df_cut.columns = ['y', 'x']
    df_cut.reset_index()

    # divise par 1000
    df_cut['x']= df_cut['x'].apply(lambda z: int(math.ceil(int(z)/1000)))

    # write to csv
    if feature == 'runtime':
        feature = 'x_runtime'
    file_name = "JSON_Files/" + feature + "_" + str(cluster_number) + ".json"
    df_cut.to_json(file_name, orient='records')


#--------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------#

# generate all the JSON files
Features = ['nb_views']
cluster_number = -1
nb_of_bins = 15
for tags in Tags:
    cluster_number += 1
    for feat in Features:
        generate_json_from_tags(tags, feat, nb_of_bins, cluster_number)


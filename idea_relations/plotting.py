# -*- coding: utf-8 -*-

# Plotting
# Please run in Python3

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# plt.style.use('science')

year_idea_mapping_file = "/Users/shichengliu/Desktop/College_CS/cs257/NLP-win-21/idea_relations/RMRB_p10_integrated/doc_topic-p10sample_1.csv"

idea_name1 = u"科学技术, 工作者, 研究所, 科学家, 科学研究, 中国科学院, 科技人员, 讨论会, 科学院, 实验室"
idea_name2 = u"新华社, 不久前, 第一次, 大熊猫, 动物园, 第三次, 赠送给, 第一批, 附图片, 第一个"

# NOTE: This is the line number, for any idea you see in a text editor,
# DEDUCT ONE
idea1_index_number = 12
idea2_index_number = 43

ORIGINAL_FORMAT = True

# output_file = "/Users/shichengliu/Desktop/College_CS/cs257/NLP-win-21/idea_relations/ALL_OUTPUTS/plots/sample.png"
THRES = 0.01

def transform_function(string):
    string = string.replace('[', '').replace(']', '')
    res = []
    for element in string.split(','):
        res.append(int(element))
    return res

def check_exists_1(row):
    if idea1_index_number in transform_function(row['idea_present']):
        return 1
    return 0

def check_exists_2(row):
    if idea2_index_number in transform_function(row['idea_present']):
        return 1
    return 0

def check_exists_other_format(index, row):
    if row['topic{}'.format(index)] > THRES:
        return 1
    return 0

def generate_column_names(count = 50):
    res = []
    for i in range(count):
        res.append("topic{}".format(i))
    return res




if ORIGINAL_FORMAT:
    dataset = pd.read_csv(year_idea_mapping_file, header=None, names=['year', 'idea_present'])
    print(dataset.head(5))
    
    dataset['1_present'] = dataset.apply(lambda row: check_exists_1(row), axis = 1)
    dataset['2_present'] = dataset.apply(lambda row: check_exists_2(row), axis = 1)

else:
    dataset = pd.read_csv(year_idea_mapping_file, names=["id"] + generate_column_names() + ["year"], delim_whitespace=True, skiprows=[0])
    print(dataset.columns)
    print(dataset.head(5))

    dataset['1_present'] = dataset.apply(lambda row: check_exists_other_format(idea1_index_number, row), axis = 1)
    dataset['2_present'] = dataset.apply(lambda row: check_exists_other_format(idea2_index_number, row), axis = 1)



# print(dataset.columns)
# print(list(dataset['present_1']))

# dataset['present_1'] = dataset.apply(lambda row: row['present_1'] / row['all_count'])
# dataset['present_2'] = dataset.apply(lambda row: row['present_2'] / row['all_count'])
groups = dataset.groupby('year').groups.keys()
year = [*groups]

dataset = dataset.groupby('year').agg(
present_1=pd.NamedAgg(column="1_present", aggfunc=np.sum),
present_2=pd.NamedAgg(column="2_present", aggfunc=np.sum),
all_count=pd.NamedAgg(column="year", aggfunc=np.size),
)
print(dataset.head(5))

present_1 = list(dataset['present_1'])
present_2 = list(dataset['present_2'])
all = list(dataset['all_count'])

# print(present_1)
# print(present_2)

# print(dataset.head(5))

present_1 = [present_1[i] / all[i] for i in range(len(present_1))]
present_2 = [present_2[i] / all[i] for i in range(len(present_2))]

fig, ax = plt.subplots()
ax.plot(year, present_1, label = idea_name1)
ax.plot(year, present_2, label = idea_name2)
ax.legend()

ax.set(xlabel='year', ylabel='percentage of ideas in corpus')

# fig.savefig("test.png")
plt.show()
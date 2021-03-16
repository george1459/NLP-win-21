# -*- coding: utf-8 -*-

import collections
import os
import functools
import numpy as np
import utils
import io


def load_topic_words(vocab, input_file, top=10):
    """Get the top 10 words for each topic"""
    topic_map = {}
    with open(input_file) as fin:
        for line in fin:
            parts = line.strip().split()
            tid = int(parts[0])
            top_words = parts[2:2+top]
            topic_map[tid] = ",".join([vocab[int(w)] for w in top_words])
    return topic_map


def load_doc_topics(input_file, doc_topic_file, threshold=0.01):
    """Load topics in each document"""
    articles = []
    # fd = open(doc_topic_output_file, "w")
    # print("opening {}".format(doc_topic_output_file))
    with open(doc_topic_file) as tfin:
        for data in utils.read_json_list(input_file):
            topic_line = tfin.readline()
            if not topic_line:
                break
            ideas = topic_line.strip().split()[2:]
            ideas = set([i for (i, v) in enumerate(ideas)
                         if float(v) > threshold])
            articles.append(utils.IdeaArticle(fulldate=int(data["date"]),
                                         ideas=ideas))
    #         fd.write('{},"{}"\n'.format(int(data["date"]), list(ideas)))
    #         print('{},"{}"\n'.format(int(data["date"]), list(ideas)))
    # fd.close()
    return articles


def load_articles(input_file, topic_dir):
    vocab_file = "%s/data.word_id.dict" % topic_dir
    doc_topic_file = "%s/doc-topics.gz" % topic_dir
    topic_word_file = "%s/topic-words.gz" % topic_dir
    doc_topic_output_file = "%s/doc-topic-filterred.txt" % topic_dir
    vocab = utils.read_word_dict(vocab_file)
    topic_map = load_topic_words(vocab, topic_word_file)
    articles = load_doc_topics(input_file, doc_topic_file)
    with io.open(doc_topic_output_file, "w") as fd:
        for article in articles:
            fd.write(u'{},"{}"\n'.format(article.fulldate, list(article.ideas)))

    with io.open("%s/topic-words-filterred.txt" % topic_dir, "w", encoding="utf8") as fd:
        for key, value in topic_map.items():
            fd.write(u"{} {}\n".format(key, value))
            
    return articles, vocab, topic_map


def check_mallet_directory(directory):
    vocab_file = "%s/data.word_id.dict" % directory
    doc_topic_file = "%s/doc-topics.gz" % directory
    topic_word_file = "%s/topic-words.gz" % directory
    return all([os.path.exists(filename)
               for filename in [vocab_file, doc_topic_file, topic_word_file]])

if __name__ == "__main__":
    load_articles("/mnt/disks/sdb/data/RMRB_all.jsonlist", "/mnt/disks/sdb/data/RMRB_plotting/processing")
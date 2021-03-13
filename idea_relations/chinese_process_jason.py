import jieba
import re
import os
import io
import json
import random

# stop words
with io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "chinese_stop_words.txt"), 'r', encoding="utf8") as file:
    stop_words = file.read()
stop_words = stop_words.split('\n')
stop_words = set(stop_words)

with io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "stopwords-zh", "stopwords-zh.txt"), 'r', encoding="utf8") as file:
    stop_words_new = file.read()
stop_words_new = stop_words_new.split('\n')
stop_words.update(stop_words_new)

with io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "RMRB_specific_stop_words.txt"), 'r', encoding="utf8") as file:
    stop_words_new = file.read()
stop_words_new = stop_words_new.split('\n')
stop_words.update(stop_words_new)

EACH_MONTH_UPPER_LIMIT = None
OUTPUT_FILE_NAME ="RMRB_all.jsonlist"
UNZIP_FILES = False

# re_pattern_1 = re.compile('\d*')
re_pattern_2 = re.compile(r'[0-9]\d*[0-9]\d*')

def process_one_folder(folder):
    res = []
    j = 0
    for small_file in os.listdir(folder):
        if os.path.isdir(os.path.join(folder, small_file)):
            continue
        with open(os.path.join(folder, small_file), "r") as fd:
            text = fd.read().replace('\n', '').replace(' ','')
        seg_list = jieba.cut(text, cut_all=False)
        seg_list_res = []
        for i in seg_list:
            if i not in stop_words and i.isdigit() == False and i != "\r" and i.isspace() == False:
                seg_list_res.append(i)
            # else:
                # print("excluded", i)
        tmp=re.findall(re_pattern_2, small_file)
        small_dict = dict()
        small_dict['date'] = tmp[0]
        small_dict['text'] = ' '.join(seg_list_res)
        res.append(small_dict)
        if EACH_MONTH_UPPER_LIMIT != None and j > EACH_MONTH_UPPER_LIMIT:
            return res
        j += 1
    return res

def unzip_one_folder(com_file):
    new_loc = com_file.replace(".7z", "")
    # new_loc = os.path.join(new_loc, "output")
    os.system("7za e {} -o{}".format(com_file, new_loc))
    print("7za e {} -o{}".format(com_file, new_loc))

if __name__ == "__main__":
    dir_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "RMRB_dataset")
    # NOTE: The following lines are for unzipping files
    # if UNZIP_FILES:
    #     for i in os.listdir(dir_name):
    #         if os.path.isdir(os.path.join(dir_name, i)) == False:
    #             continue
    #         unzip_one_folder(os.path.join(dir_name, i))

    with io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", OUTPUT_FILE_NAME), "w", encoding='utf8') as out_fd:
        dirs = os.listdir(dir_name)
        dirs.sort()
        for i in dirs:
            if os.path.isdir(os.path.join(dir_name, i)) == False:
                continue
            res = process_one_folder(os.path.join(dir_name, i))
            for j in res:
                out_fd.write(json.dumps(j, ensure_ascii=False, encoding='utf8'))                
                out_fd.write(u"\n")
            out_fd.flush()
            print("Finished with {}".format(i))

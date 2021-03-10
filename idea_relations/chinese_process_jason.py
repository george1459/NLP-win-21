import jieba
import re
import os
import io
import json

# stop words
with io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "chinese_stop_words.txt"), 'r', encoding="utf8") as file:
    stop_words = file.read()
stop_words = stop_words.split('\n')
stop_words = set(stop_words)
# print(stop_words)

def process_one_folder(folder):
    res = []
    for small_file in os.listdir(folder):
        if os.path.isdir(os.path.join(folder, small_file)):
            continue
        with open(os.path.join(folder, small_file), "r") as fd:
            text = fd.read().replace('\n', '').replace(' ','')
        seg_list = jieba.cut(text, cut_all=False)
        seg_list_res = []
        for i in seg_list:
            if i not in stop_words:
                seg_list_res.append(i)
            # else:
                # print("excluded", i)
        tmp=re.compile(r'[0-9]\d*[0-9]\d*').findall(small_file)
        small_dict = dict()
        small_dict['date'] = tmp[0]
        small_dict['text'] = ' '.join(seg_list_res)
        # small_dict['text'] = small_dict['text'].decode('latin_1')
        # print(small_dict['text'])
        res.append(small_dict)
        # print(small_dict)
    return res

def unzip_one_folder(com_file):
    new_loc = com_file.replace(".7z", "")
    # new_loc = os.path.join(new_loc, "output")
    os.system("7za e {} -o{}".format(com_file, new_loc))
    print("7za e {} -o{}".format(com_file, new_loc))

if __name__ == "__main__":
    dir_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "RMRB_dataset")
    for i in os.listdir(dir_name):
        if os.path.isdir(os.path.join(dir_name, i)) == False:
            continue
        unzip_one_folder(os.path.join(dir_name, i))

    with io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "RMRB_all.txt"), "w", encoding='utf8') as out_fd:
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

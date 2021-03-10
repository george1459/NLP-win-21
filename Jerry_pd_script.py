# Instruction: 
# 1. clone from github 
# > get clone https://github.com/fangj/rmrb.git

# 2. Unzip all with 7-zip
# install 7-zip: apt-get install p7zip-full
# unzip with : 7z x file.7z -o/file
# > sh pre.sh

# 3. get json 
# > get_json.py



import os
import re
import json

def get_jsonlist(dir):
    json_list = []
    count = 0
    

    files_ = os.listdir(dir)
    files_ = sorted(files_)
 
    for files in files_:
       
        if count % 12 == 0:
            print(files)
        count += 1
        dic = {}
       
        tmp=re.compile(r'[0-9]\d*[0-9]\d*').findall(files)
        # tmp: ['1946', '05']
        
        content = []
        
        file_ = os.listdir(dir + '/' + files)
        file_ = sorted(file_)
     
        for file in file_:
            if os.path.isfile(dir + '/' + files + '/' + file):
                f_tag = open(dir + '/' + files + '/' + file)
                content.append(f_tag.read())
                f_tag.read()
                f_tag.close()
        
        dic['date'] = tmp[0]
        dic['text'] = ''.join(content)
        # dict month

        json_list.append(json.dumps(dic, ensure_ascii=False))


    return json_list

if __name__ =='__main__':
    json_list = get_jsonlist('rmrb7z')
    # test: 
#    json_list = get_jsonlist('rmrbtest')
    print(len(json_list))

    with open('json_list_v2.json', 'w') as writer:
        for item in json_list:
            writer.write(item)
            writer.write('\n')


import pandas as pd
import sys
import re
import collections
import nltk
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('wordnet')
from nltk.stem.wordnet import WordNetLemmatizer
lmtzr = WordNetLemmatizer()
from nltk.tokenize import word_tokenize
import xlwt
import glob
import os
def get_file_name(path):
    i = 0
    name_flag = 0
    file_name = ""
    if(path[0] == '.'):
        i += 2
    while(i < len(path)):
        if(name_flag != 0):
            file_name += path[i]
        if(path[i] == '/'):
            name_flag = 1
        i += 1
    if('/' in file_name):
        return get_file_name(file_name)
    else:
        return file_name
def divide_file_name(name):
    i = 0
    before = ""
    after = ""
    divide_flag = 0
    while(i < len(name)):
        if(name[i] == '.'):
            divide_flag = 1
        if(divide_flag == 0):
            before += name[i]
        else:
            after += name[i]
        i += 1
    return before, after
# patterns that used to find or/and replace particular chars or words
# to find chars that are not a letter, a blank or a quotation
pat_letter = re.compile(r'[^a-zA-Z \']+')
# to find the 's following the pronouns. re.I is refers to ignore case
pat_is = re.compile("(it|he|she|that|this|there|here)(\'s)", re.I)
# to find the 's following the letters
pat_s = re.compile("(?<=[a-zA-Z])\'s")
# to find the ' following the words ending by s
pat_s2 = re.compile("(?<=s)\'s?")
# to find the abbreviation of not
pat_not = re.compile("(?<=[a-zA-Z])n\'t")
# to find the abbreviation of would
pat_would = re.compile("(?<=[a-zA-Z])\'d")
# to find the abbreviation of will
pat_will = re.compile("(?<=[a-zA-Z])\'ll")
# to find the abbreviation of am
pat_am = re.compile("(?<=[I|i])\'m")
# to find the abbreviation of are
pat_are = re.compile("(?<=[a-zA-Z])\'re")
# to find the abbreviation of have
pat_ve = re.compile("(?<=[a-zA-Z])\'ve")
def open_file(file_path):
    with open(file_path, encoding='utf-8') as f:
        # txt= f.read()
        txt0 = f.readlines()
        txt = [x.strip() for x in txt0]
        txt1 = " ".join(txt)
        txt2 = re.sub('(-\s)', '', txt1)
        return txt2
def replace_abbreviations(text):
    new_text = text
    new_text = pat_letter.sub(' ', text).strip().lower()
    new_text = pat_is.sub(r"\1 is", new_text)
    new_text = pat_s.sub("", new_text)
    new_text = pat_s2.sub("", new_text)
    new_text = pat_not.sub(" not", new_text)
    new_text = pat_would.sub(" would", new_text)
    new_text = pat_will.sub(" will", new_text)
    new_text = pat_am.sub(" am", new_text)
    new_text = pat_are.sub(" are", new_text)
    new_text = pat_ve.sub(" have", new_text)
    new_text = new_text.replace('\'', ' ')
    return new_text
def text_washing(text):
    new_text = re.sub('[,\.()":;!?@#$%^&*\d]|\'s|\'', '', text)  # txet wash
    new_text = re.sub("\W|[0-9]", " ", new_text)
    #deleting the solo character
    # 删掉单个字母
    txt4 = new_text.split(" ")
    list = []
    for i in txt4:
        i = i.strip()
        if len(i) > 2:
            list.append(i)
    wash_text = " ".join(list)
    return wash_text
def merge(text):
    words = text.split()
    new_words = []
    for word in words:
        if word:
            # tag is like [('bigger', 'JJR')]
            tag = nltk.pos_tag(word_tokenize(word))
            pos = get_wordnet_pos(tag[0][1])
            if pos:
                lemmatized_word = lmtzr.lemmatize(word, pos)
                new_words.append(lemmatized_word)
            else:
                new_words.append(word)
    # get rid of stop words
    stopwords = [word.strip().lower() for word in open("stopwords.txt")]
    clean_tokens = [tok for tok in new_words if len(tok) > 1 and (tok not in stopwords)]
    return clean_tokens
def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'):
        return nltk.corpus.wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return nltk.corpus.wordnet.VERB
    elif treebank_tag.startswith('N'):
        return nltk.corpus.wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return nltk.corpus.wordnet.ADV
    else:
        return ''
def append_ext(words_list):
    count = collections.Counter(words_list)
    words = count.most_common()
    new_words = []
    for item in words:
        word, count = item
        # tag is like [('bigger', 'JJR')]
        tag = nltk.pos_tag(word_tokenize(word))[0][1]
        new_words.append((word, count, tag))
    return new_words
def data_write(file_path, datas):
    f = xlwt.Workbook()
    sheet1 = f.add_sheet(u'sheet1', cell_overwrite_ok=True)  # 创建sheet
    # 将数据写入第 i 行，第 j 列
    j = 2
    for data in datas:
        for i in range(len(data)):
            sheet1.write(i, j, data[j])
        i = i + 1
    f.save(file_path)  # 保存文件
def get_csv(file_name_before, output_path,datas): # type(datas) = list
    total_num = len(datas)
    i = -1
    # CC代表并列连词，RB代表副词，IN是介词，NN是名词，JJ是形容词
    csv_name = file_name_before + ".csv"
    csv_path = output_path + "/" + csv_name
    frame = pd.DataFrame(datas, columns=['word', 'freq', 'attribute'])
    frame.to_csv(csv_path)

def main():
    input_path = "./texts"
    output_path = "./word_freqs"
    txts = glob.glob("{}/*.txt".format(input_path))
    total_num = len(txts)
    i = 0
    txt_path = ""
    os.system("rm "+output_path+"/*")
    for txt_path in txts:
        i += 1
        file_name = get_file_name(txt_path)
        file_name_before,_ = divide_file_name(file_name)
        print("[*] %d/%d:%s" % (i, total_num, file_name))
        # get word count
        txt = open_file(txt_path)
        txt = replace_abbreviations(txt)
        txt = text_washing(txt)
        clean_tokens = merge(txt)
        new_words = append_ext(clean_tokens) # list type
        # save word count to csv
        get_csv(file_name_before, output_path, new_words)
    print("Done!")

if __name__ == "__main__":
    main()

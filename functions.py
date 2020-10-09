import pandas as pd
import os
import re
import nltk

def read_csv(file_path):

    df = pd.read_csv(file_path, encoding='utf-8', engine='python', sep=',',  quotechar='"')

    return df


def replace_chars(string):
    string = string.replace('"', '').replace('!', '').replace('?', '').replace(':', '').replace('؟', '').replace('%','')
    return string

def remedy_csv(original_file_path):
    writing_file = WriteFile("C:/Users/TDInstaller/PycharmProjects/inverted_index", "sms_remedy", "csv", f_mode="w+")
    reading_file = open(original_file_path, "r")
    new_file_content = ""
    for line in reading_file:
        stripped_line = line.strip()
        new_line = stripped_line.replace('""', '"')
        new_file_content += new_line + "\n"
        reading_file.close()

        writing_file.write(new_file_content)
        writing_file.close()


def get_stop_words():
    stop_words_list = []
    arb_stopwords_set = set(nltk.corpus.stopwords.words("arabic"))
    eng_stopwords_set = set(nltk.corpus.stopwords.words("english"))
    stop_words_list.extend(list(arb_stopwords_set))
    stop_words_list.extend(list(eng_stopwords_set))
    return stop_words_list

def double_quotes(string):
    if string is None:
        return None
    return """ "%s" """ % string

class WriteFile:
    def __init__(self, file_path, file_name, ext, f_mode="r+", new_line=False):
        self.new_line = new_line
        self.f = open(os.path.join(file_path, file_name + "." + ext), f_mode, encoding="utf-8")

    def write(self, txt, new_line=None):
        self.f.write(txt)
        new_line = self.new_line if new_line is None else None
        self.f.write("\n") if new_line else None

    def close(self):
        self.f.close()


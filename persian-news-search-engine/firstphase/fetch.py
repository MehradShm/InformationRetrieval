from __future__ import unicode_literals
import pandas as pd
import random
import re
from hazm import *
from farsichar import *
from PersianStemmer import PersianStemmer
from parsivar import FindStems
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression

############################## FirstCase Inverted_index Build Requirements
def CleanCharacters(content):
    cleaned_content= ''
    valid_characters = '''ٲ ﺁ ﺍ ﺄ ﺎ إأآاﺏ ﺐ ﺒ ﺑ ب ﭗ ﭘ ﭙ پ ٹ ﺕ ﺘ ﺖ ﺗ ت ﺛ ثﺞ ﺤ ﺠ ﺟ جﭽ ﭽ چ ﺣ
        ح ﺦ ﺨ ﺧ خﺩ ﺪ د ﺬ ذﺭ ﺮ رﺯ ﺰ زﮋ ژ ﺱ ﺲ ﺳ ﺴ سﺵ ﺶ ﺷ ﺸ ش ﺹ ﺻ ﺼ ص ﺽ ﺿ ﻀ ض
        ٹ ﻄ ﻂ ﻃ طﻈ ظ ﻊ ﻉ ﻌ عﻐ ﻏ غ ﻒ ﻑ ﻔ ﻓ ف ﻘ ﻖ ﻗ قﮑ ﮏ ﮐ ﻚ ﻜ ﻛ ك ک ﮒ ﮓ ﮔ ﮕ
         گﻝ ﻞ ﻠ ﻟ لﻡ ﻤ ﻢ ﻣ مﻥ ﻦ ﻨ ﻧ ن ۆ ﻭ ﻮ ؤو ﺓ ﻩ ھ ہ ﻬ ﻪ ﻫ ەۀه
        ﯼ ے ﯽ ﺌ ﻱ ﻰ ﯾ ﯿ ﻴ ﻳ ﻲ ي ﺋ  یﻼ ﻻﷲ ‌'''
    for character in content:
        if character in valid_characters:
            cleaned_content = cleaned_content + character
        else:
            cleaned_content = cleaned_content + ' '
    cleaned_content = re.sub(' +', ' ', content)
    return cleaned_content

def CleanStopWords(content):
    stop_words_list = []
    cleaned_stop_word_list = []
    with open('StopWords.txt', 'r') as SWFile:
        line = SWFile.readline()
        while line:
            stop_words_list.append(line)
            line = SWFile.readline()
    for word in stop_words_list:
        tmp = word.replace(' ','')
        tmp = word.replace('\n','')
        cleaned_stop_word_list.append(tmp)
    for token in content:
        if token in cleaned_stop_word_list:
            content.remove(token)
    return content
############################## SecondCase Inverted Index Build Requirements
def FixHalfSpaces(content):
    NWSC,NWEC = r'«\[\(\{', r'\.:!،؛؟»\]\)\}'  #Non-Word Starting Characters, Non-Word Ending Characters
    replacements = [(r'([^ ]ه) ی ', r'\1‌ی '),
				    (r'(^| )(ن?می) ', r'\1\2‌'),
				    (r'(?<=[^\n\d '+ NWEC + NWSC +']{2}) (تر(ین?)?|گری?|های?)(?=[ \n'+ NWEC + NWSC +']|$)', r'‌\1'),
				    (r'([^ ]ه) (ا(م|یم|ش|ند|ی|ید|ت))(?=[ \n'+ NWEC +']|$)', r'\1‌\2'),
                    (r'([^ ]ی) (ا(م|یم|ش|ند|ی|ید|ت))(?=[ \n'+ NWEC +']|$)', r'\1‌\2')]
    for replacement in replacements:
        content = re.sub(replacement[0],replacement[1],content)
    return content

def NormalizeCharacters(content):
    not_valid_characters = r'[^ابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی ‌]'
    farsi_mapping = create_correct_mapping()
    for first,second in farsi_mapping.items():
        content = re.sub(first,second,content)
    content = re.sub(not_valid_characters,' ',content)
    content = re.sub(' +', ' ', content)
    return content

def TokenizeContent(content):
    compound = []
    with open('compound.txt', 'r') as cmp:
        line = cmp.readline()
        while line:
            p = line.split(',')
            compound.append((p[0],p[1]))
            line = cmp.readline()
    for pair in compound:
        content = re.sub(pair[0],pair[1],content)
    Tokenized_content = word_tokenize(content)
    return Tokenized_content

def CutStopWords(content):
    send = []
    stop_words_list, normalized_stop_word_list = [], []
    with open('StopWords.txt', 'r') as SWFile:
        line = SWFile.readline()
        while line:
            stop_words_list.append(line)
            line = SWFile.readline()
    for word in stop_words_list:
        normalized_stop_word = NormalizeCharacters(word)
        normalized_stop_word = re.sub(' ','',normalized_stop_word)
        normalized_stop_word = re.sub('\n','',normalized_stop_word)
        normalized_stop_word = re.sub('‌','',normalized_stop_word)
        normalized_stop_word_list.append(normalized_stop_word)
    for token in content:
        if token in normalized_stop_word_list:
            content.remove(token)
        else:
            send.append(token)
    return send

def StemTokens(list_of_tokens):
    ps = PersianStemmer()
    my_stemmer = FindStems()
    for token_index in range(0,len(list_of_tokens)):
        tmp = list_of_tokens[token_index]
        flag = False
        stemmed_token = ps.run(my_stemmer.convert_to_stem(list_of_tokens[token_index]))
        if '&' in stemmed_token:
            stems_list = stemmed_token.split('&')
            stems_list[0] = NormalizeCharacters(stems_list[0])
            stems_list[1] = NormalizeCharacters(stems_list[1])
            if list_of_tokens[token_index] in stems_list[0]:
                list_of_tokens[token_index] = stems_list[0]
            else:
                list_of_tokens[token_index] = stems_list[1]
        list_of_tokens[token_index] = re.sub('\u200c','',list_of_tokens[token_index])
        list_of_tokens[token_index] = re.sub('_','',list_of_tokens[token_index])
    return list_of_tokens

def AddToDictionary(dictionary_words,doc_ID,list_of_tokens, Collection_Frequency):
    for token in list_of_tokens:
        if token in dictionary_words.keys():
            dictionary_words[token].add(doc_ID)
            Collection_Frequency[token] += 1
        else:
            dictionary_words[token] = set()
            dictionary_words[token].add(doc_ID)
            Collection_Frequency[token] = 1
    return dictionary_words

def Load_Data(sample_size):
    df1 = pd.read_csv('data/1.csv')
    df2 = pd.read_csv('data/2.csv')
    df3 = pd.read_csv('data/3.csv')
    df4 = pd.read_csv('data/4.csv')
    df5 = pd.read_csv('data/5.csv')
    df6 = pd.read_csv('data/6.csv')
    a = [df1,df2,df3,df4,df5,df6]
    b = [df1.shape[0],df2.shape[0],df3.shape[0],df4.shape[0],df5.shape[0],df6.shape[0]]
    df_sizes = [0,df1.shape[0],df1.shape[0]+df2.shape[0],
                df1.shape[0]+df2.shape[0]+df3.shape[0],
                df1.shape[0]+df2.shape[0]+df3.shape[0]+df4.shape[0],
                df1.shape[0]+df2.shape[0]+df3.shape[0]+df4.shape[0]+df5.shape[0],
                df1.shape[0]+df2.shape[0]+df3.shape[0]+df4.shape[0]+df5.shape[0]+df6.shape[0]]
    sample_data_indices = random.sample(range(0, df_sizes[5]), sample_size)
    Gdata = []
    for doc_index in range(len(sample_data_indices)):
        for i in range(7):
            if sample_data_indices[doc_index] > df_sizes[i] and sample_data_indices[doc_index]<df_sizes[i+1]:
                target_data = a[i].loc[sample_data_indices[doc_index]-df_sizes[i],'content']
                Gdata.append(target_data)
    return (sample_data_indices,Gdata)

def BuildInvertedIndex(data_sample,docIDList, Build_Case):
    sample_dic, total_tokens, distinct_tokens, all_tokens, Collection_Frequency = {}, 0, [], [], {}
    for content_index in range(len(data_sample)-5):
        if content_index%100 == 0:
            print(content_index, "^^^^^^^")
        if Build_Case == 'second':
            normalized_content = NormalizeCharacters(data_sample[content_index])
            cleaned_content = FixHalfSpaces(normalized_content)
        else:
            cleaned_content = CleanCharacters(data_sample[content_index]) # First Case normalized_content = NormalizeCharacters(data_sample[content_index])
        tokenized_content = TokenizeContent(cleaned_content)
        if Build_Case == 'second':
            non_stop_tokens = CutStopWords(tokenized_content)
        else:
            non_stop_tokens = CleanStopWords(tokenized_content) # First Case non_stop_tokens = CutStopWords(tokenized_content)
        total_tokens += len(non_stop_tokens)
        all_tokens.append(total_tokens)
        if Build_Case == 'second':
            stemmed_tokens = StemTokens(non_stop_tokens)
        else:
            stemmed_tokens = non_stop_tokens
        sample_dic = AddToDictionary(sample_dic,docIDList[content_index],non_stop_tokens, Collection_Frequency)
        distinct_tokens.append(len(sample_dic))
    return (sample_dic,total_tokens,distinct_tokens, all_tokens, Collection_Frequency)

def MakeHeapsPlot(all_tokens, distinct_tokens, Build_Case, Sample_Case):
    X = [np.log10(i) for i in all_tokens]
    Y = [np.log10(i) for i in distinct_tokens]
    x = np.array(X).reshape((-1, 1))
    y = np.array(Y)
    model = LinearRegression().fit(x,y)
    a0, a1 = model.intercept_, model.coef_[0]
    tmp = list(range(all_tokens[-1]))
    XFormula = [np.log10(i) for i in tmp]
    YFormula = [a0+(a1)* i for i in XFormula]
    print(a0, "!!!!", a1)
    plt.plot(X, Y, 'r',label = "{}case_{}_Sample".format(Build_Case,Sample_Case))
    plt.plot(XFormula, YFormula, 'm',label = "Heaps-Law {}Case_{}_Sample".format(Build_Case,Sample_Case))
    plt.legend()
    plt.show()

def MakeZipfsPlot(Collection_Frequency, Build_Case, Sample_Case):
    keyval = []
    for key in Collection_Frequency.keys():
        keyval.append((key,Collection_Frequency[key]))
    tmp = sorted(keyval,key=lambda x: x[1], reverse = True)
    K = tmp[0][1]
    Xaxis = [np.log10(i+1) for i in list(range(0,len(keyval)))]
    Yaxis = [np.log10(K) - np.log10(i+1) for i in list(range(0,len(keyval)))]
    YPaxis = [np.log10(tmp[j][1]) for j in list(range(0,len(keyval)))]
    plt.plot(Xaxis,Yaxis,'m', label = '{}_Zipf'.format(Build_Case))
    plt.plot(Xaxis,YPaxis,'y', label = '{}_data_Zipf'.format(Sample_Case))
    plt.legend()
    plt.axis([0,np.log10(K)+4,0,np.log10(K)+4])
    plt.show()

############ Main
first_docID_list, first_sample = Load_Data(5005)
second_docID_list, second_sample = Load_Data(15005)
percise_dic, percise_total_tokens, percise_distinct_tokens, percise_alltokens, pCollection_Frequency= BuildInvertedIndex(first_sample,first_docID_list,'second')
SSpercise_dic, SSpercise_total_tokens, SSpercise_distinct_tokens, SSpercise_alltokens,SSpCollection_Frequency = BuildInvertedIndex(second_sample,second_docID_list,'second')
bad_dic, bad_total_tokens, bad_distinct_tokens, bad_alltokens, bCollection_Frequency = BuildInvertedIndex(first_sample,first_docID_list,'first')
SSbad_dic, SSbad_total_tokens,SSbad_distinct_tokens, SSbad_alltokens, SSbCollection_Frequency = BuildInvertedIndex(second_sample,second_docID_list,'first')

MakeHeapsPlot(percise_alltokens, percise_distinct_tokens, "Second","Smaller")
MakeHeapsPlot(bad_alltokens, bad_distinct_tokens, "First","Smaller")
MakeHeapsPlot(SSpercise_alltokens, SSpercise_distinct_tokens, "Second","Bigger")
MakeHeapsPlot(SSbad_alltokens, SSbad_distinct_tokens, "First","Bigger")

MakeZipfsPlot(pCollection_Frequency,"Second","Smaller")
MakeZipfsPlot(bCollection_Frequency,"First","Smaller")
MakeZipfsPlot(SSpCollection_Frequency,"Second","Bigger")
MakeZipfsPlot(SSbCollection_Frequency,"First","Bigger")

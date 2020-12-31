import re

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
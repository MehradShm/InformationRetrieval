from __future__ import unicode_literals
from RelatedPlots import MakeHeapsPlot, MakeZipfsPlot
from FirstCase import CleanCharacters, CleanStopWords
from LoadData import Load_Data
from SecondCase import FixHalfSpaces,NormalizeCharacters, TokenizeContent, CutStopWords,StemTokens, AddToDictionary
import time

#len(data_sample)-5


def BuildInvertedIndex(data_sample,Build_Case):
    sample_dic, total_tokens, distinct_tokens, all_tokens, Collection_Frequency, term_frequencies = {}, 0, [], [], {}, {}
    for content_index in range(55109):
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
        sample_dic = AddToDictionary(sample_dic,content_index,non_stop_tokens, Collection_Frequency, term_frequencies)
        distinct_tokens.append(len(sample_dic))
    return (sample_dic,total_tokens,distinct_tokens, all_tokens, Collection_Frequency, term_frequencies)

print("started")
start_time = time.time()
first_sample = Load_Data()
#second_docID_list, second_sample = Load_Data(15005)
percise_dic, percise_total_tokens, percise_distinct_tokens, percise_alltokens, pCollection_Frequency, pTerm_Frequencies = BuildInvertedIndex(first_sample,'second')

with open("tf.txt",'w') as terms:
    for key in pTerm_Frequencies.keys():
        terms.write(key+" ")
        for doc_id in pTerm_Frequencies[key]:
            terms.write(str(doc_id)+":"+str(pTerm_Frequencies[key][doc_id])+" ")
        terms.write("\n")
    
with open('inverted_index.txt','w') as index:
    for key in percise_dic.keys():
        index.write(key+" ")
        for doc_id in percise_dic[key]:
            index.write(str(doc_id)+" ")
        index.write("\n")
print("--- %s seconds ---" % (time.time() - start_time))



#SSpercise_dic, SSpercise_total_tokens, SSpercise_distinct_tokens, SSpercise_alltokens,SSpCollection_Frequency = BuildInvertedIndex(second_sample,second_docID_list,'second')
#bad_dic, bad_total_tokens, bad_distinct_tokens, bad_alltokens, bCollection_Frequency = BuildInvertedIndex(first_sample,first_docID_list,'first')
#SSbad_dic, SSbad_total_tokens,SSbad_distinct_tokens, SSbad_alltokens, SSbCollection_Frequency = BuildInvertedIndex(second_sample,second_docID_list,'first')

#MakeHeapsPlot(percise_alltokens, percise_distinct_tokens, "Second","Smaller")
#MakeHeapsPlot(bad_alltokens, bad_distinct_tokens, "First","Smaller")
#MakeHeapsPlot(SSpercise_alltokens, SSpercise_distinct_tokens, "Second","Bigger")
#MakeHeapsPlot(SSbad_alltokens, SSbad_distinct_tokens, "First","Bigger")

#MakeZipfsPlot(pCollection_Frequency,"Second","Smaller")
#MakeZipfsPlot(bCollection_Frequency,"First","Smaller")
#MakeZipfsPlot(SSpCollection_Frequency,"Second","Bigger")
#MakeZipfsPlot(SSbCollection_Frequency,"First","Bigger")
